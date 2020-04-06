# ./metarecord/binding/jhs.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:0bcf4fe07fa483312851437fc9b3f33582a4d3fa
# Generated 2020-04-06 06:44:21.533676 by PyXB version 1.2.6 using Python 3.6.10.final.0
# Namespace http://skeemat.jhs-suositukset.fi/tos/2015/01/15

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six
# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:0bd4d60e-77d2-11ea-a270-0242c0a80003')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
import metarecord.binding._jhs as _ImportedBinding_metarecord_binding__jhs

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://skeemat.jhs-suositukset.fi/tos/2015/01/15', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Atomic simple type: {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}idTyyppi
class idTyyppi (pyxb.binding.datatypes.string):

    """Rakenneosan yksilöivä id-tunnus. Formaattia ei ole määritelty."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'idTyyppi')
    _XSDLocation = None
    _Documentation = 'Rakenneosan yksilöivä id-tunnus. Formaattia ei ole määritelty.'
idTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'idTyyppi', idTyyppi)
_module_typeBindings.idTyyppi = idTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}kieliKoodiTyyppi
class kieliKoodiTyyppi (pyxb.binding.datatypes.string):

    """Kielikoodin avulla elementti voi ilmetä usealla eri kielellä. Suositellaan käytettäväksi standardeja kielikoodeja (fi, se, en).		"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'kieliKoodiTyyppi')
    _XSDLocation = None
    _Documentation = 'Kielikoodin avulla elementti voi ilmetä usealla eri kielellä. Suositellaan käytettäväksi standardeja kielikoodeja (fi, se, en).\t\t'
kieliKoodiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'kieliKoodiTyyppi', kieliKoodiTyyppi)
_module_typeBindings.kieliKoodiTyyppi = kieliKoodiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}tilaKoodiTyyppi
class tilaKoodiTyyppi (pyxb.binding.datatypes.integer, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'tilaKoodiTyyppi')
    _XSDLocation = None
    _Documentation = None
tilaKoodiTyyppi._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=tilaKoodiTyyppi, enum_prefix=None)
tilaKoodiTyyppi._CF_enumeration.addEnumeration(unicode_value='1', tag=None)
tilaKoodiTyyppi._CF_enumeration.addEnumeration(unicode_value='2', tag=None)
tilaKoodiTyyppi._CF_enumeration.addEnumeration(unicode_value='3', tag=None)
tilaKoodiTyyppi._CF_enumeration.addEnumeration(unicode_value='4', tag=None)
tilaKoodiTyyppi._CF_enumeration.addEnumeration(unicode_value='5', tag=None)
tilaKoodiTyyppi._InitializeFacetMap(tilaKoodiTyyppi._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'tilaKoodiTyyppi', tilaKoodiTyyppi)
_module_typeBindings.tilaKoodiTyyppi = tilaKoodiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}versioTyyppi
class versioTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'versioTyyppi')
    _XSDLocation = None
    _Documentation = None
versioTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'versioTyyppi', versioTyyppi)
_module_typeBindings.versioTyyppi = versioTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}luokitustunnusTyyppi
class luokitustunnusTyyppi (pyxb.binding.datatypes.string):

    """Käytettäessä julkisen hallinnon yhteisiä luokituksia, tunnuksena pitää käyttää yhteisen luokituksen mukaista tunnusta."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'luokitustunnusTyyppi')
    _XSDLocation = None
    _Documentation = 'Käytettäessä julkisen hallinnon yhteisiä luokituksia, tunnuksena pitää käyttää yhteisen luokituksen mukaista tunnusta.'
luokitustunnusTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'luokitustunnusTyyppi', luokitustunnusTyyppi)
_module_typeBindings.luokitustunnusTyyppi = luokitustunnusTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}nimekeTekstiTyyppi
class nimekeTekstiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'nimekeTekstiTyyppi')
    _XSDLocation = None
    _Documentation = None
nimekeTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'nimekeTekstiTyyppi', nimekeTekstiTyyppi)
_module_typeBindings.nimekeTekstiTyyppi = nimekeTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}kuvausTekstiTyyppi
class kuvausTekstiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'kuvausTekstiTyyppi')
    _XSDLocation = None
    _Documentation = None
kuvausTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'kuvausTekstiTyyppi', kuvausTekstiTyyppi)
_module_typeBindings.kuvausTekstiTyyppi = kuvausTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}lisatiedotTekstiTyyppi
class lisatiedotTekstiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'lisatiedotTekstiTyyppi')
    _XSDLocation = None
    _Documentation = None
lisatiedotTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'lisatiedotTekstiTyyppi', lisatiedotTekstiTyyppi)
_module_typeBindings.lisatiedotTekstiTyyppi = lisatiedotTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}julkisuusluokkaKoodiTyyppi
class julkisuusluokkaKoodiTyyppi (pyxb.binding.datatypes.integer, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'julkisuusluokkaKoodiTyyppi')
    _XSDLocation = None
    _Documentation = None
julkisuusluokkaKoodiTyyppi._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=julkisuusluokkaKoodiTyyppi, enum_prefix=None)
julkisuusluokkaKoodiTyyppi._CF_enumeration.addEnumeration(unicode_value='1', tag=None)
julkisuusluokkaKoodiTyyppi._CF_enumeration.addEnumeration(unicode_value='2', tag=None)
julkisuusluokkaKoodiTyyppi._CF_enumeration.addEnumeration(unicode_value='3', tag=None)
julkisuusluokkaKoodiTyyppi._CF_enumeration.addEnumeration(unicode_value='4', tag=None)
julkisuusluokkaKoodiTyyppi._InitializeFacetMap(julkisuusluokkaKoodiTyyppi._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'julkisuusluokkaKoodiTyyppi', julkisuusluokkaKoodiTyyppi)
_module_typeBindings.julkisuusluokkaKoodiTyyppi = julkisuusluokkaKoodiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}salassapitoAikaArvoTyyppi
class salassapitoAikaArvoTyyppi (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'salassapitoAikaArvoTyyppi')
    _XSDLocation = None
    _Documentation = None
salassapitoAikaArvoTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'salassapitoAikaArvoTyyppi', salassapitoAikaArvoTyyppi)
_module_typeBindings.salassapitoAikaArvoTyyppi = salassapitoAikaArvoTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}salassapitoPerusteTekstiTyyppi
class salassapitoPerusteTekstiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'salassapitoPerusteTekstiTyyppi')
    _XSDLocation = None
    _Documentation = None
salassapitoPerusteTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'salassapitoPerusteTekstiTyyppi', salassapitoPerusteTekstiTyyppi)
_module_typeBindings.salassapitoPerusteTekstiTyyppi = salassapitoPerusteTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}salassapidonLaskentaperusteTekstiTyyppi
class salassapidonLaskentaperusteTekstiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'salassapidonLaskentaperusteTekstiTyyppi')
    _XSDLocation = None
    _Documentation = None
salassapidonLaskentaperusteTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'salassapidonLaskentaperusteTekstiTyyppi', salassapidonLaskentaperusteTekstiTyyppi)
_module_typeBindings.salassapidonLaskentaperusteTekstiTyyppi = salassapidonLaskentaperusteTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}suojaustasoKoodiTyyppi
class suojaustasoKoodiTyyppi (pyxb.binding.datatypes.integer, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'suojaustasoKoodiTyyppi')
    _XSDLocation = None
    _Documentation = None
suojaustasoKoodiTyyppi._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=suojaustasoKoodiTyyppi, enum_prefix=None)
suojaustasoKoodiTyyppi._CF_enumeration.addEnumeration(unicode_value='1', tag=None)
suojaustasoKoodiTyyppi._CF_enumeration.addEnumeration(unicode_value='2', tag=None)
suojaustasoKoodiTyyppi._CF_enumeration.addEnumeration(unicode_value='3', tag=None)
suojaustasoKoodiTyyppi._CF_enumeration.addEnumeration(unicode_value='4', tag=None)
suojaustasoKoodiTyyppi._InitializeFacetMap(suojaustasoKoodiTyyppi._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'suojaustasoKoodiTyyppi', suojaustasoKoodiTyyppi)
_module_typeBindings.suojaustasoKoodiTyyppi = suojaustasoKoodiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}turvallisuusluokkaKoodiTyyppi
class turvallisuusluokkaKoodiTyyppi (pyxb.binding.datatypes.integer, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'turvallisuusluokkaKoodiTyyppi')
    _XSDLocation = None
    _Documentation = None
turvallisuusluokkaKoodiTyyppi._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=turvallisuusluokkaKoodiTyyppi, enum_prefix=None)
turvallisuusluokkaKoodiTyyppi._CF_enumeration.addEnumeration(unicode_value='1', tag=None)
turvallisuusluokkaKoodiTyyppi._CF_enumeration.addEnumeration(unicode_value='2', tag=None)
turvallisuusluokkaKoodiTyyppi._CF_enumeration.addEnumeration(unicode_value='3', tag=None)
turvallisuusluokkaKoodiTyyppi._CF_enumeration.addEnumeration(unicode_value='4', tag=None)
turvallisuusluokkaKoodiTyyppi._InitializeFacetMap(turvallisuusluokkaKoodiTyyppi._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'turvallisuusluokkaKoodiTyyppi', turvallisuusluokkaKoodiTyyppi)
_module_typeBindings.turvallisuusluokkaKoodiTyyppi = turvallisuusluokkaKoodiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}henkilotietoluonneKoodiTyyppi
class henkilotietoluonneKoodiTyyppi (pyxb.binding.datatypes.integer, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'henkilotietoluonneKoodiTyyppi')
    _XSDLocation = None
    _Documentation = None
henkilotietoluonneKoodiTyyppi._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=henkilotietoluonneKoodiTyyppi, enum_prefix=None)
henkilotietoluonneKoodiTyyppi._CF_enumeration.addEnumeration(unicode_value='1', tag=None)
henkilotietoluonneKoodiTyyppi._CF_enumeration.addEnumeration(unicode_value='2', tag=None)
henkilotietoluonneKoodiTyyppi._CF_enumeration.addEnumeration(unicode_value='3', tag=None)
henkilotietoluonneKoodiTyyppi._CF_enumeration.addEnumeration(unicode_value='4', tag=None)
henkilotietoluonneKoodiTyyppi._CF_enumeration.addEnumeration(unicode_value='5', tag=None)
henkilotietoluonneKoodiTyyppi._InitializeFacetMap(henkilotietoluonneKoodiTyyppi._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'henkilotietoluonneKoodiTyyppi', henkilotietoluonneKoodiTyyppi)
_module_typeBindings.henkilotietoluonneKoodiTyyppi = henkilotietoluonneKoodiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}sailytysajanPituusArvoTyyppi
class sailytysajanPituusArvoTyyppi (pyxb.binding.datatypes.integer):

    """Suositeltavat arvot: 0, 3, 6, 10, 20, 50, 120 tai -1 (pysyvä säilytys)"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'sailytysajanPituusArvoTyyppi')
    _XSDLocation = None
    _Documentation = 'Suositeltavat arvot: 0, 3, 6, 10, 20, 50, 120 tai -1 (pysyvä säilytys)'
sailytysajanPituusArvoTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'sailytysajanPituusArvoTyyppi', sailytysajanPituusArvoTyyppi)
_module_typeBindings.sailytysajanPituusArvoTyyppi = sailytysajanPituusArvoTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}sailytysajanPerusteTekstiTyyppi
class sailytysajanPerusteTekstiTyyppi (pyxb.binding.datatypes.string):

    """Säilytysaika voi perustua lakiin tai olla organisaation oma päätös. Pysyvä säilytys perustuu arkistolaitoksen päätökseen."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'sailytysajanPerusteTekstiTyyppi')
    _XSDLocation = None
    _Documentation = 'Säilytysaika voi perustua lakiin tai olla organisaation oma päätös. Pysyvä säilytys perustuu arkistolaitoksen päätökseen.'
sailytysajanPerusteTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'sailytysajanPerusteTekstiTyyppi', sailytysajanPerusteTekstiTyyppi)
_module_typeBindings.sailytysajanPerusteTekstiTyyppi = sailytysajanPerusteTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}sailytysajanLaskentaperusteTekstiTyyppi
class sailytysajanLaskentaperusteTekstiTyyppi (pyxb.binding.datatypes.string):

    """Suositeltavat arvot käsittelyprosessille: Asian lopullinen ratkaisu. Suositeltavat arvot asiakirjalle: Asian lopullinen ratkaisu, Asiakirjan päivämäärä."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'sailytysajanLaskentaperusteTekstiTyyppi')
    _XSDLocation = None
    _Documentation = 'Suositeltavat arvot käsittelyprosessille: Asian lopullinen ratkaisu. Suositeltavat arvot asiakirjalle: Asian lopullinen ratkaisu, Asiakirjan päivämäärä.'
sailytysajanLaskentaperusteTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'sailytysajanLaskentaperusteTekstiTyyppi', sailytysajanLaskentaperusteTekstiTyyppi)
_module_typeBindings.sailytysajanLaskentaperusteTekstiTyyppi = sailytysajanLaskentaperusteTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}toimenpideluokkaTekstiTyyppi
class toimenpideluokkaTekstiTyyppi (pyxb.binding.datatypes.string):

    """
	Suositeltavat arvot: ohjaus, vireilletulo , valmistelu, päätöksenteko, toimeenpano, tiedoksianto, muutoksenhaku, seuranta.
	    """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'toimenpideluokkaTekstiTyyppi')
    _XSDLocation = None
    _Documentation = '\n\tSuositeltavat arvot: ohjaus, vireilletulo , valmistelu, päätöksenteko, toimeenpano, tiedoksianto, muutoksenhaku, seuranta.\n\t    '
toimenpideluokkaTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'toimenpideluokkaTekstiTyyppi', toimenpideluokkaTekstiTyyppi)
_module_typeBindings.toimenpideluokkaTekstiTyyppi = toimenpideluokkaTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}toimenpideluokkaTarkenneTekstiTyyppi
class toimenpideluokkaTarkenneTekstiTyyppi (pyxb.binding.datatypes.string):

    """
	Suositeltavat arvot: ohjaus, vireilletulo , valmistelu, päätöksenteko, toimeenpano, tiedoksianto, muutoksenhaku, seuranta.
	        """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'toimenpideluokkaTarkenneTekstiTyyppi')
    _XSDLocation = None
    _Documentation = '\n\tSuositeltavat arvot: ohjaus, vireilletulo , valmistelu, päätöksenteko, toimeenpano, tiedoksianto, muutoksenhaku, seuranta.\n\t        '
toimenpideluokkaTarkenneTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'toimenpideluokkaTarkenneTekstiTyyppi', toimenpideluokkaTarkenneTekstiTyyppi)
_module_typeBindings.toimenpideluokkaTarkenneTekstiTyyppi = toimenpideluokkaTarkenneTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}asiakirjaLuokkaTekstiTyyppi
class asiakirjaLuokkaTekstiTyyppi (pyxb.binding.datatypes.string):

    """
	Suositeltavia arvoja ovat: Aloite, Asetus, Ehdotus, Esitys, Esityslista, Hakemus, Ilmoitus, Julkaisu, Kannanotto, Kantelu, Kartta, Kertomus, Kirje, Kutsu, Kuulutus, Kuva, Laki, Lasku, Lausunto, Lausuntopyyntö, Liite, Luettelo, Lupa, Mietintö, Muistio, Määräys, Nimittämiskirja, Ohje, Ohjelma, Oikaisuvaatimus, Ote, Piirustus, Pyyntö, Päätös, Pöytäkirja, Raportti, Seloste, Selvitys, Sopimus, Strategia, Suositus, Suunnitelma, Talousarvio, Tarjous, Tarjouspyyntö, Teos, Tiedote, Tilasto, Tilaus, Tilinpäätös, Todistus, Tosite, Valitus, Valtakirja, Vastine, Yhteenveto.
	Asiakirjatyypit ilmaistaan aina yksikkömuodossa.
	    """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'asiakirjaLuokkaTekstiTyyppi')
    _XSDLocation = None
    _Documentation = '\n\tSuositeltavia arvoja ovat: Aloite, Asetus, Ehdotus, Esitys, Esityslista, Hakemus, Ilmoitus, Julkaisu, Kannanotto, Kantelu, Kartta, Kertomus, Kirje, Kutsu, Kuulutus, Kuva, Laki, Lasku, Lausunto, Lausuntopyyntö, Liite, Luettelo, Lupa, Mietintö, Muistio, Määräys, Nimittämiskirja, Ohje, Ohjelma, Oikaisuvaatimus, Ote, Piirustus, Pyyntö, Päätös, Pöytäkirja, Raportti, Seloste, Selvitys, Sopimus, Strategia, Suositus, Suunnitelma, Talousarvio, Tarjous, Tarjouspyyntö, Teos, Tiedote, Tilasto, Tilaus, Tilinpäätös, Todistus, Tosite, Valitus, Valtakirja, Vastine, Yhteenveto.\n\tAsiakirjatyypit ilmaistaan aina yksikkömuodossa.\n\t    '
asiakirjaLuokkaTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'asiakirjaLuokkaTekstiTyyppi', asiakirjaLuokkaTekstiTyyppi)
_module_typeBindings.asiakirjaLuokkaTekstiTyyppi = asiakirjaLuokkaTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}kasittelyprosessinTilaTekstiTyyppi
class kasittelyprosessinTilaTekstiTyyppi (pyxb.binding.datatypes.string):

    """
	Suositeltavia arvoja ovat: Avattu, Vireillä, Valmistelussa, Ratkaistavana, Toimitettu tiedoksi, Toimeenpantava, Päätetty, Avattu uudelleen, Muutoksenhaku, Seurannassa, Siirretty, Hävitetty.
			"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'kasittelyprosessinTilaTekstiTyyppi')
    _XSDLocation = None
    _Documentation = '\n\tSuositeltavia arvoja ovat: Avattu, Vireillä, Valmistelussa, Ratkaistavana, Toimitettu tiedoksi, Toimeenpantava, Päätetty, Avattu uudelleen, Muutoksenhaku, Seurannassa, Siirretty, Hävitetty.\n\t\t\t'
kasittelyprosessinTilaTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'kasittelyprosessinTilaTekstiTyyppi', kasittelyprosessinTilaTekstiTyyppi)
_module_typeBindings.kasittelyprosessinTilaTekstiTyyppi = kasittelyprosessinTilaTekstiTyyppi

# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = None
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}TosTiedot uses Python identifier TosTiedot
    __TosTiedot = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TosTiedot'), 'TosTiedot', '__httpskeemat_jhs_suositukset_fitos20150115_CTD_ANON_httpskeemat_jhs_suositukset_fitos20150115TosTiedot', False, None, )

    
    TosTiedot = property(__TosTiedot.value, __TosTiedot.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}Luokka uses Python identifier Luokka
    __Luokka = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Luokka'), 'Luokka', '__httpskeemat_jhs_suositukset_fitos20150115_CTD_ANON_httpskeemat_jhs_suositukset_fitos20150115Luokka', True, None, )

    
    Luokka = property(__Luokka.value, __Luokka.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}Laajennos uses Python identifier Laajennos
    __Laajennos = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Laajennos'), 'Laajennos', '__httpskeemat_jhs_suositukset_fitos20150115_CTD_ANON_httpskeemat_jhs_suositukset_fitos20150115Laajennos', True, None, )

    
    Laajennos = property(__Laajennos.value, __Laajennos.set, None, 'Yleinen laajennoselementti. Laajennoksilla mahdollistetaan organisaatiokohtaiset  elementit.')

    _ElementMap.update({
        __TosTiedot.name() : __TosTiedot,
        __Luokka.name() : __Luokka,
        __Laajennos.name() : __Laajennos
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    """Yleinen laajennoselementti. Laajennoksilla mahdollistetaan organisaatiokohtaiset  elementit."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = None
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _HasWildcardElement = True
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_ = CTD_ANON_


