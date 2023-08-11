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
