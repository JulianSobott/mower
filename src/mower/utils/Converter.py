"""
@author: Julian
@brief: Functions to convert measure units
@description:
1px = 1cm = 0.01m
"""
from typing import Union

from mower.utils.Logging import logger


PX2M_DIVIDER = 10


class Length(object):

    METER = (0, "meter", "m")
    PIXEL = (1, "pixel", "px")
    CENTIMETER = (2, "centimeter", "cm")

    def __init__(self, distance: Union[int, float], unit):
        self.length: Union[int, float] = distance
        if not(type(unit) == tuple and len(unit) == 3):
            logger.error("Enter valid length unit: (METER, PIXEL, CENTIMETER)")
            return
        if not(self.METER[0] <= unit[0] <= self.CENTIMETER[0]):
            logger.error("Enter valid length unit: (METER, PIXEL, CENTIMETER)")
            return
        self.unit = unit

    def int_val(self):
        return int(self.length)

    def meter(self) -> float:
        if self.unit == self.METER:
            return self.length
        if self.unit == self.PIXEL:
            return self.length / PX2M_DIVIDER
        if self.unit == self.CENTIMETER:
            return self.length / 100

    def pixel(self) -> int:
        if self.unit == self.METER:
            return int(self.length * PX2M_DIVIDER)
        if self.unit == self.PIXEL:
            return int(self.length)
        if self.unit == self.CENTIMETER:
            return int((self.length * PX2M_DIVIDER) / 100)

    def centimeter(self) -> float:
        if self.unit == self.METER:
            return self.length * 100
        if self.unit == self.PIXEL:
            return (self.length * PX2M_DIVIDER) / 100
        if self.unit == self.CENTIMETER:
            return self.length

    def get_distance(self, unit) -> float:
        if unit == self.METER:
            return self.meter()
        if unit == self.PIXEL:
            return self.pixel()
        if unit == self.CENTIMETER:
            return self.centimeter()

    def get_instance(self):
        return self

    def __add__(self, other):
        other_dis = Length.get_other_distance(other, self.unit)
        return Length(other_dis + self.length, self.unit)

    def __iadd__(self, other):
        self.length += Length.get_other_distance(other, self.unit)
        return self

    def __radd__(self, other):
        return Length.__add__(self, other)

    def __sub__(self, other):
        other_dis = Length.get_other_distance(other, self.unit)
        return Length(self.length - other_dis, self.unit)

    def __isub__(self, other):
        self.length -= Length.get_other_distance(other, self.unit)
        return self

    def __rsub__(self, other):
        return Length.__sub__(self, other)

    def __mul__(self, other):
        other_dis = Length.get_other_distance(other, self.unit)
        return Length(other_dis * self.length, self.unit)

    def __imul__(self, other):
        self.length *= Length.get_other_distance(other, self.unit)
        return self

    def __rmul__(self, other):
        return Length.__mul__(self, other)

    def __truediv__(self, other):
        other_dis = Length.get_other_distance(other, self.unit)
        return Length(self.length / other_dis, self.unit)

    def __itruediv__(self, other):
        self.length /= Length.get_other_distance(other, self.unit)
        return self

    def __rtruediv__(self, other):
        return Length.__truediv__(self, other)

    def __mod__(self, other):
        other_dis = Length.get_other_distance(other, self.unit)
        return Length(self.length % other_dis, self.unit)

    def __imod__(self, other):
        self.length %= Length.get_other_distance(other, self.unit)
        return self

    def __rmod__(self, other):
        return Length.__mod__(self, other)

    def __pow__(self, power, modulo=None):
        return Length(self.length**power, self.unit)

    def __neg__(self):
        return Length(-self.length, self.unit)

    def __abs__(self):
        if self.length >= 0:
            return Length(self.length, self.unit)
        else:
            return Length(-self.length, self.unit)

    def __lt__(self, other):
        if self.__sub__(abs(other)).length < 0:
            return True
        else:
            return False

    def __le__(self, other):
        if self.__sub__(abs(other)).length <= 0:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.__sub__(abs(other)).length > 0:
            return True
        else:
            return False

    def __ge__(self, other):
        if self.__sub__(abs(other)).length >= 0:
            return True
        else:
            return False

    def __eq__(self, other):
        if self.__sub__(abs(other)).length == 0:
            return True
        else:
            return False

    def __ne__(self, other):
        if self.__sub__(abs(other)).length != 0:
            return True
        else:
            return False

    def __repr__(self):
        return str(self.length) + self.unit[2]

    @staticmethod
    def get_other_distance(other, unit):
        if isinstance(other, Length):
            return other.get_distance(unit)
        else:
            # logger.warning("Length was implicit converted! Consider converting explicit to Length")
            return other

