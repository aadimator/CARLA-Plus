import gin
from enum import Enum, auto

@gin.constants_from_enum
class Rain(Enum):
    NO = auto()
    LIGHT = auto()
    HEAVY = auto()

@gin.constants_from_enum
class DayTime(Enum):
    NIGHT = auto()
    DAWN = auto()
    DAY = auto()
    DUSK = auto()

@gin.constants_from_enum
class TrafficVolume(Enum):
    LOW = auto()
    HIGH = auto()

@gin.constants_from_enum
class VehicleSpeed(Enum):
    VERY_SLOW = auto()
    SLOW = auto()
    MEDIUM = auto()
    FAST = auto()
    VERY_FAST = auto()