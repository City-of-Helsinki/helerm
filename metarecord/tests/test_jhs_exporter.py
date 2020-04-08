import uuid
from unittest import mock

import freezegun
import pytest

from metarecord.exporter.jhs import JHSExporter
from metarecord.models import Function


@pytest.mark.django_db
def test_exporter_xml_generation_is_successful(function, phase, action, record):
    function.state = Function.APPROVED
    function.save(update_fields=('attributes', 'state'))

    with freezegun.freeze_time('2020-04-01 12:00 EEST'):
        mock_uuid = uuid.uuid4()

        with mock.patch('uuid.uuid4', return_value=mock_uuid):
            xml = JHSExporter().create_xml().decode('utf-8')

    assert xml == """<?xml version="1.0" encoding="utf-8"?>
<tos:Tos xmlns:tos="http://skeemat.jhs-suositukset.fi/tos/2015/01/15">
 <tos:TosTiedot tos:id="{id}">
  <tos:Nimeke>
   <tos:NimekeKielella tos:kieliKoodi="fi">
    <tos:NimekeTeksti>Helsingin kaupungin Tiedonohjaussuunnitelma</tos:NimekeTeksti>
   </tos:NimekeKielella>
  </tos:Nimeke>
  <tos:YhteyshenkiloNimi>Tiedonhallinta</tos:YhteyshenkiloNimi>
  <tos:TosVersio>1</tos:TosVersio>
  <tos:TilaKoodi>3</tos:TilaKoodi>
  <tos:OrganisaatioNimi>Helsingin kaupunki</tos:OrganisaatioNimi>
  <tos:LisatiedotTeksti>JHS 191 XML 2020-04-01 12:00EEST exported from undefined environment</tos:LisatiedotTeksti>
 </tos:TosTiedot>
 <tos:Luokka tos:id="{func_id}">
  <tos:Luokitustunnus>00 00</tos:Luokitustunnus>
  <tos:Nimeke>
   <tos:NimekeKielella tos:kieliKoodi="fi">
    <tos:NimekeTeksti>test classification</tos:NimekeTeksti>
   </tos:NimekeKielella>
  </tos:Nimeke>
  <tos:KasittelyprosessiTiedot tos:id="{id}">
   <tos:Kayttorajoitustiedot/>
   <tos:Sailytysaikatiedot/>
   <tos:Toimenpidetiedot tos:id="{phase_id}">
    <tos:ToimenpideluokkaTarkenneTeksti>test phase</tos:ToimenpideluokkaTarkenneTeksti>
    <tos:Toimenpidetiedot tos:id="{action_id}">
     <tos:ToimenpideluokkaTarkenneTeksti>test action</tos:ToimenpideluokkaTarkenneTeksti>
     <tos:Asiakirjatieto tos:id="{rec_id}">
      <tos:Kayttorajoitustiedot/>
      <tos:Sailytysaikatiedot/>
      <tos:AsiakirjaluokkaTeksti>None</tos:AsiakirjaluokkaTeksti>
      <tos:AsiakirjaluokkaTarkenneTeksti>test record</tos:AsiakirjaluokkaTarkenneTeksti>
     </tos:Asiakirjatieto>
    </tos:Toimenpidetiedot>
   </tos:Toimenpidetiedot>
  </tos:KasittelyprosessiTiedot>
 </tos:Luokka>
</tos:Tos>
""".format(
        id=mock_uuid,
        func_id=function.uuid,
        phase_id=phase.uuid,
        action_id=action.uuid,
        rec_id=record.uuid
    )
