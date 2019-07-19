"""
:module: mower.utils.types
:synopsis: Some common type definitions usinf the typing module
:author: Julian Sobott
:author: 


"""
from typing import Tuple, List, NewType

from mower.utils import Length

#: x, y
Point = Tuple[int, int]
#: 0 = x, 1 = y
PointL = List[Length]

Direction = NewType("Direction", str)

NORTH = Direction("NORTH")
EAST = Direction("EAST")
SOUTH = Direction("SOUTH")
WEST = Direction("WEST")

MotorDirection = NewType("MotorDirection", str)

MOTOR_DIRECTION_FORWARD = MotorDirection("FORWARD")
MOTOR_DIRECTION_BACKWARD = MotorDirection("BACKWARD")
