from decimal import ROUND_HALF_UP, Decimal
import numpy as np
from math import atan, tan, degrees, sqrt


class PaintCalculations:
    def __init__(self, height, width, unit, profile=None, windowHeight=0, windowWidth=0, doorHeight=0, doorWidth=0):
        self.height = height
        self.width = width
        self.unit = unit
        self.profile = profile
        self.windowHeight = windowHeight
        self.windowWidth = windowWidth
        self.doorHeight = doorHeight
        self.doorWidth = doorWidth
        self.paintThicknessMeters = 0.0001
        self.paintThicknessFeet = self.paintThicknessMeters / 0.3048

    def findVolume(self, width, height):
        surfaceArea = width * height
        paintVolume = 0
        if self.unit == 'metric':
            paintVolume = (surfaceArea * self.paintThicknessMeters) * 1000
        if self.unit == 'usStandard':
            paintVolume = surfaceArea * self.paintThicknessFeet * 7.48052
        return Decimal(paintVolume)

            
    def calculatePaintRequired(self):
        totalPaintVolume = 0
        if self.height > 0 and self.width > 0:
            totalPaintVolume += self.findVolume(self.height, self.width)
        if self.windowHeight > 0 and self.windowWidth > 0:
            totalPaintVolume -= self.findVolume(self.windowHeight, self.windowWidth)
        if self.doorHeight > 0 and self.doorWidth > 0:
            totalPaintVolume -= self.findVolume(self.doorHeight, self.doorWidth)
        # return array containing [magnitude, unitType]
        if self.unit == 'metric':
            self.unit = 'Liters of Paint'
        else:
            self.unit = 'Gallons of Paint'
        return [Decimal(totalPaintVolume), self.unit]
    
    def calculateWindowArea(self, windowHeight, windowWidth):
        windowArea = Decimal(windowHeight) * Decimal(windowWidth)
        return windowArea

    def calculateDoorArea(self, doorHeight, doorWidth):
        doorArea = Decimal(doorHeight) * Decimal(doorWidth)
        return doorArea
    
    
def calculateSideLengths(corners):
    # Ensure the corners are in a NumPy array
    corners = np.array(corners)

    # Calculate the Euclidean distances between the first two pairs of consecutive points
    side_length1 = int(np.linalg.norm(corners[0] - corners[1]))
    side_length2 = int(np.linalg.norm(corners[1] - corners[2]))

    # Return the two sides as length and width in an array
    return [side_length1, side_length2]

import math


def calculateRealLengths(side_lengths, distance_to_rectangle, hfov, vfov, image_width, image_height):
    # Calculate the vertical field of view (VFOV) in degrees

    # Calculate the angular resolution per pixel
    angular_resolution_horizontal = hfov / image_width
    angular_resolution_vertical = vfov / image_height

    # Convert the side lengths of the inner rectangle to angles in radians
    angle_length = math.radians(side_lengths[0] * angular_resolution_horizontal)
    angle_width = math.radians(side_lengths[1] * angular_resolution_vertical)

    # Calculate the real-world lengths in feet using the tangent function
    length_real = 2 * distance_to_rectangle * math.tan(angle_length / 2)
    width_real = 2 * distance_to_rectangle * math.tan(angle_width / 2)

    # Calculate the area in square feet and square inches
    return length_real, width_real

def calculate_fovs(dfov, width, height):
    # Calculate the aspect ratio of the image
    aspect_ratio = width / height

    # Calculate the diagonal aspect ratio
    diagonal_aspect_ratio = sqrt(1 + aspect_ratio**2)

    # Convert diagonal FOV to radians
    diagonal_fov_rad = dfov * (3.14159265 / 180)

    # Calculate horizontal FOV in degrees
    hfov = 2 * degrees(atan(tan(diagonal_fov_rad / 2) / diagonal_aspect_ratio))

    # Calculate vertical FOV in degrees
    vfov = hfov / aspect_ratio

    return hfov, vfov

def calculate_vfov(hfov, dfov):
    # Calculate the ratio of the diagonal FOV to the horizontal FOV
    ratio = dfov / hfov

    # Calculate the vertical field of view using the Pythagorean theorem
    vfov = math.sqrt(dfov**2 - hfov**2) * ratio

    return vfov

from PIL import Image

def getImageDimensions(file_path):
    # Open the image file
    file_path = "./static/" + file_path
    with Image.open(file_path) as img:
        # Get the width and height of the image
        width, height = img.size

    return width, height
