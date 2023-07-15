import pint

convertInstance = pint.UnitRegistry()

class PaintCalculations:
    def __init__(self, height, width, unit):
        self.height = height
        self.width = width
        self.unit = unit
        self.paintThicknessMeters = 0.0001
        self.paintThicknessFeet = self.paintThicknessMeters / 0.3048

    def calculatePaintRequired(self):
        if self.unit == 'metric':
            # find surface area in m^2
            surfaceArea = self.height * self.width

            # find volume in m^3
            # internet searching estimates layer is 0.05mm when dry. Double this for estimated wet thickness 
            # source - https://www.quora.com/If-someone-painted-a-coat-of-paint-on-the-walls-of-their-house-a-hundred-times-would-the-walls-become-thicker
            paintVolume = (surfaceArea * self.paintThicknessMeters)
            
            # convert from m^3 to liters
            paintVolume = paintVolume * 1000
            units = 'liters of paint'

        else:
            # find surface area in feet^2
            surfaceArea = self.height * self.width

            # find volume in feet^3
            paintVolume = surfaceArea * self.paintThicknessFeet

            # convert feet^3 to gallons
            paintVolume = paintVolume * 7.48052
            units = 'gallons of paint'

        # return array containing [magnitude, unitType]
        return [paintVolume, units]
