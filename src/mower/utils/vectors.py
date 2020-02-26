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


def point_distance(p1: types.Point, p2: types.Point):
    return math.sqrt(((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2))
