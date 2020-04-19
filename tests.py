from collections import defaultdict
import unittest

from space import Object, Space, POSSIBLE_OBJECTS


class ObjectCreation(unittest.TestCase):

    def test_creature(self):
        object_type = "creature"
        creature = Object(object_type)
        self.assertEqual(creature.type, object_type)
        self.assertEqual(creature.color, POSSIBLE_OBJECTS[object_type]["color"])
        self.assertEqual(creature.moved_in_current_round, False)

    def test_not_existing_object(self):
        with self.assertRaises(ValueError):
            Object("wrong object type")


class SpaceCreation(unittest.TestCase):

    def test_space(self):
        space_size = 3
        space = Space(space_size)
        self.assertEqual(space.size, space_size)
        self.assertListEqual(space.objects, [[None]*space_size for _ in range(space_size)])
        self.assertDictEqual(space.cnt_objects, defaultdict(int))


if __name__ == '__main__':
    unittest.main()
