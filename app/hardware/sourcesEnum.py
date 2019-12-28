from enum import Enum, auto

class sourcesEnum(Enum):
    MASHTUN_INLET       = auto()
    MASHTUN_OUTLET      = auto()

    BOILKETTLE_INLET    = auto()
    BOILKETTLE_WATER    = auto()
    BOILKETTLE_RETURN   = auto()
    BOILKETTLE_OUTLET   = auto()

    CHILLER_WATER       = auto()
    CHILLER_WORT        = auto()

    DUMP                = auto()