# Complex type {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}nimekeTyyppi with content type ELEMENT_ONLY
class nimekeTyyppi (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}nimekeTyyppi with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'nimekeTyyppi')
    _XSDLocation = None
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}NimekeTeksti uses Python identifier NimekeTeksti
    __NimekeTeksti = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NimekeTeksti'), 'NimekeTeksti', '__httpskeemat_jhs_suositukset_fitos20150115_nimekeTyyppi_httpskeemat_jhs_suositukset_fitos20150115NimekeTeksti', False, None, )

    
    NimekeTeksti = property(__NimekeTeksti.value, __NimekeTeksti.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}NimekeKielella uses Python identifier NimekeKielella
    __NimekeKielella = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NimekeKielella'), 'NimekeKielella', '__httpskeemat_jhs_suositukset_fitos20150115_nimekeTyyppi_httpskeemat_jhs_suositukset_fitos20150115NimekeKielella', True, None, )

    
    NimekeKielella = property(__NimekeKielella.value, __NimekeKielella.set, None, None)

    _ElementMap.update({
        __NimekeTeksti.name() : __NimekeTeksti,
        __NimekeKielella.name() : __NimekeKielella
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.nimekeTyyppi = nimekeTyyppi
Namespace.addCategoryObject('typeBinding', 'nimekeTyyppi', nimekeTyyppi)


# Complex type {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}asiasanatTyyppi with content type ELEMENT_ONLY
class asiasanatTyyppi (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}asiasanatTyyppi with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'asiasanatTyyppi')
    _XSDLocation = None
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}AsiasanastoTeksti uses Python identifier AsiasanastoTeksti
    __AsiasanastoTeksti = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AsiasanastoTeksti'), 'AsiasanastoTeksti', '__httpskeemat_jhs_suositukset_fitos20150115_asiasanatTyyppi_httpskeemat_jhs_suositukset_fitos20150115AsiasanastoTeksti', True, None, )

    
    AsiasanastoTeksti = property(__AsiasanastoTeksti.value, __AsiasanastoTeksti.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}AsiasanaTeksti uses Python identifier AsiasanaTeksti
    __AsiasanaTeksti = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AsiasanaTeksti'), 'AsiasanaTeksti', '__httpskeemat_jhs_suositukset_fitos20150115_asiasanatTyyppi_httpskeemat_jhs_suositukset_fitos20150115AsiasanaTeksti', True, None, )

    
    AsiasanaTeksti = property(__AsiasanaTeksti.value, __AsiasanaTeksti.set, None, None)

    _ElementMap.update({
        __AsiasanastoTeksti.name() : __AsiasanastoTeksti,
        __AsiasanaTeksti.name() : __AsiasanaTeksti
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.asiasanatTyyppi = asiasanatTyyppi
Namespace.addCategoryObject('typeBinding', 'asiasanatTyyppi', asiasanatTyyppi)


# Complex type {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}kasittelysaannotTyyppi with content type ELEMENT_ONLY
class kasittelysaannotTyyppi (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}kasittelysaannotTyyppi with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'kasittelysaannotTyyppi')
    _XSDLocation = None
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}JulkisuusluokkaMuutosTeksti uses Python identifier JulkisuusluokkaMuutosTeksti
    __JulkisuusluokkaMuutosTeksti = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'JulkisuusluokkaMuutosTeksti'), 'JulkisuusluokkaMuutosTeksti', '__httpskeemat_jhs_suositukset_fitos20150115_kasittelysaannotTyyppi_httpskeemat_jhs_suositukset_fitos20150115JulkisuusluokkaMuutosTeksti', False, None, )

    
    JulkisuusluokkaMuutosTeksti = property(__JulkisuusluokkaMuutosTeksti.value, __JulkisuusluokkaMuutosTeksti.set, None, 'Esimerkiksi: Asian päättäminen, Päätöksenteko (toimenpide), Päätöksen allekirjoitus (toimenpide).')

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}AiempienVersioidenPoistoTeksti uses Python identifier AiempienVersioidenPoistoTeksti
    __AiempienVersioidenPoistoTeksti = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AiempienVersioidenPoistoTeksti'), 'AiempienVersioidenPoistoTeksti', '__httpskeemat_jhs_suositukset_fitos20150115_kasittelysaannotTyyppi_httpskeemat_jhs_suositukset_fitos20150115AiempienVersioidenPoistoTeksti', False, None, )

    
    AiempienVersioidenPoistoTeksti = property(__AiempienVersioidenPoistoTeksti.value, __AiempienVersioidenPoistoTeksti.set, None, 'Suositeltavat: Asian ratkaisu, Tietty aika asian ratkaisusta, Asiakirjan hävittäminen.')

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}TallennuspaikkaTeksti uses Python identifier TallennuspaikkaTeksti
    __TallennuspaikkaTeksti = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TallennuspaikkaTeksti'), 'TallennuspaikkaTeksti', '__httpskeemat_jhs_suositukset_fitos20150115_kasittelysaannotTyyppi_httpskeemat_jhs_suositukset_fitos20150115TallennuspaikkaTeksti', False, None, )

    
    TallennuspaikkaTeksti = property(__TallennuspaikkaTeksti.value, __TallennuspaikkaTeksti.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}SailytyspaikkaTeksti uses Python identifier SailytyspaikkaTeksti
    __SailytyspaikkaTeksti = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SailytyspaikkaTeksti'), 'SailytyspaikkaTeksti', '__httpskeemat_jhs_suositukset_fitos20150115_kasittelysaannotTyyppi_httpskeemat_jhs_suositukset_fitos20150115SailytyspaikkaTeksti', False, None, )

    
    SailytyspaikkaTeksti = property(__SailytyspaikkaTeksti.value, __SailytyspaikkaTeksti.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}Laajennos uses Python identifier Laajennos
    __Laajennos = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Laajennos'), 'Laajennos', '__httpskeemat_jhs_suositukset_fitos20150115_kasittelysaannotTyyppi_httpskeemat_jhs_suositukset_fitos20150115Laajennos', True, None, )

    
    Laajennos = property(__Laajennos.value, __Laajennos.set, None, 'Yleinen laajennoselementti. Laajennoksilla mahdollistetaan organisaatiokohtaiset  elementit.')

    _ElementMap.update({
        __JulkisuusluokkaMuutosTeksti.name() : __JulkisuusluokkaMuutosTeksti,
        __AiempienVersioidenPoistoTeksti.name() : __AiempienVersioidenPoistoTeksti,
        __TallennuspaikkaTeksti.name() : __TallennuspaikkaTeksti,
        __SailytyspaikkaTeksti.name() : __SailytyspaikkaTeksti,
        __Laajennos.name() : __Laajennos
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.kasittelysaannotTyyppi = kasittelysaannotTyyppi
Namespace.addCategoryObject('typeBinding', 'kasittelysaannotTyyppi', kasittelysaannotTyyppi)


# Complex type {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}kayttorajoitusTiedotTyyppi with content type ELEMENT_ONLY
class kayttorajoitusTiedotTyyppi (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}kayttorajoitusTiedotTyyppi with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'kayttorajoitusTiedotTyyppi')
    _XSDLocation = None
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}JulkisuusluokkaKoodi uses Python identifier JulkisuusluokkaKoodi
    __JulkisuusluokkaKoodi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'JulkisuusluokkaKoodi'), 'JulkisuusluokkaKoodi', '__httpskeemat_jhs_suositukset_fitos20150115_kayttorajoitusTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115JulkisuusluokkaKoodi', False, None, )

    
    JulkisuusluokkaKoodi = property(__JulkisuusluokkaKoodi.value, __JulkisuusluokkaKoodi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}SalassapitoAikaArvo uses Python identifier SalassapitoAikaArvo
    __SalassapitoAikaArvo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SalassapitoAikaArvo'), 'SalassapitoAikaArvo', '__httpskeemat_jhs_suositukset_fitos20150115_kayttorajoitusTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115SalassapitoAikaArvo', False, None, )

    
    SalassapitoAikaArvo = property(__SalassapitoAikaArvo.value, __SalassapitoAikaArvo.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}SalassapitoPerusteTeksti uses Python identifier SalassapitoPerusteTeksti
    __SalassapitoPerusteTeksti = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SalassapitoPerusteTeksti'), 'SalassapitoPerusteTeksti', '__httpskeemat_jhs_suositukset_fitos20150115_kayttorajoitusTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115SalassapitoPerusteTeksti', False, None, )

    
    SalassapitoPerusteTeksti = property(__SalassapitoPerusteTeksti.value, __SalassapitoPerusteTeksti.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}SalassapidonLaskentaperusteTeksti uses Python identifier SalassapidonLaskentaperusteTeksti
    __SalassapidonLaskentaperusteTeksti = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SalassapidonLaskentaperusteTeksti'), 'SalassapidonLaskentaperusteTeksti', '__httpskeemat_jhs_suositukset_fitos20150115_kayttorajoitusTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115SalassapidonLaskentaperusteTeksti', False, None, )

    
    SalassapidonLaskentaperusteTeksti = property(__SalassapidonLaskentaperusteTeksti.value, __SalassapidonLaskentaperusteTeksti.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}SuojaustasoKoodi uses Python identifier SuojaustasoKoodi
    __SuojaustasoKoodi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SuojaustasoKoodi'), 'SuojaustasoKoodi', '__httpskeemat_jhs_suositukset_fitos20150115_kayttorajoitusTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115SuojaustasoKoodi', False, None, )

    
    SuojaustasoKoodi = property(__SuojaustasoKoodi.value, __SuojaustasoKoodi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}TurvallisuusluokkaKoodi uses Python identifier TurvallisuusluokkaKoodi
    __TurvallisuusluokkaKoodi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TurvallisuusluokkaKoodi'), 'TurvallisuusluokkaKoodi', '__httpskeemat_jhs_suositukset_fitos20150115_kayttorajoitusTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115TurvallisuusluokkaKoodi', False, None, )

    
    TurvallisuusluokkaKoodi = property(__TurvallisuusluokkaKoodi.value, __TurvallisuusluokkaKoodi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}HenkilotietoluonneKoodi uses Python identifier HenkilotietoluonneKoodi
    __HenkilotietoluonneKoodi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'HenkilotietoluonneKoodi'), 'HenkilotietoluonneKoodi', '__httpskeemat_jhs_suositukset_fitos20150115_kayttorajoitusTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115HenkilotietoluonneKoodi', False, None, )

    
    HenkilotietoluonneKoodi = property(__HenkilotietoluonneKoodi.value, __HenkilotietoluonneKoodi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}Laajennos uses Python identifier Laajennos
    __Laajennos = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Laajennos'), 'Laajennos', '__httpskeemat_jhs_suositukset_fitos20150115_kayttorajoitusTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115Laajennos', True, None, )

    
    Laajennos = property(__Laajennos.value, __Laajennos.set, None, 'Yleinen laajennoselementti. Laajennoksilla mahdollistetaan organisaatiokohtaiset  elementit.')

    _ElementMap.update({
        __JulkisuusluokkaKoodi.name() : __JulkisuusluokkaKoodi,
        __SalassapitoAikaArvo.name() : __SalassapitoAikaArvo,
        __SalassapitoPerusteTeksti.name() : __SalassapitoPerusteTeksti,
        __SalassapidonLaskentaperusteTeksti.name() : __SalassapidonLaskentaperusteTeksti,
        __SuojaustasoKoodi.name() : __SuojaustasoKoodi,
        __TurvallisuusluokkaKoodi.name() : __TurvallisuusluokkaKoodi,
        __HenkilotietoluonneKoodi.name() : __HenkilotietoluonneKoodi,
        __Laajennos.name() : __Laajennos
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.kayttorajoitusTiedotTyyppi = kayttorajoitusTiedotTyyppi
Namespace.addCategoryObject('typeBinding', 'kayttorajoitusTiedotTyyppi', kayttorajoitusTiedotTyyppi)


# Complex type {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}sailytysaikaTiedotTyyppi with content type ELEMENT_ONLY
class sailytysaikaTiedotTyyppi (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}sailytysaikaTiedotTyyppi with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'sailytysaikaTiedotTyyppi')
    _XSDLocation = None
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}SailytysajanPituusArvo uses Python identifier SailytysajanPituusArvo
    __SailytysajanPituusArvo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SailytysajanPituusArvo'), 'SailytysajanPituusArvo', '__httpskeemat_jhs_suositukset_fitos20150115_sailytysaikaTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115SailytysajanPituusArvo', False, None, )

    
    SailytysajanPituusArvo = property(__SailytysajanPituusArvo.value, __SailytysajanPituusArvo.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}SailytysajanPerusteTeksti uses Python identifier SailytysajanPerusteTeksti
    __SailytysajanPerusteTeksti = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SailytysajanPerusteTeksti'), 'SailytysajanPerusteTeksti', '__httpskeemat_jhs_suositukset_fitos20150115_sailytysaikaTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115SailytysajanPerusteTeksti', False, None, )

    
    SailytysajanPerusteTeksti = property(__SailytysajanPerusteTeksti.value, __SailytysajanPerusteTeksti.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}SailytysajanLaskentaperusteTeksti uses Python identifier SailytysajanLaskentaperusteTeksti
    __SailytysajanLaskentaperusteTeksti = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'SailytysajanLaskentaperusteTeksti'), 'SailytysajanLaskentaperusteTeksti', '__httpskeemat_jhs_suositukset_fitos20150115_sailytysaikaTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115SailytysajanLaskentaperusteTeksti', False, None, )

    
    SailytysajanLaskentaperusteTeksti = property(__SailytysajanLaskentaperusteTeksti.value, __SailytysajanLaskentaperusteTeksti.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}Laajennos uses Python identifier Laajennos
    __Laajennos = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Laajennos'), 'Laajennos', '__httpskeemat_jhs_suositukset_fitos20150115_sailytysaikaTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115Laajennos', True, None, )

    
    Laajennos = property(__Laajennos.value, __Laajennos.set, None, 'Yleinen laajennoselementti. Laajennoksilla mahdollistetaan organisaatiokohtaiset  elementit.')

    _ElementMap.update({
        __SailytysajanPituusArvo.name() : __SailytysajanPituusArvo,
        __SailytysajanPerusteTeksti.name() : __SailytysajanPerusteTeksti,
        __SailytysajanLaskentaperusteTeksti.name() : __SailytysajanLaskentaperusteTeksti,
        __Laajennos.name() : __Laajennos
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.sailytysaikaTiedotTyyppi = sailytysaikaTiedotTyyppi
Namespace.addCategoryObject('typeBinding', 'sailytysaikaTiedotTyyppi', sailytysaikaTiedotTyyppi)


# Complex type {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}TosTiedotTyyppi with content type ELEMENT_ONLY
class TosTiedotTyyppi (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}TosTiedotTyyppi with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TosTiedotTyyppi')
    _XSDLocation = None
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}TilaKoodi uses Python identifier TilaKoodi
    __TilaKoodi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TilaKoodi'), 'TilaKoodi', '__httpskeemat_jhs_suositukset_fitos20150115_TosTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115TilaKoodi', False, None, )

    
    TilaKoodi = property(__TilaKoodi.value, __TilaKoodi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}TosVersio uses Python identifier TosVersio
    __TosVersio = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TosVersio'), 'TosVersio', '__httpskeemat_jhs_suositukset_fitos20150115_TosTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115TosVersio', False, None, )

    
    TosVersio = property(__TosVersio.value, __TosVersio.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}LisatiedotTeksti uses Python identifier LisatiedotTeksti
    __LisatiedotTeksti = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LisatiedotTeksti'), 'LisatiedotTeksti', '__httpskeemat_jhs_suositukset_fitos20150115_TosTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115LisatiedotTeksti', False, None, )

    
    LisatiedotTeksti = property(__LisatiedotTeksti.value, __LisatiedotTeksti.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}OrganisaatioNimi uses Python identifier OrganisaatioNimi
    __OrganisaatioNimi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OrganisaatioNimi'), 'OrganisaatioNimi', '__httpskeemat_jhs_suositukset_fitos20150115_TosTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115OrganisaatioNimi', False, None, )

    
    OrganisaatioNimi = property(__OrganisaatioNimi.value, __OrganisaatioNimi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}LaatijaNimi uses Python identifier LaatijaNimi
    __LaatijaNimi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LaatijaNimi'), 'LaatijaNimi', '__httpskeemat_jhs_suositukset_fitos20150115_TosTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115LaatijaNimi', False, None, )

    
    LaatijaNimi = property(__LaatijaNimi.value, __LaatijaNimi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}LaadittuPvm uses Python identifier LaadittuPvm
    __LaadittuPvm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LaadittuPvm'), 'LaadittuPvm', '__httpskeemat_jhs_suositukset_fitos20150115_TosTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115LaadittuPvm', False, None, )

    
    LaadittuPvm = property(__LaadittuPvm.value, __LaadittuPvm.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}MuokkaajaNimi uses Python identifier MuokkaajaNimi
    __MuokkaajaNimi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'MuokkaajaNimi'), 'MuokkaajaNimi', '__httpskeemat_jhs_suositukset_fitos20150115_TosTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115MuokkaajaNimi', False, None, )

    
    MuokkaajaNimi = property(__MuokkaajaNimi.value, __MuokkaajaNimi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}MuokattuPvm uses Python identifier MuokattuPvm
    __MuokattuPvm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'MuokattuPvm'), 'MuokattuPvm', '__httpskeemat_jhs_suositukset_fitos20150115_TosTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115MuokattuPvm', False, None, )

    
    MuokattuPvm = property(__MuokattuPvm.value, __MuokattuPvm.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}HyvaksyjaNimi uses Python identifier HyvaksyjaNimi
    __HyvaksyjaNimi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyjaNimi'), 'HyvaksyjaNimi', '__httpskeemat_jhs_suositukset_fitos20150115_TosTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115HyvaksyjaNimi', False, None, )

    
    HyvaksyjaNimi = property(__HyvaksyjaNimi.value, __HyvaksyjaNimi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}HyvaksyttyPvm uses Python identifier HyvaksyttyPvm
    __HyvaksyttyPvm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyttyPvm'), 'HyvaksyttyPvm', '__httpskeemat_jhs_suositukset_fitos20150115_TosTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115HyvaksyttyPvm', False, None, )

    
    HyvaksyttyPvm = property(__HyvaksyttyPvm.value, __HyvaksyttyPvm.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}VoimassaoloAlkaaPvm uses Python identifier VoimassaoloAlkaaPvm
    __VoimassaoloAlkaaPvm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloAlkaaPvm'), 'VoimassaoloAlkaaPvm', '__httpskeemat_jhs_suositukset_fitos20150115_TosTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115VoimassaoloAlkaaPvm', False, None, )

    
    VoimassaoloAlkaaPvm = property(__VoimassaoloAlkaaPvm.value, __VoimassaoloAlkaaPvm.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}VoimassaoloPaattyyPvm uses Python identifier VoimassaoloPaattyyPvm
    __VoimassaoloPaattyyPvm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloPaattyyPvm'), 'VoimassaoloPaattyyPvm', '__httpskeemat_jhs_suositukset_fitos20150115_TosTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115VoimassaoloPaattyyPvm', False, None, )

    
    VoimassaoloPaattyyPvm = property(__VoimassaoloPaattyyPvm.value, __VoimassaoloPaattyyPvm.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}YhteyshenkiloNimi uses Python identifier YhteyshenkiloNimi
    __YhteyshenkiloNimi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'YhteyshenkiloNimi'), 'YhteyshenkiloNimi', '__httpskeemat_jhs_suositukset_fitos20150115_TosTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115YhteyshenkiloNimi', False, None, )

    
    YhteyshenkiloNimi = property(__YhteyshenkiloNimi.value, __YhteyshenkiloNimi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}Laajennos uses Python identifier Laajennos
    __Laajennos = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Laajennos'), 'Laajennos', '__httpskeemat_jhs_suositukset_fitos20150115_TosTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115Laajennos', True, None, )

    
    Laajennos = property(__Laajennos.value, __Laajennos.set, None, 'Yleinen laajennoselementti. Laajennoksilla mahdollistetaan organisaatiokohtaiset  elementit.')

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}Nimeke uses Python identifier Nimeke
    __Nimeke = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Nimeke'), 'Nimeke', '__httpskeemat_jhs_suositukset_fitos20150115_TosTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115Nimeke', False, None, )

    
    Nimeke = property(__Nimeke.value, __Nimeke.set, None, None)

    
    # Attribute {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, 'id'), 'id', '__httpskeemat_jhs_suositukset_fitos20150115_TosTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115id', _module_typeBindings.idTyyppi, required=True)
    __id._DeclarationLocation = None
    __id._UseLocation = None
    
    id = property(__id.value, __id.set, None, None)

    _ElementMap.update({
        __TilaKoodi.name() : __TilaKoodi,
        __TosVersio.name() : __TosVersio,
        __LisatiedotTeksti.name() : __LisatiedotTeksti,
        __OrganisaatioNimi.name() : __OrganisaatioNimi,
        __LaatijaNimi.name() : __LaatijaNimi,
        __LaadittuPvm.name() : __LaadittuPvm,
        __MuokkaajaNimi.name() : __MuokkaajaNimi,
        __MuokattuPvm.name() : __MuokattuPvm,
        __HyvaksyjaNimi.name() : __HyvaksyjaNimi,
        __HyvaksyttyPvm.name() : __HyvaksyttyPvm,
        __VoimassaoloAlkaaPvm.name() : __VoimassaoloAlkaaPvm,
        __VoimassaoloPaattyyPvm.name() : __VoimassaoloPaattyyPvm,
        __YhteyshenkiloNimi.name() : __YhteyshenkiloNimi,
        __Laajennos.name() : __Laajennos,
        __Nimeke.name() : __Nimeke
    })
    _AttributeMap.update({
        __id.name() : __id
    })
_module_typeBindings.TosTiedotTyyppi = TosTiedotTyyppi
Namespace.addCategoryObject('typeBinding', 'TosTiedotTyyppi', TosTiedotTyyppi)


