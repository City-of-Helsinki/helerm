import logging
import uuid

import pyxb

from django.conf import settings
from datetime import datetime
import pytz

from metarecord.binding import jhs
from metarecord.models import Function, Classification

logger = logging.getLogger(__name__)


class JHSExporterException(Exception):
    pass


class JHSExporter:
    NAMESPACE = 'tos'
    TOS_VERSION = '1'

    JHS_MAPPING = {
        'PublicityClass': {
            'Julkinen': '1',
            'Osittain salassapidettävä': '2',
            'Osittain salassa pidettävä': '2',
            'Salassa pidettävä': '3',
            'Ei-julkinen': '4'
        },
        'PersonalData': {
            'Ei sisällä henkilötietoja': '1',
            'Sisältää henkilötietoja': '2',
            'Sisältää arkaluonteisia henkilötietoja': '3',
            'Sisältää erityisiä henkilötietoja': '4',
            'Sisältää rikoksiin tai rikkomuksiin liittyvää henkilötietoa': '5',
        }
    }

    def _get_attribute_value(self, obj, attribute_identifier):
        value = obj.attributes.get(attribute_identifier)
        if value is None:
            return None

        jhs_mapping = self.JHS_MAPPING.get(attribute_identifier)
        if jhs_mapping:
            try:
                value = jhs_mapping[value]
            except KeyError:
                raise Exception('Invalid value for %s: %s' % (attribute_identifier, value))
        return value

    def _create_restriction_info(self, obj):
        return jhs.Kayttorajoitustiedot(
            JulkisuusluokkaKoodi=self._get_attribute_value(obj, 'PublicityClass'),
            HenkilotietoluonneKoodi=self._get_attribute_value(obj, 'PersonalData'),
            SalassapitoAikaArvo=self._get_attribute_value(obj, 'SecurityPeriod'),
            SalassapitoPerusteTeksti=self._get_attribute_value(obj, 'SecurityReason'),
            SalassapidonLaskentaperusteTeksti=self._get_attribute_value(obj, 'Restriction.SecurityPeriodStart')
        )

    def _create_retention_info(self, obj):
        return jhs.Sailytysaikatiedot(
            SailytysajanPituusArvo=self._get_attribute_value(obj, 'RetentionPeriod'),
            SailytysajanPerusteTeksti=self._get_attribute_value(obj, 'RetentionReason'),
            SailytysajanLaskentaperusteTeksti=self._get_attribute_value(obj, 'RetentionPeriodStart')
        )

    def _handle_record(self, record):
        logger.info("Handling record %s" % record.pk)
        information_system = self._get_attribute_value(record, 'InformationSystem')

        return jhs.Asiakirjatieto(
            id=record.uuid,
            Kayttorajoitustiedot=self._create_restriction_info(record),
            Sailytysaikatiedot=self._create_retention_info(record),
            AsiakirjaluokkaTeksti=jhs.AsiakirjaluokkaTeksti(self._get_attribute_value(record, 'RecordType')),
            AsiakirjaluokkaTarkenneTeksti=jhs.AsiakirjaluokkaTarkenneTeksti(
                self._get_attribute_value(record, 'TypeSpecifier')
            ),
            TietojarjestelmaNimi=jhs.TietojarjestelmaNimi(information_system) if information_system else None
        )

    def _handle_action(self, action, records):
        logger.info("Handling action %s" % action.pk)
        ToimenpideTiedot = jhs.Toimenpidetiedot(
            id=action.uuid,
            Asiakirjatieto=records,
        )

        action_type = self._get_attribute_value(action, 'ActionType')
        if action_type:
            ToimenpideTiedot.ToimenpideluokkaTeksti = action_type
        type_specifier = self._get_attribute_value(action, 'TypeSpecifier')
        if type_specifier:
            ToimenpideTiedot.ToimenpideluokkaTarkenneTeksti = type_specifier

        return ToimenpideTiedot

    def _handle_phase(self, phase, actions):
        logger.info("Handling phase %s" % phase.pk)
        ToimenpideTiedot = jhs.Toimenpidetiedot(
            id=phase.uuid,
            Toimenpidetiedot=actions
        )

        phase_type = self._get_attribute_value(phase, 'PhaseType')
        if phase_type:
            ToimenpideTiedot.ToimenpideluokkaTeksti = phase_type
        type_specifier = self._get_attribute_value(phase, 'TypeSpecifier')
        if type_specifier:
            ToimenpideTiedot.ToimenpideluokkaTarkenneTeksti = type_specifier

        return ToimenpideTiedot

    def _handle_function(self, function, phases):
        logger.info("Handling function %s" % function.pk)
        information_system = self._get_attribute_value(function, 'InformationSystem')
        handling_process_info = jhs.KasittelyprosessiTiedot(
            id=uuid.uuid4(),
            Kayttorajoitustiedot=self._create_restriction_info(function),
            Sailytysaikatiedot=self._create_retention_info(function),
            TietojarjestelmaNimi=jhs.TietojarjestelmaNimi(information_system) if information_system else None,
            Toimenpidetiedot=phases
        )
        return jhs.Luokka(
            id=function.uuid,
            Luokitustunnus=function.get_classification_code(),
            Nimeke=jhs.Nimeke(jhs.NimekeKielella(function.get_name(), kieliKoodi='fi')),
            KasittelyprosessiTiedot=handling_process_info
        )

    def _handle_classification(self, classification):
        try:
            function = Function.objects.prefetch_related(
                'phases', 'phases__actions', 'phases__actions__records'
            ).filter(classification=classification).latest_approved().get()

        except Function.DoesNotExist:
            return jhs.Luokka(
                id=classification.uuid,
                Luokitustunnus=classification.code,
                Nimeke=jhs.Nimeke(jhs.NimekeKielella(classification.title, kieliKoodi='fi')),
            )

        logger.info('Processing function %s' % function)

        phases = []
        handling = None
        try:
            for phase in function.phases.all():
                actions = []
                for action in phase.actions.all():
                    records = []
                    for record in action.records.all():
                        handling = record
                        records.append(self._handle_record(record))
                    handling = action
                    actions.append(self._handle_action(action, records))
                handling = phase
                phases.append(self._handle_phase(phase, actions))
            handling = function
            func = self._handle_function(function, phases)
        except Exception as e:
            error = '%s: %s' % (e.__class__.__name__, e)
            if handling:
                logger.error('ERROR %s while processing %s' % (error, handling))
                return False
            else:
                logger.error(error)
                return False
        if func:
            try:
                func.toDOM()  # validates
            except pyxb.PyXBException as e:
                logger.error('ERROR validating the function, details:\n%s' % e.details())
                return False

        return func

    def get_queryset(self):
        # at least for now include all classifications
        qs = Classification.objects
        return qs

    def create_xml(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        pyxb.utils.domutils.BindingDOMSupport.DeclareNamespace(jhs.Namespace, self.NAMESPACE)

        tos_info = jhs.TosTiedot(
            id=uuid.uuid4(),
            Nimeke=jhs.Nimeke(jhs.NimekeKielella('Helsingin kaupungin Tiedonohjaussuunnitelma', kieliKoodi='fi')),
            OrganisaatioNimi='Helsingin kaupunki',
            YhteyshenkiloNimi='Tiedonhallinta',
            LisatiedotTeksti='JHS 191 XML {:%Y-%m-%d %H:%M%Z} {}'.format(
                datetime.now(tz=pytz.timezone(settings.TIME_ZONE)),
                settings.XML_EXPORT_DESCRIPTION),
            TilaKoodi='3',
            TosVersio=self.TOS_VERSION
        )

        classifications = []
        for classification in queryset.all():
            item = self._handle_classification(classification)
            if item:
                classifications.append(item)

        classifications.sort(key=lambda a: a.Luokitustunnus)
        logger.info('Creating the actual XML...')

        tos_root = jhs.Tos(
            TosTiedot=tos_info,
            Luokka=classifications,
        )

        try:
            dom = tos_root.toDOM()
        except pyxb.PyXBException as e:
            logger.error('ERROR while creating the XML file: %s' % e.details())
            raise JHSExporterException(e.details())

        return dom.toprettyxml(' ', encoding='utf-8')

    def export_data(self, filename):
        logger.info('Exporting data...')
        xml = self.create_xml()

        try:
            with open(filename, 'wb') as f:
                logger.info('Writing to the file...')
                f.write(xml)
                logger.info('File written')
        except Exception as e:
            logger.error('ERROR writing to the file: %s' % e)
            raise JHSExporterException(e)
