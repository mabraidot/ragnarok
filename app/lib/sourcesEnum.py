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

class waterActionsEnum(Enum):
    BUSY                = auto()
    FINISHED            = auto()
    WATER_IN            = auto()
    WATER_IN_FILTERED   = auto()
    MASHTUN_TO_KETTLE   = auto()
    KETTLE_TO_MASHTUN   = auto()
    MASHTUN_TO_DUMP     = auto()
    KETTLE_TO_DUMP      = auto()
    KETTLE_TO_CHILLER   = auto()
    MASHTUN_TO_MASHTUN  = auto()
    KETTLE_TO_KETTLE    = auto()
    CHILL               = auto()
    DUMP                = auto()


class soundsEnum(Enum):
    ALARM               = auto()
    WELCOME             = auto()
    GOODBYE             = auto()
    SUCCESS             = auto()

class valveActions(Enum):
    CLOSE               = auto()
    OPEN                = auto()

class cleaningProgramsActions(Enum):
    SHORT               = auto()
    SANITIZATION        = auto()
    FULL                = auto()

class cookingStates(Enum):
    PENDING             = auto()
    PREHEATING          = auto()
    RUNNING             = auto()
    RACKING             = auto()
    DUMPING             = auto()
    FINISHED            = auto()