# Complex type {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}luokkaTyyppi with content type ELEMENT_ONLY
class luokkaTyyppi (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}luokkaTyyppi with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'luokkaTyyppi')
    _XSDLocation = None
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}TilaKoodi uses Python identifier TilaKoodi
    __TilaKoodi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TilaKoodi'), 'TilaKoodi', '__httpskeemat_jhs_suositukset_fitos20150115_luokkaTyyppi_httpskeemat_jhs_suositukset_fitos20150115TilaKoodi', False, None, )

    
    TilaKoodi = property(__TilaKoodi.value, __TilaKoodi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}OsaVersio uses Python identifier OsaVersio
    __OsaVersio = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OsaVersio'), 'OsaVersio', '__httpskeemat_jhs_suositukset_fitos20150115_luokkaTyyppi_httpskeemat_jhs_suositukset_fitos20150115OsaVersio', False, None, )

    
    OsaVersio = property(__OsaVersio.value, __OsaVersio.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}Luokitustunnus uses Python identifier Luokitustunnus
    __Luokitustunnus = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Luokitustunnus'), 'Luokitustunnus', '__httpskeemat_jhs_suositukset_fitos20150115_luokkaTyyppi_httpskeemat_jhs_suositukset_fitos20150115Luokitustunnus', False, None, )

    
    Luokitustunnus = property(__Luokitustunnus.value, __Luokitustunnus.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}LuokitusKuvausTeksti uses Python identifier LuokitusKuvausTeksti
    __LuokitusKuvausTeksti = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LuokitusKuvausTeksti'), 'LuokitusKuvausTeksti', '__httpskeemat_jhs_suositukset_fitos20150115_luokkaTyyppi_httpskeemat_jhs_suositukset_fitos20150115LuokitusKuvausTeksti', False, None, )

    
    LuokitusKuvausTeksti = property(__LuokitusKuvausTeksti.value, __LuokitusKuvausTeksti.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}OrganisaatioNimi uses Python identifier OrganisaatioNimi
    __OrganisaatioNimi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OrganisaatioNimi'), 'OrganisaatioNimi', '__httpskeemat_jhs_suositukset_fitos20150115_luokkaTyyppi_httpskeemat_jhs_suositukset_fitos20150115OrganisaatioNimi', False, None, )

    
    OrganisaatioNimi = property(__OrganisaatioNimi.value, __OrganisaatioNimi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}LaatijaNimi uses Python identifier LaatijaNimi
    __LaatijaNimi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LaatijaNimi'), 'LaatijaNimi', '__httpskeemat_jhs_suositukset_fitos20150115_luokkaTyyppi_httpskeemat_jhs_suositukset_fitos20150115LaatijaNimi', False, None, )

    
    LaatijaNimi = property(__LaatijaNimi.value, __LaatijaNimi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}LaadittuPvm uses Python identifier LaadittuPvm
    __LaadittuPvm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LaadittuPvm'), 'LaadittuPvm', '__httpskeemat_jhs_suositukset_fitos20150115_luokkaTyyppi_httpskeemat_jhs_suositukset_fitos20150115LaadittuPvm', False, None, )

    
    LaadittuPvm = property(__LaadittuPvm.value, __LaadittuPvm.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}MuokkaajaNimi uses Python identifier MuokkaajaNimi
    __MuokkaajaNimi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'MuokkaajaNimi'), 'MuokkaajaNimi', '__httpskeemat_jhs_suositukset_fitos20150115_luokkaTyyppi_httpskeemat_jhs_suositukset_fitos20150115MuokkaajaNimi', False, None, )

    
    MuokkaajaNimi = property(__MuokkaajaNimi.value, __MuokkaajaNimi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}MuokattuPvm uses Python identifier MuokattuPvm
    __MuokattuPvm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'MuokattuPvm'), 'MuokattuPvm', '__httpskeemat_jhs_suositukset_fitos20150115_luokkaTyyppi_httpskeemat_jhs_suositukset_fitos20150115MuokattuPvm', False, None, )

    
    MuokattuPvm = property(__MuokattuPvm.value, __MuokattuPvm.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}HyvaksyjaNimi uses Python identifier HyvaksyjaNimi
    __HyvaksyjaNimi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyjaNimi'), 'HyvaksyjaNimi', '__httpskeemat_jhs_suositukset_fitos20150115_luokkaTyyppi_httpskeemat_jhs_suositukset_fitos20150115HyvaksyjaNimi', False, None, )

    
    HyvaksyjaNimi = property(__HyvaksyjaNimi.value, __HyvaksyjaNimi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}HyvaksyttyPvm uses Python identifier HyvaksyttyPvm
    __HyvaksyttyPvm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyttyPvm'), 'HyvaksyttyPvm', '__httpskeemat_jhs_suositukset_fitos20150115_luokkaTyyppi_httpskeemat_jhs_suositukset_fitos20150115HyvaksyttyPvm', False, None, )

    
    HyvaksyttyPvm = property(__HyvaksyttyPvm.value, __HyvaksyttyPvm.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}VoimassaoloAlkaaPvm uses Python identifier VoimassaoloAlkaaPvm
    __VoimassaoloAlkaaPvm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloAlkaaPvm'), 'VoimassaoloAlkaaPvm', '__httpskeemat_jhs_suositukset_fitos20150115_luokkaTyyppi_httpskeemat_jhs_suositukset_fitos20150115VoimassaoloAlkaaPvm', False, None, )

    
    VoimassaoloAlkaaPvm = property(__VoimassaoloAlkaaPvm.value, __VoimassaoloAlkaaPvm.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}VoimassaoloPaattyyPvm uses Python identifier VoimassaoloPaattyyPvm
    __VoimassaoloPaattyyPvm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloPaattyyPvm'), 'VoimassaoloPaattyyPvm', '__httpskeemat_jhs_suositukset_fitos20150115_luokkaTyyppi_httpskeemat_jhs_suositukset_fitos20150115VoimassaoloPaattyyPvm', False, None, )

    
    VoimassaoloPaattyyPvm = property(__VoimassaoloPaattyyPvm.value, __VoimassaoloPaattyyPvm.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}Laajennos uses Python identifier Laajennos
    __Laajennos = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Laajennos'), 'Laajennos', '__httpskeemat_jhs_suositukset_fitos20150115_luokkaTyyppi_httpskeemat_jhs_suositukset_fitos20150115Laajennos', True, None, )

    
    Laajennos = property(__Laajennos.value, __Laajennos.set, None, 'Yleinen laajennoselementti. Laajennoksilla mahdollistetaan organisaatiokohtaiset  elementit.')

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}Nimeke uses Python identifier Nimeke
    __Nimeke = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Nimeke'), 'Nimeke', '__httpskeemat_jhs_suositukset_fitos20150115_luokkaTyyppi_httpskeemat_jhs_suositukset_fitos20150115Nimeke', False, None, )

    
    Nimeke = property(__Nimeke.value, __Nimeke.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}KasittelyprosessiTiedot uses Python identifier KasittelyprosessiTiedot
    __KasittelyprosessiTiedot = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'KasittelyprosessiTiedot'), 'KasittelyprosessiTiedot', '__httpskeemat_jhs_suositukset_fitos20150115_luokkaTyyppi_httpskeemat_jhs_suositukset_fitos20150115KasittelyprosessiTiedot', False, None, )

    
    KasittelyprosessiTiedot = property(__KasittelyprosessiTiedot.value, __KasittelyprosessiTiedot.set, None, None)

    
    # Attribute {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, 'id'), 'id', '__httpskeemat_jhs_suositukset_fitos20150115_luokkaTyyppi_httpskeemat_jhs_suositukset_fitos20150115id', _module_typeBindings.idTyyppi, required=True)
    __id._DeclarationLocation = None
    __id._UseLocation = None
    
    id = property(__id.value, __id.set, None, None)

    _ElementMap.update({
        __TilaKoodi.name() : __TilaKoodi,
        __OsaVersio.name() : __OsaVersio,
        __Luokitustunnus.name() : __Luokitustunnus,
        __LuokitusKuvausTeksti.name() : __LuokitusKuvausTeksti,
        __OrganisaatioNimi.name() : __OrganisaatioNimi,
        __LaatijaNimi.name() : __LaatijaNimi,
        __LaadittuPvm.name() : __LaadittuPvm,
        __MuokkaajaNimi.name() : __MuokkaajaNimi,
        __MuokattuPvm.name() : __MuokattuPvm,
        __HyvaksyjaNimi.name() : __HyvaksyjaNimi,
        __HyvaksyttyPvm.name() : __HyvaksyttyPvm,
        __VoimassaoloAlkaaPvm.name() : __VoimassaoloAlkaaPvm,
        __VoimassaoloPaattyyPvm.name() : __VoimassaoloPaattyyPvm,
        __Laajennos.name() : __Laajennos,
        __Nimeke.name() : __Nimeke,
        __KasittelyprosessiTiedot.name() : __KasittelyprosessiTiedot
    })
    _AttributeMap.update({
        __id.name() : __id
    })
_module_typeBindings.luokkaTyyppi = luokkaTyyppi
Namespace.addCategoryObject('typeBinding', 'luokkaTyyppi', luokkaTyyppi)


# Complex type {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}nimekeKielellaTyyppi with content type ELEMENT_ONLY
class nimekeKielellaTyyppi (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}nimekeKielellaTyyppi with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'nimekeKielellaTyyppi')
    _XSDLocation = None
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}NimekeTeksti uses Python identifier NimekeTeksti
    __NimekeTeksti = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'NimekeTeksti'), 'NimekeTeksti', '__httpskeemat_jhs_suositukset_fitos20150115_nimekeKielellaTyyppi_httpskeemat_jhs_suositukset_fitos20150115NimekeTeksti', False, None, )

    
    NimekeTeksti = property(__NimekeTeksti.value, __NimekeTeksti.set, None, None)

    
    # Attribute {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}kieliKoodi uses Python identifier kieliKoodi
    __kieliKoodi = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, 'kieliKoodi'), 'kieliKoodi', '__httpskeemat_jhs_suositukset_fitos20150115_nimekeKielellaTyyppi_httpskeemat_jhs_suositukset_fitos20150115kieliKoodi', _module_typeBindings.kieliKoodiTyyppi, required=True)
    __kieliKoodi._DeclarationLocation = None
    __kieliKoodi._UseLocation = None
    
    kieliKoodi = property(__kieliKoodi.value, __kieliKoodi.set, None, None)

    _ElementMap.update({
        __NimekeTeksti.name() : __NimekeTeksti
    })
    _AttributeMap.update({
        __kieliKoodi.name() : __kieliKoodi
    })
_module_typeBindings.nimekeKielellaTyyppi = nimekeKielellaTyyppi
Namespace.addCategoryObject('typeBinding', 'nimekeKielellaTyyppi', nimekeKielellaTyyppi)


# Complex type {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}kasittelyprosessiTiedotTyyppi with content type ELEMENT_ONLY
class kasittelyprosessiTiedotTyyppi (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}kasittelyprosessiTiedotTyyppi with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'kasittelyprosessiTiedotTyyppi')
    _XSDLocation = None
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}OrganisaatioNimi uses Python identifier OrganisaatioNimi
    __OrganisaatioNimi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OrganisaatioNimi'), 'OrganisaatioNimi', '__httpskeemat_jhs_suositukset_fitos20150115_kasittelyprosessiTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115OrganisaatioNimi', False, None, )

    
    OrganisaatioNimi = property(__OrganisaatioNimi.value, __OrganisaatioNimi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}TietojarjestelmaNimi uses Python identifier TietojarjestelmaNimi
    __TietojarjestelmaNimi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TietojarjestelmaNimi'), 'TietojarjestelmaNimi', '__httpskeemat_jhs_suositukset_fitos20150115_kasittelyprosessiTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115TietojarjestelmaNimi', False, None, )

    
    TietojarjestelmaNimi = property(__TietojarjestelmaNimi.value, __TietojarjestelmaNimi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}LaatijaNimi uses Python identifier LaatijaNimi
    __LaatijaNimi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LaatijaNimi'), 'LaatijaNimi', '__httpskeemat_jhs_suositukset_fitos20150115_kasittelyprosessiTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115LaatijaNimi', False, None, )

    
    LaatijaNimi = property(__LaatijaNimi.value, __LaatijaNimi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}LaadittuPvm uses Python identifier LaadittuPvm
    __LaadittuPvm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LaadittuPvm'), 'LaadittuPvm', '__httpskeemat_jhs_suositukset_fitos20150115_kasittelyprosessiTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115LaadittuPvm', False, None, )

    
    LaadittuPvm = property(__LaadittuPvm.value, __LaadittuPvm.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}MuokkaajaNimi uses Python identifier MuokkaajaNimi
    __MuokkaajaNimi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'MuokkaajaNimi'), 'MuokkaajaNimi', '__httpskeemat_jhs_suositukset_fitos20150115_kasittelyprosessiTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115MuokkaajaNimi', False, None, )

    
    MuokkaajaNimi = property(__MuokkaajaNimi.value, __MuokkaajaNimi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}MuokattuPvm uses Python identifier MuokattuPvm
    __MuokattuPvm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'MuokattuPvm'), 'MuokattuPvm', '__httpskeemat_jhs_suositukset_fitos20150115_kasittelyprosessiTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115MuokattuPvm', False, None, )

    
    MuokattuPvm = property(__MuokattuPvm.value, __MuokattuPvm.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}HyvaksyjaNimi uses Python identifier HyvaksyjaNimi
    __HyvaksyjaNimi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyjaNimi'), 'HyvaksyjaNimi', '__httpskeemat_jhs_suositukset_fitos20150115_kasittelyprosessiTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115HyvaksyjaNimi', False, None, )

    
    HyvaksyjaNimi = property(__HyvaksyjaNimi.value, __HyvaksyjaNimi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}HyvaksyttyPvm uses Python identifier HyvaksyttyPvm
    __HyvaksyttyPvm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyttyPvm'), 'HyvaksyttyPvm', '__httpskeemat_jhs_suositukset_fitos20150115_kasittelyprosessiTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115HyvaksyttyPvm', False, None, )

    
    HyvaksyttyPvm = property(__HyvaksyttyPvm.value, __HyvaksyttyPvm.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}VoimassaoloAlkaaPvm uses Python identifier VoimassaoloAlkaaPvm
    __VoimassaoloAlkaaPvm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloAlkaaPvm'), 'VoimassaoloAlkaaPvm', '__httpskeemat_jhs_suositukset_fitos20150115_kasittelyprosessiTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115VoimassaoloAlkaaPvm', False, None, )

    
    VoimassaoloAlkaaPvm = property(__VoimassaoloAlkaaPvm.value, __VoimassaoloAlkaaPvm.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}VoimassaoloPaattyyPvm uses Python identifier VoimassaoloPaattyyPvm
    __VoimassaoloPaattyyPvm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloPaattyyPvm'), 'VoimassaoloPaattyyPvm', '__httpskeemat_jhs_suositukset_fitos20150115_kasittelyprosessiTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115VoimassaoloPaattyyPvm', False, None, )

    
    VoimassaoloPaattyyPvm = property(__VoimassaoloPaattyyPvm.value, __VoimassaoloPaattyyPvm.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}PaatietoryhmatTeksti uses Python identifier PaatietoryhmatTeksti
    __PaatietoryhmatTeksti = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PaatietoryhmatTeksti'), 'PaatietoryhmatTeksti', '__httpskeemat_jhs_suositukset_fitos20150115_kasittelyprosessiTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115PaatietoryhmatTeksti', False, None, )

    
    PaatietoryhmatTeksti = property(__PaatietoryhmatTeksti.value, __PaatietoryhmatTeksti.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}ProsessinOmistajaNimi uses Python identifier ProsessinOmistajaNimi
    __ProsessinOmistajaNimi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ProsessinOmistajaNimi'), 'ProsessinOmistajaNimi', '__httpskeemat_jhs_suositukset_fitos20150115_kasittelyprosessiTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115ProsessinOmistajaNimi', False, None, )

    
    ProsessinOmistajaNimi = property(__ProsessinOmistajaNimi.value, __ProsessinOmistajaNimi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}KokoavanProsessitunnuksenLahdeTeksti uses Python identifier KokoavanProsessitunnuksenLahdeTeksti
    __KokoavanProsessitunnuksenLahdeTeksti = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'KokoavanProsessitunnuksenLahdeTeksti'), 'KokoavanProsessitunnuksenLahdeTeksti', '__httpskeemat_jhs_suositukset_fitos20150115_kasittelyprosessiTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115KokoavanProsessitunnuksenLahdeTeksti', False, None, )

    
    KokoavanProsessitunnuksenLahdeTeksti = property(__KokoavanProsessitunnuksenLahdeTeksti.value, __KokoavanProsessitunnuksenLahdeTeksti.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}Laajennos uses Python identifier Laajennos
    __Laajennos = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Laajennos'), 'Laajennos', '__httpskeemat_jhs_suositukset_fitos20150115_kasittelyprosessiTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115Laajennos', True, None, )

    
    Laajennos = property(__Laajennos.value, __Laajennos.set, None, 'Yleinen laajennoselementti. Laajennoksilla mahdollistetaan organisaatiokohtaiset  elementit.')

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}Asiasanat uses Python identifier Asiasanat
    __Asiasanat = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Asiasanat'), 'Asiasanat', '__httpskeemat_jhs_suositukset_fitos20150115_kasittelyprosessiTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115Asiasanat', True, None, )

    
    Asiasanat = property(__Asiasanat.value, __Asiasanat.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}Toimenpidetiedot uses Python identifier Toimenpidetiedot
    __Toimenpidetiedot = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Toimenpidetiedot'), 'Toimenpidetiedot', '__httpskeemat_jhs_suositukset_fitos20150115_kasittelyprosessiTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115Toimenpidetiedot', True, None, )

    
    Toimenpidetiedot = property(__Toimenpidetiedot.value, __Toimenpidetiedot.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}Kayttorajoitustiedot uses Python identifier Kayttorajoitustiedot
    __Kayttorajoitustiedot = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Kayttorajoitustiedot'), 'Kayttorajoitustiedot', '__httpskeemat_jhs_suositukset_fitos20150115_kasittelyprosessiTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115Kayttorajoitustiedot', False, None, )

    
    Kayttorajoitustiedot = property(__Kayttorajoitustiedot.value, __Kayttorajoitustiedot.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}Sailytysaikatiedot uses Python identifier Sailytysaikatiedot
    __Sailytysaikatiedot = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Sailytysaikatiedot'), 'Sailytysaikatiedot', '__httpskeemat_jhs_suositukset_fitos20150115_kasittelyprosessiTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115Sailytysaikatiedot', False, None, )

    
    Sailytysaikatiedot = property(__Sailytysaikatiedot.value, __Sailytysaikatiedot.set, None, None)

    
    # Attribute {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, 'id'), 'id', '__httpskeemat_jhs_suositukset_fitos20150115_kasittelyprosessiTiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115id', _module_typeBindings.idTyyppi, required=True)
    __id._DeclarationLocation = None
    __id._UseLocation = None
    
    id = property(__id.value, __id.set, None, None)

    _ElementMap.update({
        __OrganisaatioNimi.name() : __OrganisaatioNimi,
        __TietojarjestelmaNimi.name() : __TietojarjestelmaNimi,
        __LaatijaNimi.name() : __LaatijaNimi,
        __LaadittuPvm.name() : __LaadittuPvm,
        __MuokkaajaNimi.name() : __MuokkaajaNimi,
        __MuokattuPvm.name() : __MuokattuPvm,
        __HyvaksyjaNimi.name() : __HyvaksyjaNimi,
        __HyvaksyttyPvm.name() : __HyvaksyttyPvm,
        __VoimassaoloAlkaaPvm.name() : __VoimassaoloAlkaaPvm,
        __VoimassaoloPaattyyPvm.name() : __VoimassaoloPaattyyPvm,
        __PaatietoryhmatTeksti.name() : __PaatietoryhmatTeksti,
        __ProsessinOmistajaNimi.name() : __ProsessinOmistajaNimi,
        __KokoavanProsessitunnuksenLahdeTeksti.name() : __KokoavanProsessitunnuksenLahdeTeksti,
        __Laajennos.name() : __Laajennos,
        __Asiasanat.name() : __Asiasanat,
        __Toimenpidetiedot.name() : __Toimenpidetiedot,
        __Kayttorajoitustiedot.name() : __Kayttorajoitustiedot,
        __Sailytysaikatiedot.name() : __Sailytysaikatiedot
    })
    _AttributeMap.update({
        __id.name() : __id
    })
