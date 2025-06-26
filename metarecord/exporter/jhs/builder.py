import uuid

from django.conf import settings
from django.db.models import QuerySet
from django.utils import timezone

from metarecord.exporter.jhs import bindings
from metarecord.exporter.jhs.constants import TOS_VERSION
from metarecord.models import Action, Classification, Function, Phase

JHS_MAPPING = {
    "PublicityClass": {
        "Julkinen": "1",
        "Osittain salassapidettävä": "2",
        "Osittain salassa pidettävä": "2",
        "Salassa pidettävä": "3",
        "Ei-julkinen": "4",
    },
    "PersonalData": {
        "Ei sisällä henkilötietoja": "1",
        "Sisältää henkilötietoja": "2",
        "Sisältää arkaluonteisia henkilötietoja": "3",
        "Sisältää erityisiä henkilötietoja": "4",
        "Sisältää rikoksiin tai rikkomuksiin liittyvää henkilötietoa": "5",
    },
}


def _get_attribute_value(obj, attribute_identifier: str):
    """
    Get the value of the given attribute from the given object.
    If there is a mapping available for the attribute, use it.

    :param obj: The object to get the attribute from
    :param attribute_identifier: The attribute to get the value from
    :return: The value of the attribute
    """
    value = obj.attributes.get(attribute_identifier)
    if value is None:
        return None

    jhs_mapping = JHS_MAPPING.get(attribute_identifier)
    if jhs_mapping:
        try:
            value = jhs_mapping[value]
        except KeyError:
            raise ValueError("Invalid value for %s: %s" % (attribute_identifier, value))
    return value


def _create_element_from_obj_attr(obj, element, attr: str, default=None):
    """
    Create an element from the given attribute of the given object.
    If the attribute is None, return the default value instead.

    :param obj: The object to get the attribute from
    :param element: The element to create
    :param attr: The attribute to get the value from
    :param default: The default value to use if the attribute is None
    :return: The created element
    """
    value = _get_attribute_value(obj, attr)
    if value is None:
        return element(default)
    return element(value)


def _create_element_or_none_from_obj_attr(obj, element, attr: str):
    """
    Create an element from the given attribute of the given object.
    If the attribute is None, return None instead.

    :param obj: The object to get the attribute from
    :param element: The element to create
    :param attr: The attribute to get the value from
    :return: The created element or None
    """
    value = _get_attribute_value(obj, attr)
    if value is None:
        return None
    return element(value)


def _generate_elements_from_obj(obj, element_to_attribute: dict):
    """
    Generate elements from the given attributes of the given object.

    :param obj: The object to get the attributes from
    :param element_to_attribute: A dictionary mapping elements to attributes
    :return: A list of elements
    """
    elements = [
        _create_element_or_none_from_obj_attr(obj, elem, attr)
        for elem, attr in element_to_attribute.items()
    ]
    return elements


def _build_restriction_info(obj):
    sub_elements = _generate_elements_from_obj(
        obj,
        {
            bindings.JULKISUUSLUOKKA_KOODI: "PublicityClass",
            bindings.HENKILOTIETOLUONNE_KOODI: "PersonalData",
            bindings.SALASSAPITO_AIKA_ARVO: "SecurityPeriod",
            bindings.SALASSAPITO_PERUSTE_TEKSTI: "SecurityReason",
            bindings.SALASSAPIDON_LASKENTAPERUSTE_TEKSTI: "Restriction.SecurityPeriodStart",  # noqa: E501
        },
    )
    return bindings.KAYTTORAJOITUSTIEDOT(*sub_elements)


def _build_retention_info(obj):
    sub_elements = _generate_elements_from_obj(
        obj,
        {
            bindings.SAILYTYSAJAN_PITUUS_ARVO: "RetentionPeriod",
            bindings.SAILYTYSAJAN_PERUSTE_TEKSTI: "RetentionReason",
            bindings.SAILYTYSAJAN_LASKENTAPERUSTE_TEKSTI: "RetentionPeriodStart",
        },
    )
    return bindings.SAILYTYSAIKATIEDOT(*sub_elements)


