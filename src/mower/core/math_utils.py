"""
:module: mower.
:synopsis:
:author: Julian Sobott
:author: 

public functions
-----------------

.. autofunction:: XXX

public classes
-----------------

.. autoclass:: XXX
    :members:


private functions
------------------

.. autofunction:: XXX

private classes
-----------------

.. autoclass:: XXX
    :members:

"""
import math

from mower.utils import types


def rotate_point(ref_point: types.Point, angle: int, point: types.Point) -> types.Point:
    """Rotate point around ref_point with angle measured in degree"""
    theta = math.radians(angle)
    return (round(math.cos(theta) * (point[0] - ref_point[0]) - math.sin(theta) * (point[1] - ref_point[1]) +
            ref_point[0]),
            round(math.sin(theta) * (point[0] - ref_point[0]) + math.cos(theta) * (point[1] - ref_point[1]) +
            ref_point[1]))
