import uuid

import pyxb

from metarecord.binding import jhs
from metarecord.models import Function


class JHSExporter:
    NAMESPACE = 'tos'
    TOS_VERSION = '1'

    JHS_MAPPING = {
        'PublicityClass': {
            'Julkinen': '1',
            'Osittain salassapidettävä': '2',
            'Salassa pidettävä': '3',
            'Ei-julkinen': '4'
        },
        'PersonalData': {
            'Ei sisällä henkilötietoja': '1',
            'Sisältää henkilötietoja': '2',
            'Sisältää arkaluonteisia henkilötietoja': '3'
        }
    }

    def __init__(self, output=False):
        self.output = output

    def msg(self, text):
        if self.output:
            print(text)

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
            SailytysajanPerusteTeksti=self._get_attribute_value(obj, 'RetentionReason')
        )

    def _handle_record(self, record):
        information_system = self._get_attribute_value(record, 'InformationSystem')

        return jhs.Asiakirjatieto(
            id=record.id,
            Kayttorajoitustiedot=self._create_restriction_info(record),
            Sailytysaikatiedot=self._create_retention_info(record),
            AsiakirjaluokkaTeksti=jhs.AsiakirjaluokkaTeksti(self._get_attribute_value(record, 'RecordType')),
            AsiakirjaluokkaTarkenneTeksti=jhs.AsiakirjaluokkaTarkenneTeksti(record.get_name()),
            TietojarjestelmaNimi=jhs.TietojarjestelmaNimi(information_system) if information_system else None
        )

    def _handle_action(self, action, records):
        return jhs.Toimenpidetiedot(
            id=action.id,
            ToimenpideluokkaTeksti=action.get_name(),
            Asiakirjatieto=records
        )

    def _handle_phase(self, phase, actions):
        return jhs.Toimenpidetiedot(
            id=phase.id,
            ToimenpideluokkaTeksti=phase.get_name(),
            Toimenpidetiedot=actions
        )

    def _handle_function(self, function, phases):
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
            Luokitustunnus=function.function_id,
            Nimeke=jhs.Nimeke(jhs.NimekeKielella(function.name, kieliKoodi='fi')),
            KasittelyprosessiTiedot=handling_process_info
        )

    def create_xml(self):
        pyxb.utils.domutils.BindingDOMSupport.DeclareNamespace(jhs.Namespace, self.NAMESPACE)

        tos_info = jhs.TosTiedot(
            id=uuid.uuid4(),
            Nimeke=jhs.Nimeke(jhs.NimekeKielella('TOS dokumentti', kieliKoodi='fi')),
            YhteyshenkiloNimi='John Doe',  # TODO
            TosVersio=self.TOS_VERSION
        )

        # at least for now include all functions that have data
        function_qs = Function.objects.exclude(phases__isnull=True).latest_version()
        function_qs = function_qs.prefetch_related('phases', 'phases__actions', 'phases__actions__records')

        functions = []
        for function in function_qs:
            self.msg('processing function %s' % function)
            phases = []
            handling = None
            func = None
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
                    self.msg('ERROR %s while processing %s' % (error, handling))
                else:
                    self.msg('ERROR %s' % error)
            if func:
                try:
                    func.toDOM()  # validates
                    functions.append(func)
                except pyxb.PyXBException as e:
                    self.msg('ERROR validating the function, details:\n%s' % e.details())

        self.msg('creating the actual XML...')

        tos_root = jhs.Tos(
            TosTiedot=tos_info,
            Luokka=functions,
        )

        dom = tos_root.toDOM()
        return dom.toprettyxml(' ', encoding='utf-8')

    def export_data(self, filename):
        self.msg('exporting data...')
        xml = self.create_xml()

        with open(filename, 'wb') as f:
            self.msg('writing to the file...')
            f.write(xml)

            self.msg('Done.')
