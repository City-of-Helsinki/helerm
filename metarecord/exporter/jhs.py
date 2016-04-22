import uuid

import pyxb

from metarecord.binding import jhs
from metarecord.models import Function


class JHSExporter:
    NAMESPACE = 'tos'
    TOS_VERSION = '1'

    JHS_MAPPING = {
        'publicity_class': {
            'Julkinen': '1',
            'Osittain salassapidettävä': '2',
            'Salassa pidettävä': '3',
            'Ei-julkinen': '4'
        },
        'personal_data': {
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

    def _get_value(self, obj, field_name):
        value = getattr(obj, field_name)
        if value is None:
            return None
        value = str(value)
        jhs_mapping = self.JHS_MAPPING.get(field_name)
        if jhs_mapping:
            value = jhs_mapping[value]
        return value

    def _create_restriction_info(self, obj):
        return jhs.Kayttorajoitustiedot(
            JulkisuusluokkaKoodi=self._get_value(obj, 'publicity_class'),
            HenkilotietoluonneKoodi=self._get_value(obj, 'personal_data'),
            SalassapitoAikaArvo=self._get_value(obj, 'security_period'),
            SalassapitoPerusteTeksti=self._get_value(obj, 'security_reason'),
            SalassapidonLaskentaperusteTeksti=self._get_value(obj, 'security_period_calculation_basis')
        )

    def _create_retention_info(self, obj):
        return jhs.Sailytysaikatiedot(
            SailytysajanPituusArvo=self._get_value(obj, 'retention_period'),
            SailytysajanPerusteTeksti=self._get_value(obj, 'retention_reason')
        )

    def _handle_record(self, record):
        information_system = self._get_value(record, 'information_system')

        return jhs.Asiakirjatieto(
            id=self._get_value(record, 'id'),
            Kayttorajoitustiedot=self._create_restriction_info(record),
            Sailytysaikatiedot=self._create_retention_info(record),
            AsiakirjaluokkaTeksti=jhs.AsiakirjaluokkaTeksti(self._get_value(record, 'type')),
            AsiakirjaluokkaTarkenneTeksti=jhs.AsiakirjaluokkaTarkenneTeksti(self._get_value(record, 'name')),
            TietojarjestelmaNimi=jhs.TietojarjestelmaNimi(information_system) if information_system else None
        )

    def _handle_action(self, action, records):
        return jhs.Toimenpidetiedot(
            id=self._get_value(action, 'id'),
            ToimenpideluokkaTeksti=self._get_value(action, 'name'),
            Asiakirjatieto=records
        )

    def _handle_phase(self, phase, actions):
        return jhs.Toimenpidetiedot(
            id=self._get_value(phase, 'id'),
            ToimenpideluokkaTeksti=self._get_value(phase, 'name'),
            Toimenpidetiedot=actions
        )

    def _handle_function(self, function, phases):
        information_system = self._get_value(function, 'information_system')
        handling_process_info = jhs.KasittelyprosessiTiedot(
            id=uuid.uuid4(),
            Kayttorajoitustiedot=self._create_restriction_info(function),
            Sailytysaikatiedot=self._create_retention_info(function),
            TietojarjestelmaNimi=jhs.TietojarjestelmaNimi(information_system) if information_system else None,
            Toimenpidetiedot=phases
        )
        return jhs.Luokka(
            id=self._get_value(function, 'id'),
            Luokitustunnus=self._get_value(function, 'function_id'),
            Nimeke=jhs.Nimeke(jhs.NimekeKielella(self._get_value(function, 'name'), kieliKoodi='fi')),
            KasittelyprosessiTiedot=handling_process_info
        )

    def create_xml(self):
        pyxb.utils.domutils.BindingDOMSupport.DeclareNamespace(jhs.Namespace, self.NAMESPACE)

        tos_info = jhs.TosTiedot(
            id=uuid.uuid4(),
            Nimeke=jhs.Nimeke(jhs.NimekeKielella('TOS dokumentti', kieliKoodi='fi')),
            YhteyshenkiloNimi='John Doe',
            TosVersio=self.TOS_VERSION
        )

        # at least for now include all functions that have data
        function_qs = Function.objects.exclude(phases__isnull=True)

        functions = []
        for function in function_qs:
            self.msg('processing function %s' % function)
            phases = []
            for phase in function.phases.all():
                actions = []
                for action in phase.actions.all():
                    records = []
                    for record in action.records.all():
                        records.append(self._handle_record(record))
                    actions.append(self._handle_action(action, records))
                phases.append(self._handle_phase(phase, actions))
            try:
                func = self._handle_function(function, phases)
                func.toDOM()  # validates
                functions.append(func)
            except Exception as e:
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