_module_typeBindings.kasittelyprosessiTiedotTyyppi = kasittelyprosessiTiedotTyyppi
Namespace.addCategoryObject('typeBinding', 'kasittelyprosessiTiedotTyyppi', kasittelyprosessiTiedotTyyppi)


# Complex type {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}toimenpidetiedotTyyppi with content type ELEMENT_ONLY
class toimenpidetiedotTyyppi (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}toimenpidetiedotTyyppi with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'toimenpidetiedotTyyppi')
    _XSDLocation = None
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}ToimenpiteenKuvausTeksti uses Python identifier ToimenpiteenKuvausTeksti
    __ToimenpiteenKuvausTeksti = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ToimenpiteenKuvausTeksti'), 'ToimenpiteenKuvausTeksti', '__httpskeemat_jhs_suositukset_fitos20150115_toimenpidetiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115ToimenpiteenKuvausTeksti', False, None, )

    
    ToimenpiteenKuvausTeksti = property(__ToimenpiteenKuvausTeksti.value, __ToimenpiteenKuvausTeksti.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}ToimenpideluokkaTeksti uses Python identifier ToimenpideluokkaTeksti
    __ToimenpideluokkaTeksti = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ToimenpideluokkaTeksti'), 'ToimenpideluokkaTeksti', '__httpskeemat_jhs_suositukset_fitos20150115_toimenpidetiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115ToimenpideluokkaTeksti', False, None, )

    
    ToimenpideluokkaTeksti = property(__ToimenpideluokkaTeksti.value, __ToimenpideluokkaTeksti.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}ToimenpideluokkaTarkenneTeksti uses Python identifier ToimenpideluokkaTarkenneTeksti
    __ToimenpideluokkaTarkenneTeksti = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ToimenpideluokkaTarkenneTeksti'), 'ToimenpideluokkaTarkenneTeksti', '__httpskeemat_jhs_suositukset_fitos20150115_toimenpidetiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115ToimenpideluokkaTarkenneTeksti', False, None, )

    
    ToimenpideluokkaTarkenneTeksti = property(__ToimenpideluokkaTarkenneTeksti.value, __ToimenpideluokkaTarkenneTeksti.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}KasittelyprosessinTilaTeksti uses Python identifier KasittelyprosessinTilaTeksti
    __KasittelyprosessinTilaTeksti = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'KasittelyprosessinTilaTeksti'), 'KasittelyprosessinTilaTeksti', '__httpskeemat_jhs_suositukset_fitos20150115_toimenpidetiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115KasittelyprosessinTilaTeksti', False, None, )

    
    KasittelyprosessinTilaTeksti = property(__KasittelyprosessinTilaTeksti.value, __KasittelyprosessinTilaTeksti.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}OrganisaatioNimi uses Python identifier OrganisaatioNimi
    __OrganisaatioNimi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OrganisaatioNimi'), 'OrganisaatioNimi', '__httpskeemat_jhs_suositukset_fitos20150115_toimenpidetiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115OrganisaatioNimi', False, None, )

    
    OrganisaatioNimi = property(__OrganisaatioNimi.value, __OrganisaatioNimi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}TietojarjestelmaNimi uses Python identifier TietojarjestelmaNimi
    __TietojarjestelmaNimi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TietojarjestelmaNimi'), 'TietojarjestelmaNimi', '__httpskeemat_jhs_suositukset_fitos20150115_toimenpidetiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115TietojarjestelmaNimi', False, None, )

    
    TietojarjestelmaNimi = property(__TietojarjestelmaNimi.value, __TietojarjestelmaNimi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}LaatijaNimi uses Python identifier LaatijaNimi
    __LaatijaNimi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LaatijaNimi'), 'LaatijaNimi', '__httpskeemat_jhs_suositukset_fitos20150115_toimenpidetiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115LaatijaNimi', False, None, )

    
    LaatijaNimi = property(__LaatijaNimi.value, __LaatijaNimi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}LaadittuPvm uses Python identifier LaadittuPvm
    __LaadittuPvm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LaadittuPvm'), 'LaadittuPvm', '__httpskeemat_jhs_suositukset_fitos20150115_toimenpidetiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115LaadittuPvm', False, None, )

    
    LaadittuPvm = property(__LaadittuPvm.value, __LaadittuPvm.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}MuokkaajaNimi uses Python identifier MuokkaajaNimi
    __MuokkaajaNimi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'MuokkaajaNimi'), 'MuokkaajaNimi', '__httpskeemat_jhs_suositukset_fitos20150115_toimenpidetiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115MuokkaajaNimi', False, None, )

    
    MuokkaajaNimi = property(__MuokkaajaNimi.value, __MuokkaajaNimi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}MuokattuPvm uses Python identifier MuokattuPvm
    __MuokattuPvm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'MuokattuPvm'), 'MuokattuPvm', '__httpskeemat_jhs_suositukset_fitos20150115_toimenpidetiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115MuokattuPvm', False, None, )

    
    MuokattuPvm = property(__MuokattuPvm.value, __MuokattuPvm.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}HyvaksyjaNimi uses Python identifier HyvaksyjaNimi
    __HyvaksyjaNimi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyjaNimi'), 'HyvaksyjaNimi', '__httpskeemat_jhs_suositukset_fitos20150115_toimenpidetiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115HyvaksyjaNimi', False, None, )

    
    HyvaksyjaNimi = property(__HyvaksyjaNimi.value, __HyvaksyjaNimi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}HyvaksyttyPvm uses Python identifier HyvaksyttyPvm
    __HyvaksyttyPvm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyttyPvm'), 'HyvaksyttyPvm', '__httpskeemat_jhs_suositukset_fitos20150115_toimenpidetiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115HyvaksyttyPvm', False, None, )

    
    HyvaksyttyPvm = property(__HyvaksyttyPvm.value, __HyvaksyttyPvm.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}VoimassaoloAlkaaPvm uses Python identifier VoimassaoloAlkaaPvm
    __VoimassaoloAlkaaPvm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloAlkaaPvm'), 'VoimassaoloAlkaaPvm', '__httpskeemat_jhs_suositukset_fitos20150115_toimenpidetiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115VoimassaoloAlkaaPvm', False, None, )

    
    VoimassaoloAlkaaPvm = property(__VoimassaoloAlkaaPvm.value, __VoimassaoloAlkaaPvm.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}VoimassaoloPaattyyPvm uses Python identifier VoimassaoloPaattyyPvm
    __VoimassaoloPaattyyPvm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloPaattyyPvm'), 'VoimassaoloPaattyyPvm', '__httpskeemat_jhs_suositukset_fitos20150115_toimenpidetiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115VoimassaoloPaattyyPvm', False, None, )

    
    VoimassaoloPaattyyPvm = property(__VoimassaoloPaattyyPvm.value, __VoimassaoloPaattyyPvm.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}Laajennos uses Python identifier Laajennos
    __Laajennos = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Laajennos'), 'Laajennos', '__httpskeemat_jhs_suositukset_fitos20150115_toimenpidetiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115Laajennos', True, None, )

    
    Laajennos = property(__Laajennos.value, __Laajennos.set, None, 'Yleinen laajennoselementti. Laajennoksilla mahdollistetaan organisaatiokohtaiset  elementit.')

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}Toimenpidetiedot uses Python identifier Toimenpidetiedot
    __Toimenpidetiedot = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Toimenpidetiedot'), 'Toimenpidetiedot', '__httpskeemat_jhs_suositukset_fitos20150115_toimenpidetiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115Toimenpidetiedot', True, None, )

    
    Toimenpidetiedot = property(__Toimenpidetiedot.value, __Toimenpidetiedot.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}Asiakirjatieto uses Python identifier Asiakirjatieto
    __Asiakirjatieto = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Asiakirjatieto'), 'Asiakirjatieto', '__httpskeemat_jhs_suositukset_fitos20150115_toimenpidetiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115Asiakirjatieto', True, None, )

    
    Asiakirjatieto = property(__Asiakirjatieto.value, __Asiakirjatieto.set, None, None)

    
    # Attribute {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, 'id'), 'id', '__httpskeemat_jhs_suositukset_fitos20150115_toimenpidetiedotTyyppi_httpskeemat_jhs_suositukset_fitos20150115id', _module_typeBindings.idTyyppi, required=True)
    __id._DeclarationLocation = None
    __id._UseLocation = None
    
    id = property(__id.value, __id.set, None, None)

    _ElementMap.update({
        __ToimenpiteenKuvausTeksti.name() : __ToimenpiteenKuvausTeksti,
        __ToimenpideluokkaTeksti.name() : __ToimenpideluokkaTeksti,
        __ToimenpideluokkaTarkenneTeksti.name() : __ToimenpideluokkaTarkenneTeksti,
        __KasittelyprosessinTilaTeksti.name() : __KasittelyprosessinTilaTeksti,
        __OrganisaatioNimi.name() : __OrganisaatioNimi,
        __TietojarjestelmaNimi.name() : __TietojarjestelmaNimi,
        __LaatijaNimi.name() : __LaatijaNimi,
        __LaadittuPvm.name() : __LaadittuPvm,
        __MuokkaajaNimi.name() : __MuokkaajaNimi,
        __MuokattuPvm.name() : __MuokattuPvm,
        __HyvaksyjaNimi.name() : __HyvaksyjaNimi,
        __HyvaksyttyPvm.name() : __HyvaksyttyPvm,
        __VoimassaoloAlkaaPvm.name() : __VoimassaoloAlkaaPvm,
        __VoimassaoloPaattyyPvm.name() : __VoimassaoloPaattyyPvm,
        __Laajennos.name() : __Laajennos,
        __Toimenpidetiedot.name() : __Toimenpidetiedot,
        __Asiakirjatieto.name() : __Asiakirjatieto
    })
    _AttributeMap.update({
        __id.name() : __id
    })
_module_typeBindings.toimenpidetiedotTyyppi = toimenpidetiedotTyyppi
Namespace.addCategoryObject('typeBinding', 'toimenpidetiedotTyyppi', toimenpidetiedotTyyppi)


