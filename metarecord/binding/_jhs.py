# ./metarecord/binding/_jhs.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:567ab21ac37a6d7db45f717b194c27c1e22858bd
# Generated 2020-04-06 06:44:21.528876 by PyXB version 1.2.6 using Python 3.6.10.final.0
# Namespace http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19 [xmlns:jhs]

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

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19', create_if_missing=True)
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


# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}AlayksikkoNimiTyyppi
class AlayksikkoNimiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'AlayksikkoNimiTyyppi')
    _XSDLocation = None
    _Documentation = None
AlayksikkoNimiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'AlayksikkoNimiTyyppi', AlayksikkoNimiTyyppi)
_module_typeBindings.AlayksikkoNimiTyyppi = AlayksikkoNimiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}AlkuHetkiTyyppi
class AlkuHetkiTyyppi (pyxb.binding.datatypes.dateTime):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'AlkuHetkiTyyppi')
    _XSDLocation = None
    _Documentation = None
AlkuHetkiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'AlkuHetkiTyyppi', AlkuHetkiTyyppi)
_module_typeBindings.AlkuHetkiTyyppi = AlkuHetkiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}AlkuPvmTyyppi
class AlkuPvmTyyppi (pyxb.binding.datatypes.date):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'AlkuPvmTyyppi')
    _XSDLocation = None
    _Documentation = None
AlkuPvmTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'AlkuPvmTyyppi', AlkuPvmTyyppi)
_module_typeBindings.AlkuPvmTyyppi = AlkuPvmTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}AmmattiKoodiTyyppi
class AmmattiKoodiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'AmmattiKoodiTyyppi')
    _XSDLocation = None
    _Documentation = None
AmmattiKoodiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'AmmattiKoodiTyyppi', AmmattiKoodiTyyppi)
_module_typeBindings.AmmattiKoodiTyyppi = AmmattiKoodiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}BICKoodiTyyppi
class BICKoodiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'BICKoodiTyyppi')
    _XSDLocation = None
    _Documentation = None
BICKoodiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'BICKoodiTyyppi', BICKoodiTyyppi)
_module_typeBindings.BICKoodiTyyppi = BICKoodiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}CareOfTekstiTyyppi
class CareOfTekstiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CareOfTekstiTyyppi')
    _XSDLocation = None
    _Documentation = None
CareOfTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'CareOfTekstiTyyppi', CareOfTekstiTyyppi)
_module_typeBindings.CareOfTekstiTyyppi = CareOfTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}EdellinenSukuNimiTyyppi
class EdellinenSukuNimiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'EdellinenSukuNimiTyyppi')
    _XSDLocation = None
    _Documentation = None
EdellinenSukuNimiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'EdellinenSukuNimiTyyppi', EdellinenSukuNimiTyyppi)
_module_typeBindings.EdellinenSukuNimiTyyppi = EdellinenSukuNimiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}EnsimmainenRiviTekstiTyyppi
class EnsimmainenRiviTekstiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'EnsimmainenRiviTekstiTyyppi')
    _XSDLocation = None
    _Documentation = None
EnsimmainenRiviTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'EnsimmainenRiviTekstiTyyppi', EnsimmainenRiviTekstiTyyppi)
_module_typeBindings.EnsimmainenRiviTekstiTyyppi = EnsimmainenRiviTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}EtunimetNimiTyyppi
class EtunimetNimiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'EtunimetNimiTyyppi')
    _XSDLocation = None
    _Documentation = None
EtunimetNimiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'EtunimetNimiTyyppi', EtunimetNimiTyyppi)
_module_typeBindings.EtunimetNimiTyyppi = EtunimetNimiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}EtuNimiTyyppi
class EtuNimiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'EtuNimiTyyppi')
    _XSDLocation = None
    _Documentation = None
EtuNimiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'EtuNimiTyyppi', EtuNimiTyyppi)
_module_typeBindings.EtuNimiTyyppi = EtuNimiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}FaksinumeroTekstiTyyppi
class FaksinumeroTekstiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FaksinumeroTekstiTyyppi')
    _XSDLocation = None
    _Documentation = None
FaksinumeroTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'FaksinumeroTekstiTyyppi', FaksinumeroTekstiTyyppi)
_module_typeBindings.FaksinumeroTekstiTyyppi = FaksinumeroTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}HenkiloTunnusTyyppi
class HenkiloTunnusTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'HenkiloTunnusTyyppi')
    _XSDLocation = None
    _Documentation = None
HenkiloTunnusTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'HenkiloTunnusTyyppi', HenkiloTunnusTyyppi)
_module_typeBindings.HenkiloTunnusTyyppi = HenkiloTunnusTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}HuoltosuhdeTekstiTyyppi
class HuoltosuhdeTekstiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'HuoltosuhdeTekstiTyyppi')
    _XSDLocation = None
    _Documentation = None
HuoltosuhdeTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'HuoltosuhdeTekstiTyyppi', HuoltosuhdeTekstiTyyppi)
_module_typeBindings.HuoltosuhdeTekstiTyyppi = HuoltosuhdeTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}HuoneistotunnisteNumeroTyyppi
class HuoneistotunnisteNumeroTyyppi (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'HuoneistotunnisteNumeroTyyppi')
    _XSDLocation = None
    _Documentation = None
HuoneistotunnisteNumeroTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'HuoneistotunnisteNumeroTyyppi', HuoneistotunnisteNumeroTyyppi)
_module_typeBindings.HuoneistotunnisteNumeroTyyppi = HuoneistotunnisteNumeroTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}HuoneistotunnisteJakokirjainTekstiTyyppi
class HuoneistotunnisteJakokirjainTekstiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'HuoneistotunnisteJakokirjainTekstiTyyppi')
    _XSDLocation = None
    _Documentation = None
HuoneistotunnisteJakokirjainTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'HuoneistotunnisteJakokirjainTekstiTyyppi', HuoneistotunnisteJakokirjainTekstiTyyppi)
_module_typeBindings.HuoneistotunnisteJakokirjainTekstiTyyppi = HuoneistotunnisteJakokirjainTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}HuoneistotunnisteKirjainTekstiTyyppi
class HuoneistotunnisteKirjainTekstiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'HuoneistotunnisteKirjainTekstiTyyppi')
    _XSDLocation = None
    _Documentation = None
HuoneistotunnisteKirjainTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'HuoneistotunnisteKirjainTekstiTyyppi', HuoneistotunnisteKirjainTekstiTyyppi)
_module_typeBindings.HuoneistotunnisteKirjainTekstiTyyppi = HuoneistotunnisteKirjainTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}IBANTunnusTyyppi
class IBANTunnusTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'IBANTunnusTyyppi')
    _XSDLocation = None
    _Documentation = None
IBANTunnusTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'IBANTunnusTyyppi', IBANTunnusTyyppi)
_module_typeBindings.IBANTunnusTyyppi = IBANTunnusTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}IkaluokkaTekstiTyyppi
class IkaluokkaTekstiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'IkaluokkaTekstiTyyppi')
    _XSDLocation = None
    _Documentation = None
IkaluokkaTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'IkaluokkaTekstiTyyppi', IkaluokkaTekstiTyyppi)
_module_typeBindings.IkaluokkaTekstiTyyppi = IkaluokkaTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}KansalaisuusKoodiTyyppi
class KansalaisuusKoodiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'KansalaisuusKoodiTyyppi')
    _XSDLocation = None
    _Documentation = None
KansalaisuusKoodiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'KansalaisuusKoodiTyyppi', KansalaisuusKoodiTyyppi)
_module_typeBindings.KansalaisuusKoodiTyyppi = KansalaisuusKoodiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}KatuNimiTyyppi
class KatuNimiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'KatuNimiTyyppi')
    _XSDLocation = None
    _Documentation = None
KatuNimiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'KatuNimiTyyppi', KatuNimiTyyppi)
_module_typeBindings.KatuNimiTyyppi = KatuNimiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}KieliKoodiTyyppi
class KieliKoodiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'KieliKoodiTyyppi')
    _XSDLocation = None
    _Documentation = None
KieliKoodiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'KieliKoodiTyyppi', KieliKoodiTyyppi)
_module_typeBindings.KieliKoodiTyyppi = KieliKoodiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}KolmasRiviTekstiTyyppi
class KolmasRiviTekstiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'KolmasRiviTekstiTyyppi')
    _XSDLocation = None
    _Documentation = None
KolmasRiviTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'KolmasRiviTekstiTyyppi', KolmasRiviTekstiTyyppi)
_module_typeBindings.KolmasRiviTekstiTyyppi = KolmasRiviTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}KuntaKoodiTyyppi
class KuntaKoodiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'KuntaKoodiTyyppi')
    _XSDLocation = None
    _Documentation = None
KuntaKoodiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'KuntaKoodiTyyppi', KuntaKoodiTyyppi)
_module_typeBindings.KuntaKoodiTyyppi = KuntaKoodiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}KuntaNumeroTyyppi
class KuntaNumeroTyyppi (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'KuntaNumeroTyyppi')
    _XSDLocation = None
    _Documentation = None
KuntaNumeroTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'KuntaNumeroTyyppi', KuntaNumeroTyyppi)
_module_typeBindings.KuntaNumeroTyyppi = KuntaNumeroTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}KuolemaPvmTyyppi
class KuolemaPvmTyyppi (pyxb.binding.datatypes.date):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'KuolemaPvmTyyppi')
    _XSDLocation = None
    _Documentation = None
KuolemaPvmTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'KuolemaPvmTyyppi', KuolemaPvmTyyppi)
_module_typeBindings.KuolemaPvmTyyppi = KuolemaPvmTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}KutsumaNimiTyyppi
class KutsumaNimiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'KutsumaNimiTyyppi')
    _XSDLocation = None
    _Documentation = None
KutsumaNimiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'KutsumaNimiTyyppi', KutsumaNimiTyyppi)
_module_typeBindings.KutsumaNimiTyyppi = KutsumaNimiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}KuudesRiviTekstiTyyppi
class KuudesRiviTekstiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'KuudesRiviTekstiTyyppi')
    _XSDLocation = None
    _Documentation = None
KuudesRiviTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'KuudesRiviTekstiTyyppi', KuudesRiviTekstiTyyppi)
_module_typeBindings.KuudesRiviTekstiTyyppi = KuudesRiviTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}KuvausTekstiTyyppi
class KuvausTekstiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'KuvausTekstiTyyppi')
    _XSDLocation = None
    _Documentation = None
KuvausTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'KuvausTekstiTyyppi', KuvausTekstiTyyppi)
_module_typeBindings.KuvausTekstiTyyppi = KuvausTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}LajiKoodiTyyppi
class LajiKoodiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'LajiKoodiTyyppi')
    _XSDLocation = None
    _Documentation = None
LajiKoodiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'LajiKoodiTyyppi', LajiKoodiTyyppi)
_module_typeBindings.LajiKoodiTyyppi = LajiKoodiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}LajiTekstiTyyppi
class LajiTekstiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'LajiTekstiTyyppi')
    _XSDLocation = None
    _Documentation = None
LajiTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'LajiTekstiTyyppi', LajiTekstiTyyppi)
_module_typeBindings.LajiTekstiTyyppi = LajiTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}LoppuHetkiTyyppi
class LoppuHetkiTyyppi (pyxb.binding.datatypes.dateTime):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'LoppuHetkiTyyppi')
    _XSDLocation = None
    _Documentation = None
LoppuHetkiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'LoppuHetkiTyyppi', LoppuHetkiTyyppi)
_module_typeBindings.LoppuHetkiTyyppi = LoppuHetkiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}LoppuPvmTyyppi
class LoppuPvmTyyppi (pyxb.binding.datatypes.date):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'LoppuPvmTyyppi')
    _XSDLocation = None
    _Documentation = None
LoppuPvmTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'LoppuPvmTyyppi', LoppuPvmTyyppi)
_module_typeBindings.LoppuPvmTyyppi = LoppuPvmTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}MaatunnusKoodiTyyppi
class MaatunnusKoodiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MaatunnusKoodiTyyppi')
    _XSDLocation = None
    _Documentation = None
MaatunnusKoodiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'MaatunnusKoodiTyyppi', MaatunnusKoodiTyyppi)
_module_typeBindings.MaatunnusKoodiTyyppi = MaatunnusKoodiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}NeljasRiviTekstiTyyppi
class NeljasRiviTekstiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'NeljasRiviTekstiTyyppi')
    _XSDLocation = None
    _Documentation = None
NeljasRiviTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'NeljasRiviTekstiTyyppi', NeljasRiviTekstiTyyppi)
_module_typeBindings.NeljasRiviTekstiTyyppi = NeljasRiviTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}NimilajiKoodiTyyppi
class NimilajiKoodiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'NimilajiKoodiTyyppi')
    _XSDLocation = None
    _Documentation = None
NimilajiKoodiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'NimilajiKoodiTyyppi', NimilajiKoodiTyyppi)
_module_typeBindings.NimilajiKoodiTyyppi = NimilajiKoodiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}NimiTyyppi
class NimiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'NimiTyyppi')
    _XSDLocation = None
    _Documentation = None
NimiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'NimiTyyppi', NimiTyyppi)
_module_typeBindings.NimiTyyppi = NimiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}OsoiteNumeroTyyppi
class OsoiteNumeroTyyppi (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'OsoiteNumeroTyyppi')
    _XSDLocation = None
    _Documentation = None
OsoiteNumeroTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'OsoiteNumeroTyyppi', OsoiteNumeroTyyppi)
_module_typeBindings.OsoiteNumeroTyyppi = OsoiteNumeroTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}PaayksikkoNimiTyyppi
class PaayksikkoNimiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PaayksikkoNimiTyyppi')
    _XSDLocation = None
    _Documentation = None
PaayksikkoNimiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'PaayksikkoNimiTyyppi', PaayksikkoNimiTyyppi)
_module_typeBindings.PaayksikkoNimiTyyppi = PaayksikkoNimiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}PankkitiliTunnusTyyppi
class PankkitiliTunnusTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PankkitiliTunnusTyyppi')
    _XSDLocation = None
    _Documentation = None
PankkitiliTunnusTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'PankkitiliTunnusTyyppi', PankkitiliTunnusTyyppi)
_module_typeBindings.PankkitiliTunnusTyyppi = PankkitiliTunnusTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}PostilokerolyhenneTekstiTyyppi
class PostilokerolyhenneTekstiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PostilokerolyhenneTekstiTyyppi')
    _XSDLocation = None
    _Documentation = None
PostilokerolyhenneTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'PostilokerolyhenneTekstiTyyppi', PostilokerolyhenneTekstiTyyppi)
_module_typeBindings.PostilokerolyhenneTekstiTyyppi = PostilokerolyhenneTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}PostilokeroTekstiTyyppi
class PostilokeroTekstiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PostilokeroTekstiTyyppi')
    _XSDLocation = None
    _Documentation = None
PostilokeroTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'PostilokeroTekstiTyyppi', PostilokeroTekstiTyyppi)
_module_typeBindings.PostilokeroTekstiTyyppi = PostilokeroTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}PostinumeroKoodiTyyppi
class PostinumeroKoodiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PostinumeroKoodiTyyppi')
    _XSDLocation = None
    _Documentation = None
PostinumeroKoodiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'PostinumeroKoodiTyyppi', PostinumeroKoodiTyyppi)
_module_typeBindings.PostinumeroKoodiTyyppi = PostinumeroKoodiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}PostitoimipaikkaNimiTyyppi
class PostitoimipaikkaNimiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PostitoimipaikkaNimiTyyppi')
    _XSDLocation = None
    _Documentation = None
PostitoimipaikkaNimiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'PostitoimipaikkaNimiTyyppi', PostitoimipaikkaNimiTyyppi)
_module_typeBindings.PostitoimipaikkaNimiTyyppi = PostitoimipaikkaNimiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}PuhelinnumeroTekstiTyyppi
class PuhelinnumeroTekstiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PuhelinnumeroTekstiTyyppi')
    _XSDLocation = None
    _Documentation = None
PuhelinnumeroTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'PuhelinnumeroTekstiTyyppi', PuhelinnumeroTekstiTyyppi)
_module_typeBindings.PuhelinnumeroTekstiTyyppi = PuhelinnumeroTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}SahkoinenAsiointiTunnusTyyppi
class SahkoinenAsiointiTunnusTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SahkoinenAsiointiTunnusTyyppi')
    _XSDLocation = None
    _Documentation = None
SahkoinenAsiointiTunnusTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'SahkoinenAsiointiTunnusTyyppi', SahkoinenAsiointiTunnusTyyppi)
_module_typeBindings.SahkoinenAsiointiTunnusTyyppi = SahkoinenAsiointiTunnusTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}SahkopostiosoiteTekstiTyyppi
class SahkopostiosoiteTekstiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SahkopostiosoiteTekstiTyyppi')
    _XSDLocation = None
    _Documentation = None
SahkopostiosoiteTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'SahkopostiosoiteTekstiTyyppi', SahkopostiosoiteTekstiTyyppi)
_module_typeBindings.SahkopostiosoiteTekstiTyyppi = SahkopostiosoiteTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}SiviilisaatyTekstiTyyppi
class SiviilisaatyTekstiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SiviilisaatyTekstiTyyppi')
    _XSDLocation = None
    _Documentation = None
SiviilisaatyTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'SiviilisaatyTekstiTyyppi', SiviilisaatyTekstiTyyppi)
_module_typeBindings.SiviilisaatyTekstiTyyppi = SiviilisaatyTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}StatusryhmaTekstiTyyppi
class StatusryhmaTekstiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'StatusryhmaTekstiTyyppi')
    _XSDLocation = None
    _Documentation = None
StatusryhmaTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'StatusryhmaTekstiTyyppi', StatusryhmaTekstiTyyppi)
_module_typeBindings.StatusryhmaTekstiTyyppi = StatusryhmaTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}SukuNimiTyyppi
class SukuNimiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SukuNimiTyyppi')
    _XSDLocation = None
    _Documentation = None
SukuNimiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'SukuNimiTyyppi', SukuNimiTyyppi)
_module_typeBindings.SukuNimiTyyppi = SukuNimiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}SukupuoliKoodiTyyppi
class SukupuoliKoodiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SukupuoliKoodiTyyppi')
    _XSDLocation = None
    _Documentation = None
SukupuoliKoodiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'SukupuoliKoodiTyyppi', SukupuoliKoodiTyyppi)
_module_typeBindings.SukupuoliKoodiTyyppi = SukupuoliKoodiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}SyntymaPvmTyyppi
class SyntymaPvmTyyppi (pyxb.binding.datatypes.date):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SyntymaPvmTyyppi')
    _XSDLocation = None
    _Documentation = None
SyntymaPvmTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'SyntymaPvmTyyppi', SyntymaPvmTyyppi)
_module_typeBindings.SyntymaPvmTyyppi = SyntymaPvmTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}ToinenRiviTekstiTyyppi
class ToinenRiviTekstiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ToinenRiviTekstiTyyppi')
    _XSDLocation = None
    _Documentation = None
ToinenRiviTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'ToinenRiviTekstiTyyppi', ToinenRiviTekstiTyyppi)
_module_typeBindings.ToinenRiviTekstiTyyppi = ToinenRiviTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}TurvakieltoKytkinTyyppi
class TurvakieltoKytkinTyyppi (pyxb.binding.datatypes.boolean):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TurvakieltoKytkinTyyppi')
    _XSDLocation = None
    _Documentation = None
TurvakieltoKytkinTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'TurvakieltoKytkinTyyppi', TurvakieltoKytkinTyyppi)
_module_typeBindings.TurvakieltoKytkinTyyppi = TurvakieltoKytkinTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}UlkomaaHenkiloTunnusTyyppi
class UlkomaaHenkiloTunnusTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'UlkomaaHenkiloTunnusTyyppi')
    _XSDLocation = None
    _Documentation = None
UlkomaaHenkiloTunnusTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'UlkomaaHenkiloTunnusTyyppi', UlkomaaHenkiloTunnusTyyppi)
_module_typeBindings.UlkomaaHenkiloTunnusTyyppi = UlkomaaHenkiloTunnusTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}UlkomaaPostitoimipaikkaNimiTyyppi
class UlkomaaPostitoimipaikkaNimiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'UlkomaaPostitoimipaikkaNimiTyyppi')
    _XSDLocation = None
    _Documentation = None
UlkomaaPostitoimipaikkaNimiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'UlkomaaPostitoimipaikkaNimiTyyppi', UlkomaaPostitoimipaikkaNimiTyyppi)
_module_typeBindings.UlkomaaPostitoimipaikkaNimiTyyppi = UlkomaaPostitoimipaikkaNimiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}VakinainenKytkinTyyppi
class VakinainenKytkinTyyppi (pyxb.binding.datatypes.boolean):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'VakinainenKytkinTyyppi')
    _XSDLocation = None
    _Documentation = None
VakinainenKytkinTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'VakinainenKytkinTyyppi', VakinainenKytkinTyyppi)
_module_typeBindings.VakinainenKytkinTyyppi = VakinainenKytkinTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}ValiaikainenHenkiloTunnusTyyppi
class ValiaikainenHenkiloTunnusTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ValiaikainenHenkiloTunnusTyyppi')
    _XSDLocation = None
    _Documentation = None
ValiaikainenHenkiloTunnusTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'ValiaikainenHenkiloTunnusTyyppi', ValiaikainenHenkiloTunnusTyyppi)
_module_typeBindings.ValiaikainenHenkiloTunnusTyyppi = ValiaikainenHenkiloTunnusTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}ValtiotunnusKoodiTyyppi
class ValtiotunnusKoodiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ValtiotunnusKoodiTyyppi')
    _XSDLocation = None
    _Documentation = None
ValtiotunnusKoodiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'ValtiotunnusKoodiTyyppi', ValtiotunnusKoodiTyyppi)
_module_typeBindings.ValtiotunnusKoodiTyyppi = ValtiotunnusKoodiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}ViidesRiviTekstiTyyppi
class ViidesRiviTekstiTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ViidesRiviTekstiTyyppi')
    _XSDLocation = None
    _Documentation = None
ViidesRiviTekstiTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'ViidesRiviTekstiTyyppi', ViidesRiviTekstiTyyppi)
_module_typeBindings.ViidesRiviTekstiTyyppi = ViidesRiviTekstiTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}VoimassaoloKytkinTyyppi
class VoimassaoloKytkinTyyppi (pyxb.binding.datatypes.boolean):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloKytkinTyyppi')
    _XSDLocation = None
    _Documentation = None
VoimassaoloKytkinTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'VoimassaoloKytkinTyyppi', VoimassaoloKytkinTyyppi)
_module_typeBindings.VoimassaoloKytkinTyyppi = VoimassaoloKytkinTyyppi

# Atomic simple type: {http://skeemat.jhs-suositukset.fi/yhteiset/2009/10/19}YritysTunnusTyyppi
class YritysTunnusTyyppi (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'YritysTunnusTyyppi')
    _XSDLocation = None
    _Documentation = None
YritysTunnusTyyppi._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'YritysTunnusTyyppi', YritysTunnusTyyppi)
_module_typeBindings.YritysTunnusTyyppi = YritysTunnusTyyppi

AlayksikkoNimi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AlayksikkoNimi'), AlayksikkoNimiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', AlayksikkoNimi.name().localName(), AlayksikkoNimi)

AlkuHetki = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AlkuHetki'), AlkuHetkiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', AlkuHetki.name().localName(), AlkuHetki)

AlkuPvm = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AlkuPvm'), AlkuPvmTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', AlkuPvm.name().localName(), AlkuPvm)

AmmattiKoodi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AmmattiKoodi'), AmmattiKoodiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', AmmattiKoodi.name().localName(), AmmattiKoodi)

BICKoodi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'BICKoodi'), BICKoodiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', BICKoodi.name().localName(), BICKoodi)

CareOfTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CareOfTeksti'), CareOfTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', CareOfTeksti.name().localName(), CareOfTeksti)

EdellinenSukuNimi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EdellinenSukuNimi'), EdellinenSukuNimiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', EdellinenSukuNimi.name().localName(), EdellinenSukuNimi)

EnsimmainenRiviTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EnsimmainenRiviTeksti'), EnsimmainenRiviTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', EnsimmainenRiviTeksti.name().localName(), EnsimmainenRiviTeksti)

EtunimetNimi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EtunimetNimi'), EtunimetNimiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', EtunimetNimi.name().localName(), EtunimetNimi)

EtuNimi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EtuNimi'), EtuNimiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', EtuNimi.name().localName(), EtuNimi)

FaksinumeroTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FaksinumeroTeksti'), FaksinumeroTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', FaksinumeroTeksti.name().localName(), FaksinumeroTeksti)

HenkiloTunnus = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HenkiloTunnus'), HenkiloTunnusTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', HenkiloTunnus.name().localName(), HenkiloTunnus)

HuoltosuhdeTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HuoltosuhdeTeksti'), HuoltosuhdeTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', HuoltosuhdeTeksti.name().localName(), HuoltosuhdeTeksti)

HuoneistotunnisteNumero = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HuoneistotunnisteNumero'), HuoneistotunnisteNumeroTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', HuoneistotunnisteNumero.name().localName(), HuoneistotunnisteNumero)

HuoneistotunnisteJakokirjainTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HuoneistotunnisteJakokirjainTeksti'), HuoneistotunnisteJakokirjainTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', HuoneistotunnisteJakokirjainTeksti.name().localName(), HuoneistotunnisteJakokirjainTeksti)

HuoneistotunnisteKirjainTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'HuoneistotunnisteKirjainTeksti'), HuoneistotunnisteKirjainTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', HuoneistotunnisteKirjainTeksti.name().localName(), HuoneistotunnisteKirjainTeksti)

IBANTunnus = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IBANTunnus'), IBANTunnusTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', IBANTunnus.name().localName(), IBANTunnus)

IkaluokkaTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IkaluokkaTeksti'), IkaluokkaTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', IkaluokkaTeksti.name().localName(), IkaluokkaTeksti)

KansalaisuusKoodi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'KansalaisuusKoodi'), KansalaisuusKoodiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', KansalaisuusKoodi.name().localName(), KansalaisuusKoodi)

KatuNimi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'KatuNimi'), KatuNimiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', KatuNimi.name().localName(), KatuNimi)

KieliKoodi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'KieliKoodi'), KieliKoodiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', KieliKoodi.name().localName(), KieliKoodi)

KolmasRiviTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'KolmasRiviTeksti'), KolmasRiviTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', KolmasRiviTeksti.name().localName(), KolmasRiviTeksti)

KuntaKoodi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'KuntaKoodi'), KuntaKoodiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', KuntaKoodi.name().localName(), KuntaKoodi)

KuntaNumero = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'KuntaNumero'), KuntaNumeroTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', KuntaNumero.name().localName(), KuntaNumero)

KuolemaPvm = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'KuolemaPvm'), KuolemaPvmTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', KuolemaPvm.name().localName(), KuolemaPvm)

KutsumaNimi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'KutsumaNimi'), KutsumaNimiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', KutsumaNimi.name().localName(), KutsumaNimi)

KuudesRiviTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'KuudesRiviTeksti'), KuudesRiviTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', KuudesRiviTeksti.name().localName(), KuudesRiviTeksti)

KuvausTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'KuvausTeksti'), KuvausTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', KuvausTeksti.name().localName(), KuvausTeksti)

LajiKoodi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LajiKoodi'), LajiKoodiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', LajiKoodi.name().localName(), LajiKoodi)

LajiTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LajiTeksti'), LajiTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', LajiTeksti.name().localName(), LajiTeksti)

LoppuHetki = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LoppuHetki'), LoppuHetkiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', LoppuHetki.name().localName(), LoppuHetki)

LoppuPvm = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LoppuPvm'), LoppuPvmTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', LoppuPvm.name().localName(), LoppuPvm)

MaatunnusKoodi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MaatunnusKoodi'), MaatunnusKoodiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', MaatunnusKoodi.name().localName(), MaatunnusKoodi)

NeljasRiviTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NeljasRiviTeksti'), NeljasRiviTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', NeljasRiviTeksti.name().localName(), NeljasRiviTeksti)

NimilajiKoodi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'NimilajiKoodi'), NimilajiKoodiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', NimilajiKoodi.name().localName(), NimilajiKoodi)

Nimi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Nimi'), NimiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', Nimi.name().localName(), Nimi)

OsoiteNumero = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'OsoiteNumero'), OsoiteNumeroTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', OsoiteNumero.name().localName(), OsoiteNumero)

PaayksikkoNimi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PaayksikkoNimi'), PaayksikkoNimiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', PaayksikkoNimi.name().localName(), PaayksikkoNimi)

