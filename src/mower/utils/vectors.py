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


class Vec2:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, Vec2) and self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


def point_distance(p1: Vec2, p2: Vec2):
    return math.sqrt(((p1.x-p2.x)**2 + (p1.y-p2.y)**2))


def intersect(s1: Vec2, s2: Vec2, c1: Vec2, c2: Vec2):
    """Test the intersection between two lines (two pairs of coordinates for two points).
    Return the coordinates for the intersection and the subject and clipper alphas if the test passes.
    Algorithm based on: http://paulbourke.net/geometry/lineline2d/
    """
    den = (c2.y - c1.y) * (s2.x - s1.x) - (c2.x - c1.x) * (s2.y - s1.y)

    if not den:
        return None

    us = ((c2.x - c1.x) * (s1.y - c1.y) - (c2.y - c1.y) * (s1.x - c1.x)) / den
    uc = ((s2.x - s1.x) * (s1.y - c1.y) - (s2.y - s1.y) * (s1.x - c1.x)) / den

    if (us == 0 or us == 1) and (0 <= uc <= 1) or\
       (uc == 0 or uc == 1) and (0 <= us <= 1):
        return None     # degenerate

    elif (0 < us < 1) and (0 < uc < 1):
        x = s1.x + us * (s2.x - s1.x)
        y = s1.y + us * (s2.y - s1.y)
        return Vec2(x, y), us, uc

    return None
