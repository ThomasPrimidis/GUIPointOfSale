import unittest
import sys
sys.path.insert(0, "../src")
from item import Item

class Test_Item(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(TypeError):
          Item(1, 30, 3, 2, 0)
        with self.assertRaises(TypeError):
          Item("A", "A", 3, 2, 0)
        with self.assertRaises(TypeError):
          Item("A", 30, "A", 2, 0)
        with self.assertRaises(TypeError):
          Item("A", 30, 3, "A", 0)
        with self.assertRaises(TypeError):
          Item("A", 30, 3, 2, "A")

        with self.assertRaises(ValueError):
          Item("Z", 30, 3, 2, 0)
        with self.assertRaises(ValueError):
          Item("A", -30, 3, 2, 0)
        with self.assertRaises(ValueError):
          Item("A", 30, -3, 2, 0)
        with self.assertRaises(ValueError):
          Item("A", 30, 3, -2, 0)
        with self.assertRaises(ValueError):
          Item("A", 30, 3, 0, -2)
        with self.assertRaises(ValueError):
          Item("A", 30, 3, 2, 2)

    def test_getMultibuyCost(self):
        item = Item("A", 30, 3, 2, 0)
        with self.assertRaises(TypeError):
          item.getMultibuyCost("a")
        with self.assertRaises(ValueError):
          item.getMultibuyCost(-1)


if __name__ == '__main__':
    unittest.main()
