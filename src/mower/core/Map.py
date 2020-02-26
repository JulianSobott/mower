"""
:module: mower.core.Map
:synopsis: A map can store the data of all cells
:author: Julian Sobott
:author:

public classes
----------------------

.. autoclass:: Map
    :members:

"""
from typing import Union, List

from mower.utils.vectors import point_distance
from mower.utils.Logging import logger


class Map:
    """
    The map stores data for each cell. It is build up from :class:`mower.core.map_utils.Quad` 's.
    """

    def __init__(self):
        self.paths: List['Path'] = []
        self.current_path: 'Path' = None
        self._current_rect: List[Node] = [None] * 4

    def debug_add_rect(self, x, y, width, height):
        path = Path()
        path.add_position((x, y))
        path.add_position((x + width, y))
        path.add_position((x + width, y + height))
        path.add_position((x, y + height))
        self.paths.append(path)

    def begin_dynamic_rect(self, x, y):
        path = Path()
        for i in range(4):
            self._current_rect[i] = path.add_position((x, y))
        self.paths.append(path)
        self.current_path = path

    def update_dynamic_rect(self, x, y):
        x0, y0 = self._current_rect[0].pos
        self._current_rect[1].pos = x0, y
        self._current_rect[2].pos = x, y
        self._current_rect[3].pos = x, y0

    def begin_new_path(self):
        self.current_path = Path()
        self.paths.append(self.current_path)

    def end_new_path(self):
        pass    # TODO: union with overlapping paths

    def add_point(self, x, y, min_delta=10):
        if self.current_path.end() is None or point_distance((x, y), self.current_path.end().pos) > min_delta:
            self.paths[-1].add_position((x, y))

    def update(self, passed_time: Union[float, int]):
        pass

    def reset(self):
        self.__init__()


class Path:

    def __init__(self):
        self.begin = None
        self.last = None
        self._current = None

    def add_position(self, position):
        node = Node(position, None, None)
        if self.begin is None:
            self.begin = node
            self.begin.successor = node
            self.begin.predecessor = node
            self._current = self.begin
        else:
            self.begin.predecessor.successor = node
            node.successor = self.begin
            node.predecessor = self.begin.predecessor
            self.begin.predecessor = node
        return node

    def end(self):
        return self.begin.predecessor if self.begin else None

    def __iter__(self):
        yield self._current
        self._current = self._current.successor
        while self._current is not self.begin:
            yield self._current
            self._current = self._current.successor

    def __next__(self):
        self._current = self._current.successor
        return self._current


class Node:

    def __init__(self, pos, predecessor, successor):
        self.pos = pos
        self.predecessor = predecessor
        self.successor = successor

    def __repr__(self):
        return f"Node(pos={self.pos}, predecessor={id(self.predecessor)}, successor={id(self.successor)})"