def _build_record(record):
    return bindings.ASIAKIRJATIETO(
        _build_restriction_info(record),
        _build_retention_info(record),
        # NOTE: This returns "None" as a string, because it's how
        # the old PyXB implementation did it.
        _create_element_from_obj_attr(
            record, bindings.ASIAKIRJALUOKKA_TEKSTI, "RecordType", default="None"
        ),
        _create_element_from_obj_attr(
            record,
            bindings.ASIAKIRJALUOKKA_TARKENNE_TEKSTI,
            "TypeSpecifier",
            default="None",
        ),
        _create_element_or_none_from_obj_attr(
            record, bindings.TIETOJARJESTELMA_NIMI, "InformationSystem"
        ),
        id=str(record.uuid),
    )


def _build_action(action: Action):
    records = [_build_record(record) for record in action.records.all()]
    return bindings.TOIMENPIDETIEDOT(
        _create_element_or_none_from_obj_attr(
            action, bindings.TOIMENPIDELUOKKA_TEKSTI, "ActionType"
        ),
        _create_element_or_none_from_obj_attr(
            action, bindings.TOIMENPIDELUOKKA_TARKENNE_TEKSTI, "TypeSpecifier"
        ),
        *records,
        id=str(action.uuid),
    )


def _build_phase(phase: Phase):
    actions = [_build_action(action) for action in phase.actions.all()]
    return bindings.TOIMENPIDETIEDOT(
        _create_element_or_none_from_obj_attr(
            phase, bindings.TOIMENPIDELUOKKA_TEKSTI, "PhaseType"
        ),
        _create_element_or_none_from_obj_attr(
            phase, bindings.TOIMENPIDELUOKKA_TARKENNE_TEKSTI, "TypeSpecifier"
        ),
        *actions,
        id=str(phase.uuid),
    )


def _build_function(function: Function):
    phases = [_build_phase(phase) for phase in function.phases.all()]
    return bindings.LUOKKA(
        bindings.LUOKITUSTUNNUS(function.get_classification_code()),
        bindings.NIMEKE(
            bindings.NIMEKE_KIELELLA(
                bindings.NIMEKE_TEKSTI(function.get_name()), kieliKoodi="fi"
            )
        ),
        bindings.KASITTELYPROSESSI_TIEDOT(
            _build_restriction_info(function),
            _build_retention_info(function),
            _create_element_or_none_from_obj_attr(
                function, bindings.TIETOJARJESTELMA_NIMI, "InformationSystem"
            ),
            *phases,
            id=str(uuid.uuid4()),
        ),
        id=str(function.uuid),
    )


def _build_classification(classification: Classification):
    try:
        func = (
            Function.objects.prefetch_related(
                "phases", "phases__actions", "phases__actions__records"
            )
            .filter(classification__uuid=classification.uuid)
            .latest_approved()
            .get()
        )
    except Function.DoesNotExist:
        # No functions found, return only the classification.
        return bindings.LUOKKA(
            bindings.LUOKITUSTUNNUS(classification.code),
            bindings.NIMEKE(
                bindings.NIMEKE_KIELELLA(
                    bindings.NIMEKE_TEKSTI(classification.title),
                    kieliKoodi="fi",
                )
            ),
            id=str(classification.uuid),
        )

    return _build_function(func)


def _build_tos_info():
    return bindings.TOS_TIEDOT(
        bindings.NIMEKE(
            bindings.NIMEKE_KIELELLA(
                bindings.NIMEKE_TEKSTI("Helsingin kaupungin Tiedonohjaussuunnitelma"),
                kieliKoodi="fi",
            )
        ),
        bindings.YHTEYSHENKILO_NIMI("Tiedonhallinta"),
        bindings.TOS_VERSIO(TOS_VERSION),
        bindings.TILA_KOODI("3"),
        bindings.ORGANISAATIO_NIMI("Helsingin kaupunki"),
        bindings.LISATIEDOT(
            "JHS 191 XML {:%Y-%m-%d %H:%M%Z} {}".format(
                timezone.localtime(timezone.now()),
                settings.XML_EXPORT_DESCRIPTION,
            )
        ),
        id=str(uuid.uuid4()),
    )


def build_tos_document(classifications_qs: QuerySet[Classification]):
    """
    Builds a full TOS XML document from the given queryset of classifications.
    """
    classifications = [_build_classification(c) for c in classifications_qs]
    tos_info = _build_tos_info()
    return bindings.TOS(
        tos_info,
        *classifications,
    )
