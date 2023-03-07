import logging
import uuid
from datetime import datetime

import pytz
from django.conf import settings
from lxml import etree, objectify

from metarecord.models import Classification, Function

logger = logging.getLogger(__name__)

JHS_NAMESPACE = "http://skeemat.jhs-suositukset.fi/tos/2015/01/15"

E = objectify.ElementMaker(
    annotate=False,
    namespace=JHS_NAMESPACE,
    nsmap={"tos": JHS_NAMESPACE},
)

TOS_PREFIX = f"{{{JHS_NAMESPACE}}}"

TOS = E.Tos
TOS_TIEDOT = E.TosTiedot
LUOKKA = E.Luokka
LAAJENNOS = E.Laajennos
NIMEKE = E.Nimeke
NIMEKE_KIELELLA = E.NimekeKielella
NIMEKE_TEKSTI = E.NimekeTeksti
ORGANISAATIO_NIMI = E.OrganisaatioNimi
YHTEYSHENKILO_NIMI = E.YhteyshenkiloNimi
LISATIEDOT = E.LisatiedotTeksti
TILA_KOODI = E.TilaKoodi
TOS_VERSIO = E.TosVersio
LUOKITUSTUNNUS = E.Luokitustunnus
LUOKITUSVASTUU = E.Luokitusvastuu
KASITTELYPROSESSI_TIEDOT = E.KasittelyprosessiTiedot
TIETOJARJESTELMA_NIMI = E.TietojarjestelmaNimi

TOIMENPIDETIEDOT = E.Toimenpidetiedot
TOIMENPIDELUOKKA_TEKSTI = E.ToimenpideluokkaTeksti
TOIMENPIDELUOKKA_TARKENNE_TEKSTI = E.ToimenpideluokkaTarkenneTeksti

KAYTTORAJOITUSTIEDOT = E.Kayttorajoitustiedot
JULKISUUSLUOKKA_KOODI = E.JulkisuusluokkaKoodi
HENKILOTIETOLUONNE_KOODI = E.HenkilotietoluonneKoodi
SALASSAPITO_AIKA_ARVO = E.SalassapitoAikaArvo
SALASSAPITO_PERUSTE_TEKSTI = E.SalassapitoPerusteTeksti
SALASSAPIDON_LASKENTAPERUSTE_TEKSTI = E.SalassapidonLaskentaperusteTeksti

SAILYTYSAIKATIEDOT = E.Sailytysaikatiedot
SAILYTYSAJAN_PITUUS_ARVO = E.SailytysajanPituusArvo
SAILYTYSAJAN_PERUSTE_TEKSTI = E.SailytysajanPerusteTeksti
SAILYTYSAJAN_LASKENTAPERUSTE_TEKSTI = E.SailytysajanLaskentaperusteTeksti

ASIAKIRJATIETO = E.Asiakirjatieto
ASIAKIRJALUOKKA_TEKSTI = E.AsiakirjaluokkaTeksti
ASIAKIRJALUOKKA_TARKENNE_TEKSTI = E.AsiakirjaluokkaTarkenneTeksti


def tos_attr(name):
    return f"{TOS_PREFIX}{name}"


def tos_attrs(**attrs):
    return {tos_attr(name): value for name, value in attrs.items()}


def fix_xml_declaration_single_quotes(xml: bytes) -> bytes:
    """
    Fix XML declaration single quotes to double quotes.

    This is a hard-coded feature in lxml, which, at the time of writing,
    isn't getting fixed anytime soon. This is a workaround for that.
    """
    old_declaration = b"<?xml version='1.0' encoding='utf-8'?>"  # single quotes
    if xml.startswith(old_declaration):
        return xml.replace(old_declaration, b'<?xml version="1.0" encoding="utf-8"?>')
    return xml


class JHSExporterException(Exception):
    pass


