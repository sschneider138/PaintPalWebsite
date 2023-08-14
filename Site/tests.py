from django.test import TestCase
from PIL import Image
from calculations.PaintCalculations import *

class ImageProcessingTests(TestCase):

    def test_get_image_dimensions(self):
        test_image_path = './staticfiles/testImages/test1.jpg'
        expected_width, expected_height = 612, 365
        width, height = getImageDimensions(test_image_path)
        self.assertEqual(width, expected_width)
        self.assertEqual(height, expected_height)

    def test_calculate_vfov(self):
        hfov = 70
        dfov = 77
        # Calculating the expected vertical FOV
        expected_vfov = (dfov**2 - hfov**2)**0.5 * (dfov / hfov)
        vfov = calculate_vfov(hfov, dfov)
        self.assertEqual(vfov, expected_vfov)

class PaintCalculations:
    def __init__(self, height, width, unit,profile=None, windowHeight=0, windowWidth=0):
      self.height = height
      self.width = width
      self.unit = unit
      self.profile = profile
      self.windowHeight = windowHeight
      self.windowWidth = windowWidth

class TestPaintCalculations(TestCase):
    def test_initialization(self):
        paint_calc = PaintCalculations(10, 5, 'm', 'profile1', 2, 1)
        self.assertEqual(paint_calc.width, 5) 
        self.assertEqual(paint_calc.unit, 'm')
        self.assertEqual(paint_calc.profile, 'profile1')
        self.assertEqual(paint_calc.windowHeight, 2)
        self.assertEqual(paint_calc.windowWidth, 1)