# Complex type {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}asiakirjatietoTyyppi with content type ELEMENT_ONLY
class asiakirjatietoTyyppi (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}asiakirjatietoTyyppi with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'asiakirjatietoTyyppi')
    _XSDLocation = None
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}AsiakirjaluokkaTeksti uses Python identifier AsiakirjaluokkaTeksti
    __AsiakirjaluokkaTeksti = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AsiakirjaluokkaTeksti'), 'AsiakirjaluokkaTeksti', '__httpskeemat_jhs_suositukset_fitos20150115_asiakirjatietoTyyppi_httpskeemat_jhs_suositukset_fitos20150115AsiakirjaluokkaTeksti', False, None, )

    
    AsiakirjaluokkaTeksti = property(__AsiakirjaluokkaTeksti.value, __AsiakirjaluokkaTeksti.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}OrganisaatioNimi uses Python identifier OrganisaatioNimi
    __OrganisaatioNimi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'OrganisaatioNimi'), 'OrganisaatioNimi', '__httpskeemat_jhs_suositukset_fitos20150115_asiakirjatietoTyyppi_httpskeemat_jhs_suositukset_fitos20150115OrganisaatioNimi', False, None, )

    
    OrganisaatioNimi = property(__OrganisaatioNimi.value, __OrganisaatioNimi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}TietojarjestelmaNimi uses Python identifier TietojarjestelmaNimi
    __TietojarjestelmaNimi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TietojarjestelmaNimi'), 'TietojarjestelmaNimi', '__httpskeemat_jhs_suositukset_fitos20150115_asiakirjatietoTyyppi_httpskeemat_jhs_suositukset_fitos20150115TietojarjestelmaNimi', False, None, )

    
    TietojarjestelmaNimi = property(__TietojarjestelmaNimi.value, __TietojarjestelmaNimi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}LaatijaNimi uses Python identifier LaatijaNimi
    __LaatijaNimi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LaatijaNimi'), 'LaatijaNimi', '__httpskeemat_jhs_suositukset_fitos20150115_asiakirjatietoTyyppi_httpskeemat_jhs_suositukset_fitos20150115LaatijaNimi', False, None, )

    
    LaatijaNimi = property(__LaatijaNimi.value, __LaatijaNimi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}LaadittuPvm uses Python identifier LaadittuPvm
    __LaadittuPvm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LaadittuPvm'), 'LaadittuPvm', '__httpskeemat_jhs_suositukset_fitos20150115_asiakirjatietoTyyppi_httpskeemat_jhs_suositukset_fitos20150115LaadittuPvm', False, None, )

    
    LaadittuPvm = property(__LaadittuPvm.value, __LaadittuPvm.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}MuokkaajaNimi uses Python identifier MuokkaajaNimi
    __MuokkaajaNimi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'MuokkaajaNimi'), 'MuokkaajaNimi', '__httpskeemat_jhs_suositukset_fitos20150115_asiakirjatietoTyyppi_httpskeemat_jhs_suositukset_fitos20150115MuokkaajaNimi', False, None, )

    
    MuokkaajaNimi = property(__MuokkaajaNimi.value, __MuokkaajaNimi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}MuokattuPvm uses Python identifier MuokattuPvm
    __MuokattuPvm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'MuokattuPvm'), 'MuokattuPvm', '__httpskeemat_jhs_suositukset_fitos20150115_asiakirjatietoTyyppi_httpskeemat_jhs_suositukset_fitos20150115MuokattuPvm', False, None, )

    
    MuokattuPvm = property(__MuokattuPvm.value, __MuokattuPvm.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}HyvaksyjaNimi uses Python identifier HyvaksyjaNimi
    __HyvaksyjaNimi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyjaNimi'), 'HyvaksyjaNimi', '__httpskeemat_jhs_suositukset_fitos20150115_asiakirjatietoTyyppi_httpskeemat_jhs_suositukset_fitos20150115HyvaksyjaNimi', False, None, )

    
    HyvaksyjaNimi = property(__HyvaksyjaNimi.value, __HyvaksyjaNimi.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}HyvaksyttyPvm uses Python identifier HyvaksyttyPvm
    __HyvaksyttyPvm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyttyPvm'), 'HyvaksyttyPvm', '__httpskeemat_jhs_suositukset_fitos20150115_asiakirjatietoTyyppi_httpskeemat_jhs_suositukset_fitos20150115HyvaksyttyPvm', False, None, )

    
    HyvaksyttyPvm = property(__HyvaksyttyPvm.value, __HyvaksyttyPvm.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}VoimassaoloAlkaaPvm uses Python identifier VoimassaoloAlkaaPvm
    __VoimassaoloAlkaaPvm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloAlkaaPvm'), 'VoimassaoloAlkaaPvm', '__httpskeemat_jhs_suositukset_fitos20150115_asiakirjatietoTyyppi_httpskeemat_jhs_suositukset_fitos20150115VoimassaoloAlkaaPvm', False, None, )

    
    VoimassaoloAlkaaPvm = property(__VoimassaoloAlkaaPvm.value, __VoimassaoloAlkaaPvm.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}VoimassaoloPaattyyPvm uses Python identifier VoimassaoloPaattyyPvm
    __VoimassaoloPaattyyPvm = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloPaattyyPvm'), 'VoimassaoloPaattyyPvm', '__httpskeemat_jhs_suositukset_fitos20150115_asiakirjatietoTyyppi_httpskeemat_jhs_suositukset_fitos20150115VoimassaoloPaattyyPvm', False, None, )

    
    VoimassaoloPaattyyPvm = property(__VoimassaoloPaattyyPvm.value, __VoimassaoloPaattyyPvm.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}PaatietoryhmatTeksti uses Python identifier PaatietoryhmatTeksti
    __PaatietoryhmatTeksti = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PaatietoryhmatTeksti'), 'PaatietoryhmatTeksti', '__httpskeemat_jhs_suositukset_fitos20150115_asiakirjatietoTyyppi_httpskeemat_jhs_suositukset_fitos20150115PaatietoryhmatTeksti', False, None, )

    
    PaatietoryhmatTeksti = property(__PaatietoryhmatTeksti.value, __PaatietoryhmatTeksti.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}AsiakirjaluokkaTarkenneTeksti uses Python identifier AsiakirjaluokkaTarkenneTeksti
    __AsiakirjaluokkaTarkenneTeksti = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AsiakirjaluokkaTarkenneTeksti'), 'AsiakirjaluokkaTarkenneTeksti', '__httpskeemat_jhs_suositukset_fitos20150115_asiakirjatietoTyyppi_httpskeemat_jhs_suositukset_fitos20150115AsiakirjaluokkaTarkenneTeksti', False, None, )

    
    AsiakirjaluokkaTarkenneTeksti = property(__AsiakirjaluokkaTarkenneTeksti.value, __AsiakirjaluokkaTarkenneTeksti.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}Laajennos uses Python identifier Laajennos
    __Laajennos = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Laajennos'), 'Laajennos', '__httpskeemat_jhs_suositukset_fitos20150115_asiakirjatietoTyyppi_httpskeemat_jhs_suositukset_fitos20150115Laajennos', True, None, )

    
    Laajennos = property(__Laajennos.value, __Laajennos.set, None, 'Yleinen laajennoselementti. Laajennoksilla mahdollistetaan organisaatiokohtaiset  elementit.')

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}Asiasanat uses Python identifier Asiasanat
    __Asiasanat = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Asiasanat'), 'Asiasanat', '__httpskeemat_jhs_suositukset_fitos20150115_asiakirjatietoTyyppi_httpskeemat_jhs_suositukset_fitos20150115Asiasanat', True, None, )

    
    Asiasanat = property(__Asiasanat.value, __Asiasanat.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}Kasittelysaannot uses Python identifier Kasittelysaannot
    __Kasittelysaannot = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Kasittelysaannot'), 'Kasittelysaannot', '__httpskeemat_jhs_suositukset_fitos20150115_asiakirjatietoTyyppi_httpskeemat_jhs_suositukset_fitos20150115Kasittelysaannot', False, None, )

    
    Kasittelysaannot = property(__Kasittelysaannot.value, __Kasittelysaannot.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}Kayttorajoitustiedot uses Python identifier Kayttorajoitustiedot
    __Kayttorajoitustiedot = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Kayttorajoitustiedot'), 'Kayttorajoitustiedot', '__httpskeemat_jhs_suositukset_fitos20150115_asiakirjatietoTyyppi_httpskeemat_jhs_suositukset_fitos20150115Kayttorajoitustiedot', False, None, )

    
    Kayttorajoitustiedot = property(__Kayttorajoitustiedot.value, __Kayttorajoitustiedot.set, None, None)

    
    # Element {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}Sailytysaikatiedot uses Python identifier Sailytysaikatiedot
    __Sailytysaikatiedot = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Sailytysaikatiedot'), 'Sailytysaikatiedot', '__httpskeemat_jhs_suositukset_fitos20150115_asiakirjatietoTyyppi_httpskeemat_jhs_suositukset_fitos20150115Sailytysaikatiedot', False, None, )

    
    Sailytysaikatiedot = property(__Sailytysaikatiedot.value, __Sailytysaikatiedot.set, None, None)

    
    # Attribute {http://skeemat.jhs-suositukset.fi/tos/2015/01/15}id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, 'id'), 'id', '__httpskeemat_jhs_suositukset_fitos20150115_asiakirjatietoTyyppi_httpskeemat_jhs_suositukset_fitos20150115id', _module_typeBindings.idTyyppi, required=True)
    __id._DeclarationLocation = None
    __id._UseLocation = None
    
    id = property(__id.value, __id.set, None, None)

    _ElementMap.update({
        __AsiakirjaluokkaTeksti.name() : __AsiakirjaluokkaTeksti,
        __OrganisaatioNimi.name() : __OrganisaatioNimi,
        __TietojarjestelmaNimi.name() : __TietojarjestelmaNimi,
        __LaatijaNimi.name() : __LaatijaNimi,
        __LaadittuPvm.name() : __LaadittuPvm,
        __MuokkaajaNimi.name() : __MuokkaajaNimi,
        __MuokattuPvm.name() : __MuokattuPvm,
        __HyvaksyjaNimi.name() : __HyvaksyjaNimi,
        __HyvaksyttyPvm.name() : __HyvaksyttyPvm,
        __VoimassaoloAlkaaPvm.name() : __VoimassaoloAlkaaPvm,
        __VoimassaoloPaattyyPvm.name() : __VoimassaoloPaattyyPvm,
        __PaatietoryhmatTeksti.name() : __PaatietoryhmatTeksti,
        __AsiakirjaluokkaTarkenneTeksti.name() : __AsiakirjaluokkaTarkenneTeksti,
        __Laajennos.name() : __Laajennos,
        __Asiasanat.name() : __Asiasanat,
        __Kasittelysaannot.name() : __Kasittelysaannot,
        __Kayttorajoitustiedot.name() : __Kayttorajoitustiedot,
        __Sailytysaikatiedot.name() : __Sailytysaikatiedot
    })
    _AttributeMap.update({
        __id.name() : __id
    })
_module_typeBindings.asiakirjatietoTyyppi = asiakirjatietoTyyppi
Namespace.addCategoryObject('typeBinding', 'asiakirjatietoTyyppi', asiakirjatietoTyyppi)


OrganisaatioNimi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OrganisaatioNimi'), pyxb.binding.datatypes.string, location=None)
Namespace.addCategoryObject('elementBinding', OrganisaatioNimi.name().localName(), OrganisaatioNimi)

TietojarjestelmaNimi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TietojarjestelmaNimi'), pyxb.binding.datatypes.string, location=None)
Namespace.addCategoryObject('elementBinding', TietojarjestelmaNimi.name().localName(), TietojarjestelmaNimi)

AsiasanastoTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AsiasanastoTeksti'), pyxb.binding.datatypes.string, location=None)
Namespace.addCategoryObject('elementBinding', AsiasanastoTeksti.name().localName(), AsiasanastoTeksti)

AsiasanaTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AsiasanaTeksti'), pyxb.binding.datatypes.string, location=None)
Namespace.addCategoryObject('elementBinding', AsiasanaTeksti.name().localName(), AsiasanaTeksti)

PaatietoryhmatTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PaatietoryhmatTeksti'), pyxb.binding.datatypes.string, location=None)
Namespace.addCategoryObject('elementBinding', PaatietoryhmatTeksti.name().localName(), PaatietoryhmatTeksti)

KokoavanProsessitunnuksenLahdeTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'KokoavanProsessitunnuksenLahdeTeksti'), pyxb.binding.datatypes.string, location=None)
Namespace.addCategoryObject('elementBinding', KokoavanProsessitunnuksenLahdeTeksti.name().localName(), KokoavanProsessitunnuksenLahdeTeksti)

AsiakirjaluokkaTarkenneTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AsiakirjaluokkaTarkenneTeksti'), pyxb.binding.datatypes.string, location=None)
Namespace.addCategoryObject('elementBinding', AsiakirjaluokkaTarkenneTeksti.name().localName(), AsiakirjaluokkaTarkenneTeksti)

JulkisuusluokkaMuutosTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'JulkisuusluokkaMuutosTeksti'), pyxb.binding.datatypes.string, documentation='Esimerkiksi: Asian päättäminen, Päätöksenteko (toimenpide), Päätöksen allekirjoitus (toimenpide).', location=None)
Namespace.addCategoryObject('elementBinding', JulkisuusluokkaMuutosTeksti.name().localName(), JulkisuusluokkaMuutosTeksti)

AiempienVersioidenPoistoTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AiempienVersioidenPoistoTeksti'), pyxb.binding.datatypes.string, documentation='Suositeltavat: Asian ratkaisu, Tietty aika asian ratkaisusta, Asiakirjan hävittäminen.', location=None)
Namespace.addCategoryObject('elementBinding', AiempienVersioidenPoistoTeksti.name().localName(), AiempienVersioidenPoistoTeksti)

TallennuspaikkaTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TallennuspaikkaTeksti'), pyxb.binding.datatypes.string, location=None)
Namespace.addCategoryObject('elementBinding', TallennuspaikkaTeksti.name().localName(), TallennuspaikkaTeksti)

SailytyspaikkaTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SailytyspaikkaTeksti'), pyxb.binding.datatypes.string, location=None)
Namespace.addCategoryObject('elementBinding', SailytyspaikkaTeksti.name().localName(), SailytyspaikkaTeksti)

TilaKoodi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TilaKoodi'), tilaKoodiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', TilaKoodi.name().localName(), TilaKoodi)

TosVersio = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TosVersio'), versioTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', TosVersio.name().localName(), TosVersio)

OsaVersio = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OsaVersio'), versioTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', OsaVersio.name().localName(), OsaVersio)

Luokitustunnus = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Luokitustunnus'), luokitustunnusTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', Luokitustunnus.name().localName(), Luokitustunnus)

NimekeTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NimekeTeksti'), nimekeTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', NimekeTeksti.name().localName(), NimekeTeksti)

ToimenpiteenKuvausTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ToimenpiteenKuvausTeksti'), kuvausTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', ToimenpiteenKuvausTeksti.name().localName(), ToimenpiteenKuvausTeksti)

LuokitusKuvausTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LuokitusKuvausTeksti'), kuvausTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', LuokitusKuvausTeksti.name().localName(), LuokitusKuvausTeksti)

KuvausTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'KuvausTeksti'), kuvausTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', KuvausTeksti.name().localName(), KuvausTeksti)

LisatiedotTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LisatiedotTeksti'), lisatiedotTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', LisatiedotTeksti.name().localName(), LisatiedotTeksti)

JulkisuusluokkaKoodi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'JulkisuusluokkaKoodi'), julkisuusluokkaKoodiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', JulkisuusluokkaKoodi.name().localName(), JulkisuusluokkaKoodi)

SalassapitoAikaArvo = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SalassapitoAikaArvo'), salassapitoAikaArvoTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', SalassapitoAikaArvo.name().localName(), SalassapitoAikaArvo)

SalassapitoPerusteTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SalassapitoPerusteTeksti'), salassapitoPerusteTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', SalassapitoPerusteTeksti.name().localName(), SalassapitoPerusteTeksti)

SalassapidonLaskentaperusteTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SalassapidonLaskentaperusteTeksti'), salassapidonLaskentaperusteTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', SalassapidonLaskentaperusteTeksti.name().localName(), SalassapidonLaskentaperusteTeksti)

SuojaustasoKoodi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SuojaustasoKoodi'), suojaustasoKoodiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', SuojaustasoKoodi.name().localName(), SuojaustasoKoodi)

TurvallisuusluokkaKoodi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TurvallisuusluokkaKoodi'), turvallisuusluokkaKoodiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', TurvallisuusluokkaKoodi.name().localName(), TurvallisuusluokkaKoodi)

HenkilotietoluonneKoodi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HenkilotietoluonneKoodi'), henkilotietoluonneKoodiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', HenkilotietoluonneKoodi.name().localName(), HenkilotietoluonneKoodi)

SailytysajanPituusArvo = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SailytysajanPituusArvo'), sailytysajanPituusArvoTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', SailytysajanPituusArvo.name().localName(), SailytysajanPituusArvo)

SailytysajanPerusteTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SailytysajanPerusteTeksti'), sailytysajanPerusteTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', SailytysajanPerusteTeksti.name().localName(), SailytysajanPerusteTeksti)

SailytysajanLaskentaperusteTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SailytysajanLaskentaperusteTeksti'), sailytysajanLaskentaperusteTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', SailytysajanLaskentaperusteTeksti.name().localName(), SailytysajanLaskentaperusteTeksti)

ToimenpideluokkaTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ToimenpideluokkaTeksti'), toimenpideluokkaTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', ToimenpideluokkaTeksti.name().localName(), ToimenpideluokkaTeksti)

ToimenpideluokkaTarkenneTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ToimenpideluokkaTarkenneTeksti'), toimenpideluokkaTarkenneTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', ToimenpideluokkaTarkenneTeksti.name().localName(), ToimenpideluokkaTarkenneTeksti)

AsiakirjaluokkaTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AsiakirjaluokkaTeksti'), asiakirjaLuokkaTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', AsiakirjaluokkaTeksti.name().localName(), AsiakirjaluokkaTeksti)

KasittelyprosessinTilaTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'KasittelyprosessinTilaTeksti'), kasittelyprosessinTilaTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', KasittelyprosessinTilaTeksti.name().localName(), KasittelyprosessinTilaTeksti)

LaatijaNimi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LaatijaNimi'), _ImportedBinding_metarecord_binding__jhs.NimiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', LaatijaNimi.name().localName(), LaatijaNimi)

LaadittuPvm = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LaadittuPvm'), _ImportedBinding_metarecord_binding__jhs.AlkuPvmTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', LaadittuPvm.name().localName(), LaadittuPvm)

MuokkaajaNimi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MuokkaajaNimi'), _ImportedBinding_metarecord_binding__jhs.NimiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', MuokkaajaNimi.name().localName(), MuokkaajaNimi)

MuokattuPvm = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MuokattuPvm'), _ImportedBinding_metarecord_binding__jhs.AlkuPvmTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', MuokattuPvm.name().localName(), MuokattuPvm)

HyvaksyjaNimi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyjaNimi'), _ImportedBinding_metarecord_binding__jhs.NimiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', HyvaksyjaNimi.name().localName(), HyvaksyjaNimi)

HyvaksyttyPvm = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyttyPvm'), _ImportedBinding_metarecord_binding__jhs.AlkuPvmTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', HyvaksyttyPvm.name().localName(), HyvaksyttyPvm)

VoimassaoloAlkaaPvm = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloAlkaaPvm'), _ImportedBinding_metarecord_binding__jhs.AlkuPvmTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', VoimassaoloAlkaaPvm.name().localName(), VoimassaoloAlkaaPvm)