# TODO: Replace the old exporter (JHSExporter) with this one
class JHSExporterV2:
    NAMESPACE = "tos"
    TOS_VERSION = "1"

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

    def _create_element_from_obj_attr(self, obj, element, attr: str, default=None):
        """
        Create an element from the given attribute of the given object.
        If the attribute is None, return the default value instead.

        :param obj: The object to get the attribute from
        :param element: The element to create
        :param attr: The attribute to get the value from
        :param default: The default value to use if the attribute is None
        :return: The created element
        """
        value = self._get_attribute_value(obj, attr)
        if value is None:
            return element(default)
        return element(value)

    def _create_element_or_none_from_obj_attr(self, obj, element, attr: str):
        """
        Create an element from the given attribute of the given object.
        If the attribute is None, return None instead.

        :param obj: The object to get the attribute from
        :param element: The element to create
        :param attr: The attribute to get the value from
        :return: The created element or None
        """
        value = self._get_attribute_value(obj, attr)
        if value is None:
            return None
        return element(value)

    def _get_attribute_value(self, obj, attribute_identifier: str):
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

        jhs_mapping = self.JHS_MAPPING.get(attribute_identifier)
        if jhs_mapping:
            try:
                value = jhs_mapping[value]
            except KeyError:
                raise Exception(
                    "Invalid value for %s: %s" % (attribute_identifier, value)
                )
        return value

    def _generate_elements_from_obj(self, obj, element_to_attribute: dict):
        """
        Generate elements from the given attributes of the given object.

        :param obj: The object to get the attributes from
        :param element_to_attribute: A dictionary mapping elements to attributes
        :return: A list of elements
        """
        elements = [
            self._create_element_or_none_from_obj_attr(obj, elem, attr)
            for elem, attr in element_to_attribute.items()
        ]
        return elements

    def _create_restriction_info(self, obj):
        sub_elements = self._generate_elements_from_obj(
            obj,
            {
                JULKISUUSLUOKKA_KOODI: "PublicityClass",
                HENKILOTIETOLUONNE_KOODI: "PersonalData",
                SALASSAPITO_AIKA_ARVO: "SecurityPeriod",
                SALASSAPITO_PERUSTE_TEKSTI: "SecurityReason",
                SALASSAPIDON_LASKENTAPERUSTE_TEKSTI: "Restriction.SecurityPeriodStart",
            },
        )
        return KAYTTORAJOITUSTIEDOT(*sub_elements)

    def _create_retention_info(self, obj):
        sub_elements = self._generate_elements_from_obj(
            obj,
            {
                SAILYTYSAJAN_PITUUS_ARVO: "RetentionPeriod",
                SAILYTYSAJAN_PERUSTE_TEKSTI: "RetentionReason",
                SAILYTYSAJAN_LASKENTAPERUSTE_TEKSTI: "RetentionPeriodStart",
            },
        )
        return SAILYTYSAIKATIEDOT(*sub_elements)

    def _handle_record(self, record):
        return ASIAKIRJATIETO(
            self._create_restriction_info(record),
            self._create_retention_info(record),
            # NOTE: This returns "None" as a string, because it's how
            # the old PyXB implementation did it.
            self._create_element_from_obj_attr(
                record, ASIAKIRJALUOKKA_TEKSTI, "RecordType", default="None"
            ),
            self._create_element_from_obj_attr(
                record, ASIAKIRJALUOKKA_TARKENNE_TEKSTI, "TypeSpecifier", default="None"
            ),
            self._create_element_or_none_from_obj_attr(
                record, TIETOJARJESTELMA_NIMI, "InformationSystem"
            ),
            tos_attrs(id=str(record.uuid)),
        )

    def _handle_action(self, action):
        records = [self._handle_record(record) for record in action.records.all()]
        return TOIMENPIDETIEDOT(
            self._create_element_or_none_from_obj_attr(
                action, TOIMENPIDELUOKKA_TEKSTI, "ActionType"
            ),
            self._create_element_or_none_from_obj_attr(
                action, TOIMENPIDELUOKKA_TARKENNE_TEKSTI, "TypeSpecifier"
            ),
            *records,
            tos_attrs(id=str(action.uuid)),
        )

    def _handle_phase(self, phase):
        actions = [self._handle_action(action) for action in phase.actions.all()]
        return TOIMENPIDETIEDOT(
            self._create_element_or_none_from_obj_attr(
                phase, TOIMENPIDELUOKKA_TEKSTI, "PhaseType"
            ),
            self._create_element_or_none_from_obj_attr(
                phase, TOIMENPIDELUOKKA_TARKENNE_TEKSTI, "TypeSpecifier"
            ),
            *actions,
            tos_attrs(id=str(phase.uuid)),
        )

    def _handle_function(self, function):
        phases = [self._handle_phase(phase) for phase in function.phases.all()]
        return LUOKKA(
            LUOKITUSTUNNUS(function.get_classification_code()),
            NIMEKE(
                NIMEKE_KIELELLA(
                    NIMEKE_TEKSTI(function.get_name()), tos_attrs(kieliKoodi="fi")
                )
            ),
            KASITTELYPROSESSI_TIEDOT(
                self._create_restriction_info(function),
                self._create_retention_info(function),
                self._create_element_or_none_from_obj_attr(
                    function, TIETOJARJESTELMA_NIMI, "InformationSystem"
                ),
                *phases,
                tos_attrs(id=str(uuid.uuid4())),
            ),
            tos_attrs(id=str(uuid.uuid4())),
        )

    def _handle_classification(self, classification):
        try:
            function = (
                Function.objects.prefetch_related(
                    "phases", "phases__actions", "phases__actions__records"
                )
                .filter(classification__uuid=classification.uuid)
                .latest_approved()
                .get()
            )
        except Function.DoesNotExist:
            return LUOKKA(
                LUOKITUSTUNNUS(classification.code),
                NIMEKE(
                    NIMEKE_KIELELLA(
                        NIMEKE_TEKSTI(classification.title),
                        tos_attrs(kieliKoodi="fi"),
                    )
                ),
                tos_attrs(id=str(classification.uuid)),
            )

        # TODO Error handling

        phases = [self._handle_phase(phase) for phase in function.phases.all()]
        return LUOKKA(
            LUOKITUSTUNNUS(function.get_classification_code()),
            NIMEKE(
                NIMEKE_KIELELLA(
                    NIMEKE_TEKSTI(function.get_name()), tos_attrs(kieliKoodi="fi")
                )
            ),
            KASITTELYPROSESSI_TIEDOT(
                self._create_restriction_info(function),
                self._create_retention_info(function),
                self._create_element_or_none_from_obj_attr(
                    function, TIETOJARJESTELMA_NIMI, "InformationSystem"
                ),
                *phases,
                tos_attrs(id=str(uuid.uuid4())),
            ),
            tos_attrs(id=str(function.uuid)),
        )

    def get_queryset(self):
        # at least for now include all classifications
        return Classification.objects.all()

    def create_xml(self, queryset=None):
        queryset = queryset or self.get_queryset()

        tos_info = TOS_TIEDOT(
            NIMEKE(
                NIMEKE_KIELELLA(
                    NIMEKE_TEKSTI("Helsingin kaupungin Tiedonohjaussuunnitelma"),
                    tos_attrs(kieliKoodi="fi"),
                )
            ),
            YHTEYSHENKILO_NIMI("Tiedonhallinta"),
            TOS_VERSIO(self.TOS_VERSION),
            TILA_KOODI("3"),
            ORGANISAATIO_NIMI("Helsingin kaupunki"),
            LISATIEDOT(
                "JHS 191 XML {:%Y-%m-%d %H:%M%Z} {}".format(
                    datetime.now(tz=pytz.timezone(settings.TIME_ZONE)),
                    settings.XML_EXPORT_DESCRIPTION,
                )
            ),
            tos_attrs(id=str(uuid.uuid4())),
        )
        classifications = []
        for classification in queryset:
            classifications.append(self._handle_classification(classification))

        tos_root = TOS(tos_info, *classifications)
        # TODO Error handling
        xml = etree.tostring(
            tos_root,
            xml_declaration=True,
            encoding="utf-8",
            pretty_print=True,
        )
        return fix_xml_declaration_single_quotes(xml)

    def export_data(self, filename):
        logger.info("Exporting data...")
        xml = self.create_xml()

        try:
            with open(filename, "wb") as f:
                logger.info("Writing to the file...")
                f.write(xml)
                logger.info("File written")
        except Exception as e:
            logger.error("ERROR writing to the file: %s" % e)
            raise JHSExporterException(e)
