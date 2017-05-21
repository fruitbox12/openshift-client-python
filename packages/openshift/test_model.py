from .model import *
import unittest



class TestStringMethods(unittest.TestCase):

    def test_empty(self):
        empty = Model()
        self.assertIs(empty.metadata, Missing)
        self.assertIs(empty["metadata"], Missing)
        self.assertIs(empty.metadata.a, Missing)
        self.assertIs(empty.metadata["a"], Missing)

    def test_access(self):
        m = Model()
        m.metadata = {
            "a": 1,
            "b": 2,
            "map1": {
                "c": 3,
                "d": 4
            },
            "list1": [
                5,
                6,
                7,
            ],
            "list2": [
                {
                    "e": 5,
                    "f": 6
                },
                {
                    "g": 5,
                    "h": 6
                },
            ],
            "anull": None,
            "astring": "thevalue"
        }

        self.assertIsNot(m.metadata, Missing)
        self.assertIsNot(m.metadata.a, Missing)
        self.assertEqual(m.metadata.b, 2)

        self.assertIsNot(m.metadata.map1, Missing)
        self.assertIsNot(m.metadata["map1"], Missing)

        self.assertIs(m.metadata["map_notthere"], Missing)
        self.assertIs(m.metadata.map_notthere, Missing)

        self.assertEqual(m.metadata.map1.c, 3)
        self.assertEqual(m.metadata.map1.d, 4)
        self.assertIs(m.metadata.map1.e, Missing)

        self.assertEqual(len(m.metadata.list1), 3)
        self.assertEqual(len(m.metadata["list1"]), 3)
        self.assertEqual(m.metadata.list1[0], 5)
        self.assertEqual(m.metadata.list1, [5,6,7])
        self.assertEqual(m.metadata["list1"], [5,6,7])

        try:
            m.metadata.list1[3]
            self.fail("Did not receive expected IndexError")
        except IndexError:
            pass

        self.assertIsNot(m.metadata.list2, Missing)
        self.assertIsNot(m.metadata.list2[0], Missing)
        self.assertIsNot(m.metadata.list2[1], Missing)
        self.assertIsNot(m.metadata.list2[1].g, Missing)
        self.assertIsNot(m.metadata.list2[1].h, Missing)
        self.assertIs(m.metadata.list2[1].notthere, Missing)
        self.assertIsNone(m.metadata.anull)

        self.assertEqual(m.metadata.astring, "thevalue")
        self.assertEqual(m.metadata["astring"], "thevalue")

        m.list3 = ['a', 'b']
        self.assertIsNot(m.list3, Missing)
        self.assertIsNot(m["list3"], Missing)
        self.assertEqual(m["list3"][0], "a")

        m.a = 5
        m.b = "hello"
        m.c = True
        m.d = False
        m.e = None

        self.assertEqual(m.a, 5)
        self.assertEqual(m.b, "hello")
        self.assertEqual(m.c, True)
        self.assertEqual(m.d, False)
        self.assertEqual(m.e, None)

    def test_match(self):

        l1 = ListModel(["a", "b", "c"])
        self.assertTrue(l1.can_match("b", "c"))
        self.assertTrue(l1.can_match("a", "c"))
        self.assertTrue(l1.can_match("c"))
        self.assertTrue(l1.can_match("a"))

        self.assertFalse(l1.can_match("1"))
        self.assertFalse(l1.can_match("1", "2"))
        self.assertFalse(l1.can_match(True))

        self.assertFalse(l1.can_match({"a": 2}))

        l2 = ListModel([True])
        self.assertTrue(l2.can_match(True))
        self.assertFalse(l2.can_match(False))

        l3 = ListModel([
            {
                "a": 1,
                "b": 2,
                "c": 3
            },
            {
                "d": 1,
                "e": 2,
                "f": 3
            },
            {
                "d": True,
                "e": [2, 3, True],
                "f": 3
            }
        ])

        self.assertTrue(l3.can_match(
            {
                "c": 3
            }
        ))
        self.assertTrue(l3.can_match(
            {
                "c": 3,
                "a": 1
            }
        ))
        self.assertTrue(l3.can_match(
            {
                "c": 3,
                "a": 1,
                "b": 2
            }
        ))
        self.assertFalse(l3.can_match(
            {
                "a": 1,
                "b": 3,
            }
        ))
        self.assertFalse(l3.can_match(
            {
                "b": 3,
            }
        ))
        self.assertTrue(l3.can_match(
            {
                "d": True,
                "f": 3,
            }
        ))
        self.assertFalse(l3.can_match(
            {
                "e": 3,
            }
        ))
        self.assertTrue(l3.can_match(
            {
                "e": [3],
            }
        ))
        self.assertTrue(l3.can_match(
            {
                "e": [2, 3],
            }
        ))
        self.assertTrue(l3.can_match(
            {
                "e": [2, 3, True],
            }
        ))
        self.assertFalse(l3.can_match(
            {
                "d": True,
                "e": [2, 3, False],
            }
        ))
        self.assertTrue(l3.can_match(
            {
                "d": True,
                "e": [2, 3, True],
            }
        ))


        l4 = ListModel([
            {
                "a": 1,
                "b": {
                    "a1": 5,
                    "b1": {
                        "a2": 6,
                        "b2": {
                            "a3": 7,
                            "b3": 8
                        }
                    }
                },
                "c": 3
            },
        ])

        self.assertTrue(l4.can_match(
            {
                "a": 1,
            }
        ))
        self.assertTrue(l4.can_match(
            {
                "a": 1,
                "b": {
                    "a1": 5
                }
            }
        ))
        self.assertTrue(l4.can_match(
            {
                "a": 1,
                "b": {
                    "a1": 5,
                    "b1": {
                        "a2": 6
                    }
                }
            }
        ))
        self.assertTrue(l4.can_match(
            {
                "a": 1,
                "b": {
                    "a1": 5,
                    "b1": {
                        "b2": {
                            "b3": 8
                        }
                    }
                }
            }
        ))


if __name__ == '__main__':
    unittest.main()



