import unittest

from mower.core.Map import *


class TestDrawing(unittest.TestCase):

    def test_rect_union1(self):
        p1 = Path.from_points([Vec2(0, 0), Vec2(10, 0), Vec2(10, 10), Vec2(0, 10)])
        p2 = Path.from_points([Vec2(5, 5), Vec2(7, 5), Vec2(7, 15), Vec2(5, 15)])
        paths = p1.union(p2)
        expected = [Vec2(0, 0), Vec2(10, 0), Vec2(10, 10), Vec2(7, 10), Vec2(7, 15), Vec2(5, 15), Vec2(5, 10),
                    Vec2(0, 10)]
        self.assertEqual(1, len(paths))
        self.assertEqual(len(expected), len(paths[0].points()))
        for v in expected:
            self.assertIn(v, paths[0].points())

    def test_rect_union2(self):
        p1 = Path.from_points([Vec2(0, 0), Vec2(10, 0), Vec2(10, 10), Vec2(0, 10)])
        p2 = Path.from_points([Vec2(5, 5), Vec2(7, 5), Vec2(7, 15), Vec2(5, 15)])
        paths = p1.union(p2)
        expected = [Vec2(0, 0), Vec2(10, 0), Vec2(10, 10), Vec2(7, 10), Vec2(7, 15), Vec2(5, 15), Vec2(5, 10),
                    Vec2(0, 10)]
        self.assertEqual(1, len(paths))
        self.assertEqual(len(expected), len(paths[0].points()))
        for v in expected:
            self.assertIn(v, paths[0].points())

    def test_union_degeneracies(self):
        p1 = Path.from_points([Vec2(0, 0), Vec2(10, 0), Vec2(10, 10), Vec2(0, 10)])
        p2 = Path.from_points([Vec2(10, 5), Vec2(15, 0), Vec2(15, 10)])
        paths = p1.union(p2)
        expected = [Vec2(0, 0), Vec2(10, 0), Vec2(10, 5), Vec2(15, 0), Vec2(15, 10), Vec2(10, 5),
                    Vec2(10, 10), Vec2(0, 10)]
        self.assertEqual(1, len(paths))
        self.assertEqual(len(expected), len(paths[0].points()))
        for v in expected:
            self.assertIn(v, paths[0].points())

    def test_union_degeneracies2(self):
        p1 = Path.from_points([Vec2(0, 0), Vec2(10, 0), Vec2(10, 10), Vec2(0, 10)])
        p2 = Path.from_points([Vec2(10, 0), Vec2(15, 0), Vec2(15, 10)])
        paths = p1.union(p2)
        expected = [Vec2(0, 0), Vec2(10, 0), Vec2(15, 0), Vec2(15, 10), Vec2(10, 0),
                    Vec2(10, 10), Vec2(0, 10)]
        self.assertEqual(1, len(paths))
        self.assertEqual(len(expected), len(paths[0].points()))
        for v in expected:
            self.assertIn(v, paths[0].points())

    def test_union_degeneracies3(self):
        p1 = Path.from_points([Vec2(0, 0), Vec2(10, 0), Vec2(10, 10), Vec2(0, 10)])
        p2 = Path.from_points([Vec2(10, 0), Vec2(15, 0), Vec2(15, 5), Vec2(10, 5)])
        paths = p1.union(p2)
        expected = [Vec2(0, 0), Vec2(10, 0), Vec2(15, 0), Vec2(15, 5), Vec2(10, 5), Vec2(10, 0),
                    Vec2(10, 10), Vec2(0, 10)]
        self.assertEqual(1, len(paths))
        self.assertEqual(len(expected), len(paths[0].points()))
        for v in expected:
            self.assertIn(v, paths[0].points())

    def test_union_degeneracies4(self):
        p1 = Path.from_points([Vec2(0, 0), Vec2(10, 0), Vec2(10, 10), Vec2(0, 10)])
        p2 = Path.from_points([Vec2(10, 3), Vec2(15, 0), Vec2(15, 5), Vec2(10, 5)])
        paths = p1.union(p2)
        expected = [Vec2(0, 0), Vec2(10, 0), Vec2(10, 3), Vec2(15, 0), Vec2(15, 5), Vec2(10, 5),
                    Vec2(10, 10), Vec2(0, 10)]
        self.assertEqual(1, len(paths))
        self.assertEqual(len(expected), len(paths[0].points()))
        for v in expected:
            self.assertIn(v, paths[0].points())

    def test_is_inside(self):
        p1 = Path.from_points([Vec2(0, 0), Vec2(10, 0), Vec2(10, 10), Vec2(0, 10)])
        point = Node(Vec2(5, 5))
        self.assertTrue(point.is_inside(p1))


if __name__ == '__main__':
    unittest.main()
