"""
:module: mower.utils.polygons
:synopsis: Polygon classes
:author: Julian Sobott

public classes
-----------------

.. autoclass:: Polygon
    :members:


private functions
------------------

.. autofunction:: XXX

private classes
-----------------

.. autoclass:: XXX
    :members:

"""

from mower.utils.vectors import Vec2, intersect


class Polygon:

    RET_SELF = "self"
    RET_CLIP = "clip"
    RET_DISJOINT = "disjoint"
    RET_UNION = "union"

    def __init__(self):
        self.begin: Node = None
        self._current: Node = None

    def add(self, node: 'Node'):
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

    def add_position(self, position: Vec2):
        node = Node(position)
        return self.add(node)

    def end(self):
        return self.begin.predecessor if self.begin else None

    def insert(self, node, start, end):
        curr = start
        while curr != end and curr.alpha < node.alpha:
            curr = curr.successor

        node.successor = curr
        node.predecessor = curr.predecessor
        curr.predecessor.successor = node
        curr.predecessor = node

    def find(self, pos: Vec2, start: 'Node'):
        s = start
        while s.pos != pos:
            s = s.successor
        return s

    def next_non_intersecting(self, n):
        c = n
        while c.intersect:
            c = c.successor
        return c

    def unprocessed(self):
        for n in self:
            if n.intersect and not n.checked:
                return True
        return False

    def first_intersect(self):
        for n in self:
            if n.intersect and not n.checked:
                return n

    def points(self):
        p = []
        for v in self:
            p.append(v.pos)
        return p

    def union(self, other):
        return self.clip(other, False, False)

    def difference(self, clip):
        return self.clip(clip, False, True)

    def clip(self, clip, s_entry, c_entry):
        """Clip this polygon using another one as a clipper.
        This is where the algorithm is executed. It allows you to make
        a UNION, INTERSECT or DIFFERENCE operation between two polygons.
        Given two polygons A, B the following operations may be performed:
        A|B ... A OR B  (Union of A and B)
        A&B ... A AND B (Intersection of A and B)
        A\B ... A - B
        B\A ... B - A
        The entry records store the direction the algorithm should take when
        it arrives at that entry point in an intersection. Depending on the
        operation requested, the direction is set as follows for entry points
        (f=forward, b=backward; exit points are always set to the opposite):
              Entry
              A   B
              -----
        A|B   b   b
        A&B   f   f
        A\B   b   f
        B\A   f   b
        f = True, b = False when stored in the entry record
        """
        # find intersections
        found_intersection = False
        for s in self:
            if not s.intersect:
                for c in clip:
                    if not c.intersect:
                        try:
                            i, alpha_s, alpha_c = intersect(s.pos, self.next_non_intersecting(s.successor).pos,
                                                            c.pos, clip.next_non_intersecting(c.successor).pos)
                            found_intersection = True
                            i_s = Node(i, alpha_s, intersect=True, entry=False)
                            i_c = Node(i, alpha_c, intersect=True, entry=False)
                            i_s.neighbour = i_c
                            i_c.neighbour = i_s
                            self.insert(i_s, s, self.next_non_intersecting(s.successor))
                            clip.insert(i_c, c, self.next_non_intersecting(c.successor))
                        except TypeError:
                            pass    # intersect returned None. No problem

        if not found_intersection:
            if self.begin.is_inside(clip):
                return [clip], Polygon.RET_CLIP
            if clip.begin.is_inside(self):
                return [self], Polygon.RET_SELF
            return [self, clip], Polygon.RET_DISJOINT

        # identify entry/exit points
        s_entry ^= self.begin.is_inside(clip)
        for s in self:
            if s.intersect:
                s.entry = s_entry
                s_entry = not s_entry

        c_entry ^= clip.begin.is_inside(self)
        for c in clip:
            if c.intersect:
                c.entry = c_entry
                c_entry = not c_entry

        # construct list of clipped polygons
        l = []
        while self.unprocessed():
            current = self.first_intersect()
            clipped = Polygon()
            clipped.add(Node(Vec2(current.pos.x, current.pos.y)))
            while True:
                current.set_checked()
                if current.entry:
                    while True:
                        current = current.successor
                        if not current.checked or True:
                            clipped.add(Node(Vec2(current.pos.x, current.pos.y)))
                        if current.intersect:
                            break
                else:
                    while True:
                        current = current.predecessor
                        if not current.checked or True:
                            clipped.add(Node(Vec2(current.pos.x, current.pos.y)))
                        if current.intersect:
                            break

                current = current.neighbour
                if current.checked:
                    break

            l.append(clipped)

        if not l:
            l.append(self)

        return l, Polygon.RET_UNION

    @staticmethod
    def from_points(points):
        path = Polygon()
        for p in points:
            path.add_position(p)
        return path

    def __iter__(self) -> 'Node':
        s = self.begin
        while True:
            yield s
            s = s.successor
            if s is self.begin:
                break

    def __next__(self):
        self._current = self._current.successor
        return self._current

    def __repr__(self):
        return f"Path: {id(self)} {self.points()}"


class Node:

    def __init__(self, pos: Vec2, alpha=0.0, intersect=False, entry=True, checked=False):
        self.pos = pos
        self.predecessor = None
        self.successor = None
        self.neighbour = None
        self.entry = entry
        self.alpha = alpha
        self.intersect = intersect
        self.checked = checked

    def is_inside(self, poly: Polygon):
        winding_number = 0
        infinity = Vec2(100000, self.pos.y)
        for q in poly:
            if not q.intersect and intersect(self.pos, infinity, q.pos, poly.next_non_intersecting(q.successor).pos):
                winding_number += 1
        return (winding_number % 2) != 0

    def set_checked(self):
        self.checked = True
        if self.neighbour and not self.neighbour.checked:
            self.neighbour.set_checked()

    def __repr__(self):
        return f"Node(pos={self.pos}, predecessor={id(self.predecessor)}, successor={id(self.successor)})"
