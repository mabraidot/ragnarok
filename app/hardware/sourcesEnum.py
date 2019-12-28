from enum import Enum, auto

class sourcesEnum(Enum):
    INLET_FILTERED  = auto()
    INLET           = auto()
    MASHTUN         = auto()
    BOILKETTLE      = auto()
    CHILLER_WORT    = auto()
    CHILLER_WATER   = auto()
    OUTLET          = auto()