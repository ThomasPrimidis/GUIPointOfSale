import unittest
import sys
sys.path.insert(0, "../src")
from checkout import Checkout

class Test_Checkout(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(TypeError):
            Checkout(1)
        with self.assertRaises(TypeError):
            Checkout(None, [1,2,3])
        with self.assertRaises(ValueError):
            Checkout(None, {})
        with self.assertRaises(TypeError):
            Checkout(None, {4:[25, 3, 2, 0]})
        with self.assertRaises(ValueError):
            Checkout(None, {"AA":[25, 3, 2, 0]})
        with self.assertRaises(TypeError):
            Checkout(None, {"A":(25, 3, 2, 0)})
        with self.assertRaises(ValueError):
            Checkout(None, {"A":[25, 3, 2]})
        with self.assertRaises(ValueError):
            Checkout(None, {"Z":[25, 3, 2, 0]})

        with self.assertRaises(TypeError):
            Checkout(None, {"A":[25., 3, 2, 0]})
        with self.assertRaises(TypeError):
            Checkout(None, {"A":[25, 3., 2, 0]})
        with self.assertRaises(TypeError):
            Checkout(None, {"A":[25, 3, 2., 0]})
        with self.assertRaises(TypeError):
            Checkout(None, {"A":[25, 3, 2, 0.]})

        with self.assertRaises(ValueError):
            Checkout(None, {"A":[-25, 3, 2, 0]})
        with self.assertRaises(ValueError):
            Checkout(None, {"A":[25, -3, 2, 0]})
        with self.assertRaises(ValueError):
            Checkout(None, {"A":[25, 3, -2, 0]})
        with self.assertRaises(ValueError):
            Checkout(None, {"A":[25, 3, 0, -1]})
        with self.assertRaises(ValueError):
            Checkout(None, {"A":[25, 3, 2, 1]})

    def test_copyTo(self):
        chekout_ = Checkout(None, {"A":[25,3,2,0]})
        with self.assertRaises(TypeError):
            chekout_.copyTo(5)

    def test_register(self):        
        chekout_ = Checkout(None, {"A":[25,3,2,0]})
        with self.assertRaises(TypeError):
            chekout_.register(None)

    def test_unregister(self):        
        chekout_ = Checkout(None, {"A":[25,3,2,0]})
        with self.assertRaises(TypeError):
            chekout_.unregister(None)

    def test_signal(self):
        chekout_ = Checkout(None, {"A":[25,3,2,0]})
        with self.assertRaises(TypeError):
            chekout_.signal(5)
        with self.assertRaises(ValueError):
            chekout_.signal("")
        with self.assertRaises(TypeError):
            chekout_.signal(5)

    def test_initItemsCatalogue(self):
        checkout_ = Checkout(None, {"A":[25,3,2,0]})
        with self.assertRaises(TypeError):
            checkout_._initItemsCatalogue([1,2,3])

    def test_getNumberOfItems(self):
        checkout_ = Checkout(None, 
                    {"A": [25, 3, 2, 0],
                     "B": [35, 3, 0, 100],
                     "P": [40, 3, 0, 0]
                    })
        with self.assertRaises(TypeError):
            checkout_.getNumberOfItems(4)
        with self.assertRaises(ValueError):
            checkout_.getNumberOfItems("Z")

    def test_scan(self):
        checkout_ = Checkout(None, 
                    {"A": [25, 3, 2, 0],
                     "B": [35, 3, 0, 100],
                     "P": [40, 3, 0, 0]
                    })
        with self.assertRaises(TypeError):
            checkout_.scan(5)
        with self.assertRaises(TypeError):
            checkout_.scan("A", 0)
        with self.assertRaises(ValueError):
            checkout_.scan("Z")
        with self.assertRaises(ValueError):
            checkout_.scan("A", "")

    def test_unscan(self):
        checkout_ = Checkout(None, 
                    {"A": [25, 3, 2, 0],
                     "B": [35, 3, 0, 100],
                     "P": [40, 3, 0, 0]
                    })
        with self.assertRaises(TypeError):
            checkout_.unscan(5)
        with self.assertRaises(TypeError):
            checkout_.unscan("A", 0)
        with self.assertRaises(ValueError):
            checkout_.unscan("Z")
        with self.assertRaises(ValueError):
            checkout_.unscan("A", "")

        checkout_._basket["A"]=-1
        with self.assertRaises(ValueError):
          checkout_.unscan("A")

    def test_clearBasket(self):
        checkout_ = Checkout(None, 
                    {"A": [25, 3, 2, 0],
                     "B": [35, 3, 0, 100],
                     "P": [40, 3, 0, 0]
                    })
        checkout_._basket["A"]=10
        checkout_._basket["B"]=10
        checkout_._basket["P"]=10
        with self.assertRaises(TypeError):
            checkout_.clearBasket(itemCode = 5)
        with self.assertRaises(TypeError):
            checkout_.clearBasket("P", 0)
        with self.assertRaises(ValueError):
            checkout_.clearBasket("PEAR")
        with self.assertRaises(ValueError):
            checkout_.clearBasket("P", "")


    def test_checkout(self):
        checkout_ = Checkout(None, 
                    {"A": [25, 3, 2, 0],
                     "B": [40, 3, 0, 100],
                     "P": [30, 3, 0, 0]
                    })
        with self.assertRaises(TypeError):
            checkout_.checkout(1,{})
        with self.assertRaises(TypeError):
            checkout_.checkout([],1)
        with self.assertRaises(TypeError):
            checkout_.checkout([1],{})
        with self.assertRaises(ValueError):
            checkout_.checkout(["Z"],{})
        with self.assertRaises(ValueError):
            checkout_.checkout(["A", "B", "P"],{"Z": 25})
        with self.assertRaises(TypeError):
            checkout_.checkout(["A", "B", "P"],{"A": "25"})
        with self.assertRaises(ValueError):
            checkout_.checkout(["A", "B", "P"],{"A": -25})
        with self.assertRaises(ValueError):
            checkout_.checkout(["A", "B", "P"],{"A": 100})
        self.assertEqual(155, checkout_.checkout(["B", "A", "B", "P", "B"], {"A": 25, "B": 40, "P": 30}))


    def test_total(self):
        checkout_ = Checkout(None, 
                    {"A": [25, 3, 2, 0],
                     "B": [40, 3, 0, 100],
                     "P": [30, 3, 0, 0]
                    })
        checkout_._basket["A"]=1
        checkout_._basket["B"]=3
        checkout_._basket["P"]=1
        with self.assertRaises(TypeError):
            checkout_.total(5)
        with self.assertRaises(ValueError):
            checkout_.total("banana")

        total_, savings_ = checkout_.total()
        self.assertListEqual([total_, savings_], [155, 20])
          
if __name__ == '__main__':
    unittest.main()
