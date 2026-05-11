from enum import Enum


class OwgrTour(Enum):
    """
    Tour identifiers mapping to the OWGR API's numeric tourId values.
    The enum value is the tourId used in API requests.
    """
    ALL = 0
    AsianDevelopmentTour = 1
    SunshineTour = 2
    AlpsTour = 3
    PGATourAustralasia = 4
    AsianTour = 5
    AllThailandGolfTour = 6
    ACNTour = 7
    BigEasyTour = 8
    PGATourCanada = 9
    HotelPlannerTour = 10
    ChinaTour = 11
    ChinaTourPGATourSeries = 12
    DPWorldTour = 13
    EuroProTour = 14
    JapanGolfTour = 15
    KornFerryTour = 16
    KPGATour = 17
    MajorChampionships = 18
    MENAGolfTour = 19
    NordicGolfLeague = 20
    OlympicGolfCompetition = 21
    OneAsia = 22
    PGATour = 23
    ProGolfTour = 24
    PGTIndia = 25
    PGATourSeriesChina = 26
    PGATourLatinoAmerica = 27
    WGC = 28
    MastersTournament = 29
    PGAChampionship = 30
    USOpen = 31
    TheOpen = 32
    GiraMexicana = 36
    PGATourAmericas = 37
    ClutchProTour = 39
    TartanProTour = 40
    PGATourTaiwan = 41
    LIVGolf = 42


# Map legacy tour codes (used by the old OWGR site) to OwgrTour enum values.
LEGACY_TOUR_CODE_MAP = {
    "ADT": OwgrTour.AsianDevelopmentTour,
    "Afr": OwgrTour.SunshineTour,
    "ALP": OwgrTour.AlpsTour,
    "ANZ": OwgrTour.PGATourAustralasia,
    "Asa": OwgrTour.AsianTour,
    "BET": OwgrTour.BigEasyTour,
    "Can": OwgrTour.PGATourCanada,
    "Cha": OwgrTour.DPWorldTour,
    "CHN": OwgrTour.ChinaTour,
    "CTPTC": OwgrTour.ChinaTourPGATourSeries,
    "EPT": OwgrTour.EuroProTour,
    "Eur": OwgrTour.DPWorldTour,
    "Jpn": OwgrTour.JapanGolfTour,
    "Kor": OwgrTour.KPGATour,
    "Maj": OwgrTour.MajorChampionships,
    "MGT": OwgrTour.MENAGolfTour,
    "NGL": OwgrTour.NordicGolfLeague,
    "OGC": OwgrTour.OlympicGolfCompetition,
    "One": OwgrTour.OneAsia,
    "PGAT": OwgrTour.PGATour,
    "PGT": OwgrTour.ProGolfTour,
    "PTSC": OwgrTour.PGATourSeriesChina,
    "SAm": OwgrTour.PGATourLatinoAmerica,
    "US": OwgrTour.PGATour,
    "Web": OwgrTour.KornFerryTour,
    "WGC": OwgrTour.WGC,
}
