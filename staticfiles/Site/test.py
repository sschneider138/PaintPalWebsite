import unittest

class PainCalculations:

    def __init__(self, height, width, unit,profile=None, windowHeight=0, windowWidth=0):
      self.height = height
      self.width = width
      self.unit = unit
      self.profile = profile
      self.windowHeight = windowHeight
      self.windowWidth = windowWidth

class TestPaintCalculations(unittest.TestCase):
   def test_initialization(self):
      paint_calc =PainCalculations(10, 5, 'm','profile1',2, 1)
      self.assertEqual(paint_calc.width, 5) 
      self.assertEqual(paint_calc.unit, 'm')
      self.assertEqual(paint_calc.profile,'profile1')
      self.assertEqual(paint_calc.windowHeight, 2)
      self.assertEqual(paint_calc.windowWidth, 1) 

if __name__ == '__main__': 
   unittest.main()
