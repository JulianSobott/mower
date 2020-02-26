import unittest

from mower.core.Map import *


class TestDrawing(unittest.TestCase):

    def test_rect_union(self):
        p1 = Path.from_points([Vec2(0, 0), Vec2(10, 0), Vec2(10, 10), Vec2(0, 10)])
        p2 = Path.from_points([Vec2(5, 5), Vec2(7, 5), Vec2(7, 15), Vec2(5, 15)])
        paths = p1.union(p2)
        expected = [Vec2(0, 0), Vec2(10, 0), Vec2(10, 10), Vec2(7, 10), Vec2(7, 15), Vec2(5, 15), Vec2(5, 10),
                    Vec2(0, 10)]
        self.assertEqual(1, len(paths))
        self.assertEqual(expected, paths[0].points())


if __name__ == '__main__':
    unittest.main()
