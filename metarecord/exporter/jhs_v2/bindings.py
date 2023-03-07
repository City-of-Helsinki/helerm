from lxml import objectify

JHS_NAMESPACE = "http://skeemat.jhs-suositukset.fi/tos/2015/01/15"

E = objectify.ElementMaker(
    annotate=False,
    namespace=JHS_NAMESPACE,
    nsmap={"tos": JHS_NAMESPACE},
)

TOS_PREFIX = f"{{{JHS_NAMESPACE}}}"


def tos_attr(name):
    """Shorthand for a TOS namespace attribute name."""
    return f"{TOS_PREFIX}{name}"


def create_wrapped_element(element):
    """
    Wrap an element with some magic to prefix all attributes with the TOS
    namespace prefix.
    """

    def wrapper(*children, **attrs):
        prefixed_attrs = {
            tos_attr(key): value
            for key, value in attrs.items()
            if not key.startswith("{")
        }
        return element(*children, **prefixed_attrs)

    return wrapper


# Wrapped elements
TOS = create_wrapped_element(E.Tos)
TOS_TIEDOT = create_wrapped_element(E.TosTiedot)
LUOKKA = create_wrapped_element(E.Luokka)
LAAJENNOS = create_wrapped_element(E.Laajennos)
NIMEKE = create_wrapped_element(E.Nimeke)
NIMEKE_KIELELLA = create_wrapped_element(E.NimekeKielella)
NIMEKE_TEKSTI = create_wrapped_element(E.NimekeTeksti)
ORGANISAATIO_NIMI = create_wrapped_element(E.OrganisaatioNimi)
YHTEYSHENKILO_NIMI = create_wrapped_element(E.YhteyshenkiloNimi)
LISATIEDOT = create_wrapped_element(E.LisatiedotTeksti)
TILA_KOODI = create_wrapped_element(E.TilaKoodi)
TOS_VERSIO = create_wrapped_element(E.TosVersio)
LUOKITUSTUNNUS = create_wrapped_element(E.Luokitustunnus)
LUOKITUSVASTUU = create_wrapped_element(E.Luokitusvastuu)
KASITTELYPROSESSI_TIEDOT = create_wrapped_element(E.KasittelyprosessiTiedot)
TIETOJARJESTELMA_NIMI = create_wrapped_element(E.TietojarjestelmaNimi)
TOIMENPIDETIEDOT = create_wrapped_element(E.Toimenpidetiedot)
TOIMENPIDELUOKKA_TEKSTI = create_wrapped_element(E.ToimenpideluokkaTeksti)
TOIMENPIDELUOKKA_TARKENNE_TEKSTI = create_wrapped_element(
    E.ToimenpideluokkaTarkenneTeksti
)
KAYTTORAJOITUSTIEDOT = create_wrapped_element(E.Kayttorajoitustiedot)
JULKISUUSLUOKKA_KOODI = create_wrapped_element(E.JulkisuusluokkaKoodi)
HENKILOTIETOLUONNE_KOODI = create_wrapped_element(E.HenkilotietoluonneKoodi)
SALASSAPITO_AIKA_ARVO = create_wrapped_element(E.SalassapitoAikaArvo)
SALASSAPITO_PERUSTE_TEKSTI = create_wrapped_element(E.SalassapitoPerusteTeksti)
SALASSAPIDON_LASKENTAPERUSTE_TEKSTI = create_wrapped_element(
    E.SalassapidonLaskentaperusteTeksti
)
SAILYTYSAIKATIEDOT = create_wrapped_element(E.Sailytysaikatiedot)
SAILYTYSAJAN_PITUUS_ARVO = create_wrapped_element(E.SailytysajanPituusArvo)
SAILYTYSAJAN_PERUSTE_TEKSTI = create_wrapped_element(E.SailytysajanPerusteTeksti)
SAILYTYSAJAN_LASKENTAPERUSTE_TEKSTI = create_wrapped_element(
    E.SailytysajanLaskentaperusteTeksti
)
ASIAKIRJATIETO = create_wrapped_element(E.Asiakirjatieto)
ASIAKIRJALUOKKA_TEKSTI = create_wrapped_element(E.AsiakirjaluokkaTeksti)
ASIAKIRJALUOKKA_TARKENNE_TEKSTI = create_wrapped_element(
    E.AsiakirjaluokkaTarkenneTeksti
)
