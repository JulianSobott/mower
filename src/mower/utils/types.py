"""
:module: mower.utils.types
:synopsis: Some common type definitions usinf the typing module
:author: Julian Sobott
:author: 


"""
from typing import Tuple, List, NewType

from mower.utils import Length


"""Points"""
#: x, y
Point = Tuple[int, int]
#: 0 = x, 1 = y
PointL = List[Length]


"""Direction 4D"""
Direction_4D = NewType("Direction_4D", str)

NORTH = Direction_4D("NORTH")
EAST = Direction_4D("EAST")
SOUTH = Direction_4D("SOUTH")
WEST = Direction_4D("WEST")


"""Direction 2D"""
Direction_2D = NewType("Direction_2D", str)

DIRECTION_FORWARD = Direction_2D("FORWARD")
DIRECTION_BACKWARD = Direction_2D("BACKWARD")


"""Side"""
Side = NewType("Side", str)

LEFT_SIDE = Side("LEFT")
RIGHT_SIDE = Side("RIGHT")
