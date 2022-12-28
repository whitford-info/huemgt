from enum import Enum

__all__ = ["LightTypeEnum"]


class LightTypeEnum(str, Enum):
    """ """

    ecl = "Extended color light"
    plug = "On/Off plug-in unit"
