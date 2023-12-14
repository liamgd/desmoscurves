import enum


class ClickType(enum.Enum):
    MOUSE = 1
    REMOVE = 2
    GHOST = 3
    SHARP = 4
    ADD = 5


class PointType(enum.Enum):
    REVERSE_HANDLE = 1
    POINT = 2
    HANDLE = 3
