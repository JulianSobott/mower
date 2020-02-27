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
from mower.utils.types import Underground, Grass, Unknown, Obstacle
from mower.utils.polygons import Polygon, Node
from mower.utils.Logging import logger


class Map:
    """
    The map stores data for each cell. It is build up from :class:`mower.core.map_utils.Quad` 's.
    """

    def __init__(self):
        self.areas: List['Area'] = []
        self.current_area: 'Area' = None
        self._current_rect: List[Node] = [None] * 4
        self._current_rect_origin: Vec2 = None

    def debug_add_rect(self, x, y, width, height):
        path = Polygon()
        path.add_position(Vec2(x, y))
        path.add_position(Vec2(x + width, y))
        path.add_position(Vec2(x + width, y + height))
        path.add_position(Vec2(x, y + height))
        self.paths.append(path)

    def begin_dynamic_rect(self, x, y, underground):
        poly = Polygon()
        for i in range(4):
            self._current_rect[i] = poly.add_position(Vec2(x, y))
        area = Area(underground, poly)
        self._current_rect_origin = Vec2(x, y)
        self.current_area = area
        self.areas.append(area)

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

    def begin_new_area(self, underground: Underground):
        self.current_area = Area(underground, Polygon())
        self.areas.append(self.current_area)

    def end_new_path(self):
        # TODO: Handle holes
        if len(self.areas) >= 2:
            new_areas_queue = [self.current_area]
            final_new_areas = []
            for area in self.areas:
                area_is_disjoint = True
                processed_new_areas = []
                while len(new_areas_queue) > 0:
                    new_area = new_areas_queue.pop()
                    if new_area is not area:
                        res = new_area.polygon.union(area.polygon)
                        if res[1] == Polygon.RET_UNION:
                            processed_new_areas += map(lambda poly: Area(new_area.underground, poly), res[0])
                            # TODO: proper underground
                            area_is_disjoint = False
                        elif res[1] == Polygon.RET_DISJOINT:
                            processed_new_areas.append(new_area)
                        elif res[1] == Polygon.RET_SELF:       # existing path in new path
                            processed_new_areas.append(new_area)
                            area_is_disjoint = False
                        elif res[1] == Polygon.RET_CLIP:   # new path in existing path
                            pass    # new path no longer needed
                new_areas_queue = processed_new_areas
                if area_is_disjoint:
                    final_new_areas.append(area)
            final_new_areas += new_areas_queue
            self.areas = final_new_areas

    def add_point_to_area(self, x, y, min_delta=10):
        if self.current_area.polygon.end() is None or \
                point_distance(Vec2(x, y), self.current_area.polygon.end().pos) > min_delta:
            self.paths[-1].add_position(Vec2(x, y))

    def update(self, passed_time: Union[float, int]):
        pass

    def reset(self):
        self.__init__()


class Area:

    def __init__(self, underground: Underground, polygon: Polygon):
        self.underground = underground
        self.polygon = polygon