PankkitiliTunnus = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PankkitiliTunnus'), PankkitiliTunnusTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', PankkitiliTunnus.name().localName(), PankkitiliTunnus)

PostilokerolyhenneTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PostilokerolyhenneTeksti'), PostilokerolyhenneTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', PostilokerolyhenneTeksti.name().localName(), PostilokerolyhenneTeksti)

PostilokeroTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PostilokeroTeksti'), PostilokeroTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', PostilokeroTeksti.name().localName(), PostilokeroTeksti)

PostinumeroKoodi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PostinumeroKoodi'), PostinumeroKoodiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', PostinumeroKoodi.name().localName(), PostinumeroKoodi)

PostitoimipaikkaNimi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PostitoimipaikkaNimi'), PostitoimipaikkaNimiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', PostitoimipaikkaNimi.name().localName(), PostitoimipaikkaNimi)

PuhelinnumeroTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PuhelinnumeroTeksti'), PuhelinnumeroTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', PuhelinnumeroTeksti.name().localName(), PuhelinnumeroTeksti)

SahkoinenAsiointiTunnus = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SahkoinenAsiointiTunnus'), SahkoinenAsiointiTunnusTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', SahkoinenAsiointiTunnus.name().localName(), SahkoinenAsiointiTunnus)

SahkopostiosoiteTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SahkopostiosoiteTeksti'), SahkopostiosoiteTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', SahkopostiosoiteTeksti.name().localName(), SahkopostiosoiteTeksti)

SiviilisaatyTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SiviilisaatyTeksti'), SiviilisaatyTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', SiviilisaatyTeksti.name().localName(), SiviilisaatyTeksti)

StatusryhmaTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'StatusryhmaTeksti'), StatusryhmaTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', StatusryhmaTeksti.name().localName(), StatusryhmaTeksti)

SukuNimi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SukuNimi'), SukuNimiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', SukuNimi.name().localName(), SukuNimi)

SukupuoliKoodi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SukupuoliKoodi'), SukupuoliKoodiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', SukupuoliKoodi.name().localName(), SukupuoliKoodi)

SyntymaPvm = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'SyntymaPvm'), SyntymaPvmTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', SyntymaPvm.name().localName(), SyntymaPvm)

ToinenRiviTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ToinenRiviTeksti'), ToinenRiviTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', ToinenRiviTeksti.name().localName(), ToinenRiviTeksti)

TurvakieltoKytkin = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TurvakieltoKytkin'), TurvakieltoKytkinTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', TurvakieltoKytkin.name().localName(), TurvakieltoKytkin)

UlkomaaHenkiloTunnus = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'UlkomaaHenkiloTunnus'), UlkomaaHenkiloTunnusTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', UlkomaaHenkiloTunnus.name().localName(), UlkomaaHenkiloTunnus)

UlkomaaPostitoimipaikkaNimi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'UlkomaaPostitoimipaikkaNimi'), UlkomaaPostitoimipaikkaNimiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', UlkomaaPostitoimipaikkaNimi.name().localName(), UlkomaaPostitoimipaikkaNimi)

VakinainenKytkin = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'VakinainenKytkin'), VakinainenKytkinTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', VakinainenKytkin.name().localName(), VakinainenKytkin)

ValiaikainenHenkiloTunnus = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ValiaikainenHenkiloTunnus'), ValiaikainenHenkiloTunnusTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', ValiaikainenHenkiloTunnus.name().localName(), ValiaikainenHenkiloTunnus)

ValtiotunnusKoodi = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ValtiotunnusKoodi'), ValtiotunnusKoodiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', ValtiotunnusKoodi.name().localName(), ValtiotunnusKoodi)

ViidesRiviTeksti = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ViidesRiviTeksti'), ViidesRiviTekstiTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', ViidesRiviTeksti.name().localName(), ViidesRiviTeksti)

VoimassaoloKytkin = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'VoimassaoloKytkin'), VoimassaoloKytkinTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', VoimassaoloKytkin.name().localName(), VoimassaoloKytkin)

YritysTunnus = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'YritysTunnus'), YritysTunnusTyyppi, location=None)
Namespace.addCategoryObject('elementBinding', YritysTunnus.name().localName(), YritysTunnus)
