from enum import Enum, IntEnum


class TodoState(IntEnum, Enum):
    BEFORE_PROCESS = 1
    ON_PROGRESS = 2
    COMPLETE = 3
