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

from mower.utils.vectors import point_distance, Vec2
from mower.utils.polygons import Polygon, Node
from mower.utils.Logging import logger


class Map:
    """
    The map stores data for each cell. It is build up from :class:`mower.core.map_utils.Quad` 's.
    """

    def __init__(self):
        self.paths: List['Polygon'] = []
        self.current_path: 'Polygon' = None
        self._current_rect: List[Node] = [None] * 4
        self._current_rect_origin: Vec2 = None

    def debug_add_rect(self, x, y, width, height):
        path = Polygon()
        path.add_position(Vec2(x, y))
        path.add_position(Vec2(x + width, y))
        path.add_position(Vec2(x + width, y + height))
        path.add_position(Vec2(x, y + height))
        self.paths.append(path)

    def begin_dynamic_rect(self, x, y):
        path = Polygon()
        for i in range(4):
            self._current_rect[i] = path.add_position(Vec2(x, y))
        self.paths.append(path)
        self.current_path = path
        self._current_rect_origin = Vec2(x, y)

    def update_dynamic_rect(self, x, y):
        if x > self._current_rect_origin.x:
            x0 = self._current_rect_origin.x
            w = x - self._current_rect_origin.x
        else:
            x0 = x
            w = self._current_rect_origin.x - x
        if y > self._current_rect_origin.y:
            y0 = self._current_rect_origin.y
            h = y - self._current_rect_origin.y
        else:
            y0 = y
            h = self._current_rect_origin.y - y
        self._current_rect[0].pos = Vec2(x0, y0)
        self._current_rect[1].pos = Vec2(x0 + w, y0)
        self._current_rect[2].pos = Vec2(x0 + w, y0 + h)
        self._current_rect[3].pos = Vec2(x0, y0 + h)

    def begin_new_path(self):
        self.current_path = Polygon()
        self.paths.append(self.current_path)

    def end_new_path(self):
        # TODO: Handle holes
        if len(self.paths) >= 2:
            new_paths_queue = [self.current_path]
            final_new_paths = []
            for path in self.paths:
                path_is_disjoint = True
                processed_new_paths = []
                while len(new_paths_queue) > 0:
                    new_path = new_paths_queue.pop()
                    if new_path is not path:
                        res = new_path.union(path)
                        if res[1] == Polygon.RET_UNION:
                            processed_new_paths += res[0]
                            path_is_disjoint = False
                        elif res[1] == Polygon.RET_DISJOINT:
                            processed_new_paths.append(new_path)
                        elif res[1] == Polygon.RET_SELF:       # existing path in new path
                            processed_new_paths.append(new_path)
                            path_is_disjoint = False
                        elif res[1] == Polygon.RET_CLIP:   # new path in existing path
                            pass    # new path no longer needed
                new_paths_queue = processed_new_paths
                if path_is_disjoint:
                    final_new_paths.append(path)
            final_new_paths += new_paths_queue
            self.paths = final_new_paths

    def add_point(self, x, y, min_delta=10):
        if self.current_path.end() is None or point_distance(Vec2(x, y), self.current_path.end().pos) > min_delta:
            self.paths[-1].add_position(Vec2(x, y))

    def update(self, passed_time: Union[float, int]):
        pass

    def reset(self):
        self.__init__()