VoimassaoloPaattyyPvm = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloPaattyyPvm'), _ImportedBinding_metarecord_binding__jhs.LoppuPvmTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', VoimassaoloPaattyyPvm.name().localName(), VoimassaoloPaattyyPvm)

YhteyshenkiloNimi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'YhteyshenkiloNimi'), _ImportedBinding_metarecord_binding__jhs.NimiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', YhteyshenkiloNimi.name().localName(), YhteyshenkiloNimi)

ProsessinOmistajaNimi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProsessinOmistajaNimi'), _ImportedBinding_metarecord_binding__jhs.NimiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', ProsessinOmistajaNimi.name().localName(), ProsessinOmistajaNimi)

Tos = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Tos'), CTD_ANON, location=None)
Namespace.addCategoryObject('elementBinding', Tos.name().localName(), Tos)

Laajennos = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Laajennos'), CTD_ANON_, documentation='Yleinen laajennoselementti. Laajennoksilla mahdollistetaan organisaatiokohtaiset  elementit.', location=None)
Namespace.addCategoryObject('elementBinding', Laajennos.name().localName(), Laajennos)

Nimeke = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Nimeke'), nimekeTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', Nimeke.name().localName(), Nimeke)

Asiasanat = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Asiasanat'), asiasanatTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', Asiasanat.name().localName(), Asiasanat)

Kasittelysaannot = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Kasittelysaannot'), kasittelysaannotTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', Kasittelysaannot.name().localName(), Kasittelysaannot)

Kayttorajoitustiedot = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Kayttorajoitustiedot'), kayttorajoitusTiedotTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', Kayttorajoitustiedot.name().localName(), Kayttorajoitustiedot)

Sailytysaikatiedot = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Sailytysaikatiedot'), sailytysaikaTiedotTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', Sailytysaikatiedot.name().localName(), Sailytysaikatiedot)

TosTiedot = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TosTiedot'), TosTiedotTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', TosTiedot.name().localName(), TosTiedot)

Luokka = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Luokka'), luokkaTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', Luokka.name().localName(), Luokka)

NimekeKielella = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NimekeKielella'), nimekeKielellaTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', NimekeKielella.name().localName(), NimekeKielella)

KasittelyprosessiTiedot = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'KasittelyprosessiTiedot'), kasittelyprosessiTiedotTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', KasittelyprosessiTiedot.name().localName(), KasittelyprosessiTiedot)

Toimenpidetiedot = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Toimenpidetiedot'), toimenpidetiedotTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', Toimenpidetiedot.name().localName(), Toimenpidetiedot)

Asiakirjatieto = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Asiakirjatieto'), asiakirjatietoTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', Asiakirjatieto.name().localName(), Asiakirjatieto)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TosTiedot'), TosTiedotTyyppi, scope=CTD_ANON, location=None))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Luokka'), luokkaTyyppi, scope=CTD_ANON, location=None))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Laajennos'), CTD_ANON_, scope=CTD_ANON, documentation='Yleinen laajennoselementti. Laajennoksilla mahdollistetaan organisaatiokohtaiset  elementit.', location=None))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=None)
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TosTiedot')), None)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Luokka')), None)
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Laajennos')), None)
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton()




def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_skip, namespace_constraint=pyxb.binding.content.Wildcard.NC_any), None)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_._Automaton = _BuildAutomaton_()




nimekeTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NimekeTeksti'), nimekeTekstiTyyppi, scope=nimekeTyyppi, location=None))

nimekeTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NimekeKielella'), nimekeKielellaTyyppi, scope=nimekeTyyppi, location=None))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(nimekeTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NimekeKielella')), None)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(nimekeTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NimekeTeksti')), None)
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
nimekeTyyppi._Automaton = _BuildAutomaton_2()




asiasanatTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AsiasanastoTeksti'), pyxb.binding.datatypes.string, scope=asiasanatTyyppi, location=None))

asiasanatTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AsiasanaTeksti'), pyxb.binding.datatypes.string, scope=asiasanatTyyppi, location=None))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=None)
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=None)
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(asiasanatTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AsiasanastoTeksti')), None)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(asiasanatTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AsiasanaTeksti')), None)
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
asiasanatTyyppi._Automaton = _BuildAutomaton_3()




kasittelysaannotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'JulkisuusluokkaMuutosTeksti'), pyxb.binding.datatypes.string, scope=kasittelysaannotTyyppi, documentation='Esimerkiksi: Asian päättäminen, Päätöksenteko (toimenpide), Päätöksen allekirjoitus (toimenpide).', location=None))

kasittelysaannotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AiempienVersioidenPoistoTeksti'), pyxb.binding.datatypes.string, scope=kasittelysaannotTyyppi, documentation='Suositeltavat: Asian ratkaisu, Tietty aika asian ratkaisusta, Asiakirjan hävittäminen.', location=None))

kasittelysaannotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TallennuspaikkaTeksti'), pyxb.binding.datatypes.string, scope=kasittelysaannotTyyppi, location=None))

kasittelysaannotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SailytyspaikkaTeksti'), pyxb.binding.datatypes.string, scope=kasittelysaannotTyyppi, location=None))

kasittelysaannotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Laajennos'), CTD_ANON_, scope=kasittelysaannotTyyppi, documentation='Yleinen laajennoselementti. Laajennoksilla mahdollistetaan organisaatiokohtaiset  elementit.', location=None))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=None)
    counters.add(cc_4)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(kasittelysaannotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'JulkisuusluokkaMuutosTeksti')), None)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(kasittelysaannotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AiempienVersioidenPoistoTeksti')), None)
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(kasittelysaannotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TallennuspaikkaTeksti')), None)
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(kasittelysaannotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SailytyspaikkaTeksti')), None)
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(kasittelysaannotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Laajennos')), None)
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
kasittelysaannotTyyppi._Automaton = _BuildAutomaton_4()




kayttorajoitusTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'JulkisuusluokkaKoodi'), julkisuusluokkaKoodiTyyppi, scope=kayttorajoitusTiedotTyyppi, location=None))

kayttorajoitusTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SalassapitoAikaArvo'), salassapitoAikaArvoTyyppi, scope=kayttorajoitusTiedotTyyppi, location=None))

kayttorajoitusTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SalassapitoPerusteTeksti'), salassapitoPerusteTekstiTyyppi, scope=kayttorajoitusTiedotTyyppi, location=None))

kayttorajoitusTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SalassapidonLaskentaperusteTeksti'), salassapidonLaskentaperusteTekstiTyyppi, scope=kayttorajoitusTiedotTyyppi, location=None))

kayttorajoitusTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SuojaustasoKoodi'), suojaustasoKoodiTyyppi, scope=kayttorajoitusTiedotTyyppi, location=None))

kayttorajoitusTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TurvallisuusluokkaKoodi'), turvallisuusluokkaKoodiTyyppi, scope=kayttorajoitusTiedotTyyppi, location=None))

kayttorajoitusTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HenkilotietoluonneKoodi'), henkilotietoluonneKoodiTyyppi, scope=kayttorajoitusTiedotTyyppi, location=None))

kayttorajoitusTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Laajennos'), CTD_ANON_, scope=kayttorajoitusTiedotTyyppi, documentation='Yleinen laajennoselementti. Laajennoksilla mahdollistetaan organisaatiokohtaiset  elementit.', location=None))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=None, metadata=None)
    counters.add(cc_7)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(kayttorajoitusTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'JulkisuusluokkaKoodi')), None)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(kayttorajoitusTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SuojaustasoKoodi')), None)
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(kayttorajoitusTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TurvallisuusluokkaKoodi')), None)
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(kayttorajoitusTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'HenkilotietoluonneKoodi')), None)
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(kayttorajoitusTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SalassapitoAikaArvo')), None)
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(kayttorajoitusTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SalassapitoPerusteTeksti')), None)
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(kayttorajoitusTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SalassapidonLaskentaperusteTeksti')), None)
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(kayttorajoitusTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Laajennos')), None)
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True) ]))
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
kayttorajoitusTiedotTyyppi._Automaton = _BuildAutomaton_5()




sailytysaikaTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SailytysajanPituusArvo'), sailytysajanPituusArvoTyyppi, scope=sailytysaikaTiedotTyyppi, location=None))

sailytysaikaTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SailytysajanPerusteTeksti'), sailytysajanPerusteTekstiTyyppi, scope=sailytysaikaTiedotTyyppi, location=None))

sailytysaikaTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SailytysajanLaskentaperusteTeksti'), sailytysajanLaskentaperusteTekstiTyyppi, scope=sailytysaikaTiedotTyyppi, location=None))

sailytysaikaTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Laajennos'), CTD_ANON_, scope=sailytysaikaTiedotTyyppi, documentation='Yleinen laajennoselementti. Laajennoksilla mahdollistetaan organisaatiokohtaiset  elementit.', location=None))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=None)
    counters.add(cc_3)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(sailytysaikaTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SailytysajanPituusArvo')), None)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(sailytysaikaTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SailytysajanPerusteTeksti')), None)
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(sailytysaikaTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'SailytysajanLaskentaperusteTeksti')), None)
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(sailytysaikaTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Laajennos')), None)
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
sailytysaikaTiedotTyyppi._Automaton = _BuildAutomaton_6()




TosTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TilaKoodi'), tilaKoodiTyyppi, scope=TosTiedotTyyppi, location=None))

TosTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TosVersio'), versioTyyppi, scope=TosTiedotTyyppi, location=None))

TosTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LisatiedotTeksti'), lisatiedotTekstiTyyppi, scope=TosTiedotTyyppi, location=None))

TosTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OrganisaatioNimi'), pyxb.binding.datatypes.string, scope=TosTiedotTyyppi, location=None))

TosTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LaatijaNimi'), _ImportedBinding_metarecord_binding__jhs.NimiTyyppi, scope=TosTiedotTyyppi, location=None))

TosTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LaadittuPvm'), _ImportedBinding_metarecord_binding__jhs.AlkuPvmTyyppi, scope=TosTiedotTyyppi, location=None))

TosTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MuokkaajaNimi'), _ImportedBinding_metarecord_binding__jhs.NimiTyyppi, scope=TosTiedotTyyppi, location=None))

TosTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MuokattuPvm'), _ImportedBinding_metarecord_binding__jhs.AlkuPvmTyyppi, scope=TosTiedotTyyppi, location=None))

TosTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyjaNimi'), _ImportedBinding_metarecord_binding__jhs.NimiTyyppi, scope=TosTiedotTyyppi, location=None))

TosTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyttyPvm'), _ImportedBinding_metarecord_binding__jhs.AlkuPvmTyyppi, scope=TosTiedotTyyppi, location=None))

TosTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloAlkaaPvm'), _ImportedBinding_metarecord_binding__jhs.AlkuPvmTyyppi, scope=TosTiedotTyyppi, location=None))

TosTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloPaattyyPvm'), _ImportedBinding_metarecord_binding__jhs.LoppuPvmTyyppi, scope=TosTiedotTyyppi, location=None))

TosTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'YhteyshenkiloNimi'), _ImportedBinding_metarecord_binding__jhs.NimiTyyppi, scope=TosTiedotTyyppi, location=None))

TosTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Laajennos'), CTD_ANON_, scope=TosTiedotTyyppi, documentation='Yleinen laajennoselementti. Laajennoksilla mahdollistetaan organisaatiokohtaiset  elementit.', location=None))

TosTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Nimeke'), nimekeTyyppi, scope=TosTiedotTyyppi, location=None))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=None, metadata=None)
    counters.add(cc_11)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(TosTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Nimeke')), None)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(TosTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'YhteyshenkiloNimi')), None)
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(TosTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TosVersio')), None)
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(TosTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TilaKoodi')), None)
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(TosTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OrganisaatioNimi')), None)
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(TosTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LaatijaNimi')), None)
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(TosTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LaadittuPvm')), None)
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(TosTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'MuokkaajaNimi')), None)
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(TosTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'MuokattuPvm')), None)
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(TosTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyjaNimi')), None)
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(TosTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyttyPvm')), None)
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(TosTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloAlkaaPvm')), None)
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(TosTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloPaattyyPvm')), None)
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(TosTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LisatiedotTeksti')), None)
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(TosTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Laajennos')), None)
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    transitions.append(fac.Transition(st_9, [
         ]))
    transitions.append(fac.Transition(st_10, [
         ]))
    transitions.append(fac.Transition(st_11, [
         ]))
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_11, True) ]))
    st_14._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
TosTiedotTyyppi._Automaton = _BuildAutomaton_7()




luokkaTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TilaKoodi'), tilaKoodiTyyppi, scope=luokkaTyyppi, location=None))

luokkaTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OsaVersio'), versioTyyppi, scope=luokkaTyyppi, location=None))

luokkaTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Luokitustunnus'), luokitustunnusTyyppi, scope=luokkaTyyppi, location=None))

luokkaTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LuokitusKuvausTeksti'), kuvausTekstiTyyppi, scope=luokkaTyyppi, location=None))

luokkaTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OrganisaatioNimi'), pyxb.binding.datatypes.string, scope=luokkaTyyppi, location=None))

luokkaTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LaatijaNimi'), _ImportedBinding_metarecord_binding__jhs.NimiTyyppi, scope=luokkaTyyppi, location=None))

luokkaTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LaadittuPvm'), _ImportedBinding_metarecord_binding__jhs.AlkuPvmTyyppi, scope=luokkaTyyppi, location=None))

luokkaTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MuokkaajaNimi'), _ImportedBinding_metarecord_binding__jhs.NimiTyyppi, scope=luokkaTyyppi, location=None))

luokkaTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MuokattuPvm'), _ImportedBinding_metarecord_binding__jhs.AlkuPvmTyyppi, scope=luokkaTyyppi, location=None))

luokkaTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyjaNimi'), _ImportedBinding_metarecord_binding__jhs.NimiTyyppi, scope=luokkaTyyppi, location=None))

luokkaTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyttyPvm'), _ImportedBinding_metarecord_binding__jhs.AlkuPvmTyyppi, scope=luokkaTyyppi, location=None))

luokkaTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloAlkaaPvm'), _ImportedBinding_metarecord_binding__jhs.AlkuPvmTyyppi, scope=luokkaTyyppi, location=None))

luokkaTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloPaattyyPvm'), _ImportedBinding_metarecord_binding__jhs.LoppuPvmTyyppi, scope=luokkaTyyppi, location=None))

luokkaTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Laajennos'), CTD_ANON_, scope=luokkaTyyppi, documentation='Yleinen laajennoselementti. Laajennoksilla mahdollistetaan organisaatiokohtaiset  elementit.', location=None))

luokkaTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Nimeke'), nimekeTyyppi, scope=luokkaTyyppi, location=None))

luokkaTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'KasittelyprosessiTiedot'), kasittelyprosessiTiedotTyyppi, scope=luokkaTyyppi, location=None))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=None, metadata=None)
    counters.add(cc_13)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(luokkaTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OrganisaatioNimi')), None)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(luokkaTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LaatijaNimi')), None)
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(luokkaTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LaadittuPvm')), None)
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(luokkaTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'MuokkaajaNimi')), None)
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(luokkaTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'MuokattuPvm')), None)
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(luokkaTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyjaNimi')), None)
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(luokkaTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyttyPvm')), None)
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(luokkaTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloAlkaaPvm')), None)
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(luokkaTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloPaattyyPvm')), None)
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(luokkaTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Luokitustunnus')), None)
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(luokkaTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TilaKoodi')), None)
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(luokkaTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OsaVersio')), None)
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(luokkaTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Nimeke')), None)
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(luokkaTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LuokitusKuvausTeksti')), None)
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(luokkaTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'KasittelyprosessiTiedot')), None)
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(luokkaTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Laajennos')), None)
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
         ]))
    transitions.append(fac.Transition(st_11, [
         ]))
    transitions.append(fac.Transition(st_12, [
         ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    transitions.append(fac.Transition(st_15, [
         ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_11, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_12, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_13, True) ]))
    st_15._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
luokkaTyyppi._Automaton = _BuildAutomaton_8()




nimekeKielellaTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NimekeTeksti'), nimekeTekstiTyyppi, scope=nimekeKielellaTyyppi, location=None))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(nimekeKielellaTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'NimekeTeksti')), None)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
nimekeKielellaTyyppi._Automaton = _BuildAutomaton_9()




kasittelyprosessiTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OrganisaatioNimi'), pyxb.binding.datatypes.string, scope=kasittelyprosessiTiedotTyyppi, location=None))

kasittelyprosessiTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TietojarjestelmaNimi'), pyxb.binding.datatypes.string, scope=kasittelyprosessiTiedotTyyppi, location=None))

kasittelyprosessiTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LaatijaNimi'), _ImportedBinding_metarecord_binding__jhs.NimiTyyppi, scope=kasittelyprosessiTiedotTyyppi, location=None))

kasittelyprosessiTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LaadittuPvm'), _ImportedBinding_metarecord_binding__jhs.AlkuPvmTyyppi, scope=kasittelyprosessiTiedotTyyppi, location=None))

kasittelyprosessiTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MuokkaajaNimi'), _ImportedBinding_metarecord_binding__jhs.NimiTyyppi, scope=kasittelyprosessiTiedotTyyppi, location=None))

kasittelyprosessiTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MuokattuPvm'), _ImportedBinding_metarecord_binding__jhs.AlkuPvmTyyppi, scope=kasittelyprosessiTiedotTyyppi, location=None))

kasittelyprosessiTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyjaNimi'), _ImportedBinding_metarecord_binding__jhs.NimiTyyppi, scope=kasittelyprosessiTiedotTyyppi, location=None))

kasittelyprosessiTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyttyPvm'), _ImportedBinding_metarecord_binding__jhs.AlkuPvmTyyppi, scope=kasittelyprosessiTiedotTyyppi, location=None))

kasittelyprosessiTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloAlkaaPvm'), _ImportedBinding_metarecord_binding__jhs.AlkuPvmTyyppi, scope=kasittelyprosessiTiedotTyyppi, location=None))

kasittelyprosessiTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloPaattyyPvm'), _ImportedBinding_metarecord_binding__jhs.LoppuPvmTyyppi, scope=kasittelyprosessiTiedotTyyppi, location=None))

kasittelyprosessiTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PaatietoryhmatTeksti'), pyxb.binding.datatypes.string, scope=kasittelyprosessiTiedotTyyppi, location=None))

kasittelyprosessiTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ProsessinOmistajaNimi'), _ImportedBinding_metarecord_binding__jhs.NimiTyyppi, scope=kasittelyprosessiTiedotTyyppi, location=None))

kasittelyprosessiTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'KokoavanProsessitunnuksenLahdeTeksti'), pyxb.binding.datatypes.string, scope=kasittelyprosessiTiedotTyyppi, location=None))

kasittelyprosessiTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Laajennos'), CTD_ANON_, scope=kasittelyprosessiTiedotTyyppi, documentation='Yleinen laajennoselementti. Laajennoksilla mahdollistetaan organisaatiokohtaiset  elementit.', location=None))

kasittelyprosessiTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Asiasanat'), asiasanatTyyppi, scope=kasittelyprosessiTiedotTyyppi, location=None))

kasittelyprosessiTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Toimenpidetiedot'), toimenpidetiedotTyyppi, scope=kasittelyprosessiTiedotTyyppi, location=None))

kasittelyprosessiTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Kayttorajoitustiedot'), kayttorajoitusTiedotTyyppi, scope=kasittelyprosessiTiedotTyyppi, location=None))

kasittelyprosessiTiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Sailytysaikatiedot'), sailytysaikaTiedotTyyppi, scope=kasittelyprosessiTiedotTyyppi, location=None))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=None)
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=None, metadata=None)
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=None, metadata=None)
    counters.add(cc_15)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(kasittelyprosessiTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TietojarjestelmaNimi')), None)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(kasittelyprosessiTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Kayttorajoitustiedot')), None)
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(kasittelyprosessiTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Sailytysaikatiedot')), None)
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(kasittelyprosessiTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Toimenpidetiedot')), None)
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(kasittelyprosessiTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OrganisaatioNimi')), None)
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(kasittelyprosessiTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LaatijaNimi')), None)
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(kasittelyprosessiTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LaadittuPvm')), None)
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(kasittelyprosessiTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'MuokkaajaNimi')), None)
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(kasittelyprosessiTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'MuokattuPvm')), None)
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(kasittelyprosessiTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyjaNimi')), None)
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(kasittelyprosessiTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyttyPvm')), None)
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(kasittelyprosessiTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloAlkaaPvm')), None)
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(kasittelyprosessiTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloPaattyyPvm')), None)
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(kasittelyprosessiTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Asiasanat')), None)
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(kasittelyprosessiTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PaatietoryhmatTeksti')), None)
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(kasittelyprosessiTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ProsessinOmistajaNimi')), None)
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(kasittelyprosessiTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'KokoavanProsessitunnuksenLahdeTeksti')), None)
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(kasittelyprosessiTiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Laajennos')), None)
    st_17 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    transitions.append(fac.Transition(st_9, [
         ]))
    transitions.append(fac.Transition(st_10, [
         ]))
    transitions.append(fac.Transition(st_11, [
         ]))
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    transitions.append(fac.Transition(st_15, [
         ]))
    transitions.append(fac.Transition(st_16, [
         ]))
    transitions.append(fac.Transition(st_17, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_11, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_12, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_13, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_13, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_14, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_14, False) ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_15, True) ]))
    st_17._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
kasittelyprosessiTiedotTyyppi._Automaton = _BuildAutomaton_10()




toimenpidetiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ToimenpiteenKuvausTeksti'), kuvausTekstiTyyppi, scope=toimenpidetiedotTyyppi, location=None))

toimenpidetiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ToimenpideluokkaTeksti'), toimenpideluokkaTekstiTyyppi, scope=toimenpidetiedotTyyppi, location=None))

toimenpidetiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ToimenpideluokkaTarkenneTeksti'), toimenpideluokkaTarkenneTekstiTyyppi, scope=toimenpidetiedotTyyppi, location=None))

toimenpidetiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'KasittelyprosessinTilaTeksti'), kasittelyprosessinTilaTekstiTyyppi, scope=toimenpidetiedotTyyppi, location=None))

toimenpidetiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OrganisaatioNimi'), pyxb.binding.datatypes.string, scope=toimenpidetiedotTyyppi, location=None))

toimenpidetiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TietojarjestelmaNimi'), pyxb.binding.datatypes.string, scope=toimenpidetiedotTyyppi, location=None))

toimenpidetiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LaatijaNimi'), _ImportedBinding_metarecord_binding__jhs.NimiTyyppi, scope=toimenpidetiedotTyyppi, location=None))

toimenpidetiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LaadittuPvm'), _ImportedBinding_metarecord_binding__jhs.AlkuPvmTyyppi, scope=toimenpidetiedotTyyppi, location=None))

toimenpidetiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MuokkaajaNimi'), _ImportedBinding_metarecord_binding__jhs.NimiTyyppi, scope=toimenpidetiedotTyyppi, location=None))

toimenpidetiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MuokattuPvm'), _ImportedBinding_metarecord_binding__jhs.AlkuPvmTyyppi, scope=toimenpidetiedotTyyppi, location=None))

toimenpidetiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyjaNimi'), _ImportedBinding_metarecord_binding__jhs.NimiTyyppi, scope=toimenpidetiedotTyyppi, location=None))

toimenpidetiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyttyPvm'), _ImportedBinding_metarecord_binding__jhs.AlkuPvmTyyppi, scope=toimenpidetiedotTyyppi, location=None))

toimenpidetiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloAlkaaPvm'), _ImportedBinding_metarecord_binding__jhs.AlkuPvmTyyppi, scope=toimenpidetiedotTyyppi, location=None))

toimenpidetiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloPaattyyPvm'), _ImportedBinding_metarecord_binding__jhs.LoppuPvmTyyppi, scope=toimenpidetiedotTyyppi, location=None))

toimenpidetiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Laajennos'), CTD_ANON_, scope=toimenpidetiedotTyyppi, documentation='Yleinen laajennoselementti. Laajennoksilla mahdollistetaan organisaatiokohtaiset  elementit.', location=None))

toimenpidetiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Toimenpidetiedot'), toimenpidetiedotTyyppi, scope=toimenpidetiedotTyyppi, location=None))

toimenpidetiedotTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Asiakirjatieto'), asiakirjatietoTyyppi, scope=toimenpidetiedotTyyppi, location=None))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=None, metadata=None)
    counters.add(cc_15)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(toimenpidetiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ToimenpideluokkaTeksti')), None)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(toimenpidetiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ToimenpideluokkaTarkenneTeksti')), None)
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(toimenpidetiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ToimenpiteenKuvausTeksti')), None)
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(toimenpidetiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'KasittelyprosessinTilaTeksti')), None)
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(toimenpidetiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TietojarjestelmaNimi')), None)
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(toimenpidetiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OrganisaatioNimi')), None)
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(toimenpidetiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LaatijaNimi')), None)
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(toimenpidetiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LaadittuPvm')), None)
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(toimenpidetiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'MuokkaajaNimi')), None)
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(toimenpidetiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'MuokattuPvm')), None)
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(toimenpidetiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyjaNimi')), None)
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(toimenpidetiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyttyPvm')), None)
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(toimenpidetiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloAlkaaPvm')), None)
    st_12 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(toimenpidetiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloPaattyyPvm')), None)
    st_13 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(toimenpidetiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Asiakirjatieto')), None)
    st_14 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(toimenpidetiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Toimenpidetiedot')), None)
    st_15 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(toimenpidetiedotTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Laajennos')), None)
    st_16 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_11, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_12, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_13, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_13, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
         ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_14, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_14, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_14, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_14, True) ]))
    transitions.append(fac.Transition(st_15, [
         ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_14, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_14, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_15, True) ]))
    st_16._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
toimenpidetiedotTyyppi._Automaton = _BuildAutomaton_11()




asiakirjatietoTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AsiakirjaluokkaTeksti'), asiakirjaLuokkaTekstiTyyppi, scope=asiakirjatietoTyyppi, location=None))

asiakirjatietoTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OrganisaatioNimi'), pyxb.binding.datatypes.string, scope=asiakirjatietoTyyppi, location=None))

asiakirjatietoTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TietojarjestelmaNimi'), pyxb.binding.datatypes.string, scope=asiakirjatietoTyyppi, location=None))

asiakirjatietoTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LaatijaNimi'), _ImportedBinding_metarecord_binding__jhs.NimiTyyppi, scope=asiakirjatietoTyyppi, location=None))

asiakirjatietoTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LaadittuPvm'), _ImportedBinding_metarecord_binding__jhs.AlkuPvmTyyppi, scope=asiakirjatietoTyyppi, location=None))

asiakirjatietoTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MuokkaajaNimi'), _ImportedBinding_metarecord_binding__jhs.NimiTyyppi, scope=asiakirjatietoTyyppi, location=None))

asiakirjatietoTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MuokattuPvm'), _ImportedBinding_metarecord_binding__jhs.AlkuPvmTyyppi, scope=asiakirjatietoTyyppi, location=None))

asiakirjatietoTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyjaNimi'), _ImportedBinding_metarecord_binding__jhs.NimiTyyppi, scope=asiakirjatietoTyyppi, location=None))

asiakirjatietoTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyttyPvm'), _ImportedBinding_metarecord_binding__jhs.AlkuPvmTyyppi, scope=asiakirjatietoTyyppi, location=None))

asiakirjatietoTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloAlkaaPvm'), _ImportedBinding_metarecord_binding__jhs.AlkuPvmTyyppi, scope=asiakirjatietoTyyppi, location=None))

asiakirjatietoTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloPaattyyPvm'), _ImportedBinding_metarecord_binding__jhs.LoppuPvmTyyppi, scope=asiakirjatietoTyyppi, location=None))

asiakirjatietoTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PaatietoryhmatTeksti'), pyxb.binding.datatypes.string, scope=asiakirjatietoTyyppi, location=None))

asiakirjatietoTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AsiakirjaluokkaTarkenneTeksti'), pyxb.binding.datatypes.string, scope=asiakirjatietoTyyppi, location=None))

asiakirjatietoTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Laajennos'), CTD_ANON_, scope=asiakirjatietoTyyppi, documentation='Yleinen laajennoselementti. Laajennoksilla mahdollistetaan organisaatiokohtaiset  elementit.', location=None))

asiakirjatietoTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Asiasanat'), asiasanatTyyppi, scope=asiakirjatietoTyyppi, location=None))

asiakirjatietoTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Kasittelysaannot'), kasittelysaannotTyyppi, scope=asiakirjatietoTyyppi, location=None))

asiakirjatietoTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Kayttorajoitustiedot'), kayttorajoitusTiedotTyyppi, scope=asiakirjatietoTyyppi, location=None))

asiakirjatietoTyyppi._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Sailytysaikatiedot'), sailytysaikaTiedotTyyppi, scope=asiakirjatietoTyyppi, location=None))

def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=None, metadata=None)
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=None)
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=None, metadata=None)
    counters.add(cc_14)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(asiakirjatietoTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Kayttorajoitustiedot')), None)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(asiakirjatietoTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Sailytysaikatiedot')), None)
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(asiakirjatietoTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'OrganisaatioNimi')), None)
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(asiakirjatietoTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LaatijaNimi')), None)
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(asiakirjatietoTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LaadittuPvm')), None)
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(asiakirjatietoTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'MuokkaajaNimi')), None)
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(asiakirjatietoTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'MuokattuPvm')), None)
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(asiakirjatietoTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyjaNimi')), None)
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(asiakirjatietoTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'HyvaksyttyPvm')), None)
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(asiakirjatietoTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloAlkaaPvm')), None)
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(asiakirjatietoTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloPaattyyPvm')), None)
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(asiakirjatietoTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AsiakirjaluokkaTeksti')), None)
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(asiakirjatietoTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AsiakirjaluokkaTarkenneTeksti')), None)
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(asiakirjatietoTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TietojarjestelmaNimi')), None)
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(asiakirjatietoTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Kasittelysaannot')), None)
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(asiakirjatietoTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Asiasanat')), None)
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(asiakirjatietoTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PaatietoryhmatTeksti')), None)
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(asiakirjatietoTyyppi._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Laajennos')), None)
    st_17 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    transitions.append(fac.Transition(st_9, [
         ]))
    transitions.append(fac.Transition(st_10, [
         ]))
    transitions.append(fac.Transition(st_11, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    transitions.append(fac.Transition(st_15, [
         ]))
    transitions.append(fac.Transition(st_16, [
         ]))
    transitions.append(fac.Transition(st_17, [
         ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_11, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_12, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_13, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_13, False) ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_14, True) ]))
    st_17._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
asiakirjatietoTyyppi._Automaton = _BuildAutomaton_12()

