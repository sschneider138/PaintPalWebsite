from decimal import ROUND_HALF_UP, Decimal

class PaintCalculations:
    def __init__(self, height, width, unit, profile=None, windowHeight=0, windowWidth=0, doorHeight=0, doorWidth=0,):
        self.height = height
        self.width = width
        self.unit = unit
        self.profile = profile
        self.windowHeight = windowHeight
        self.windowWidth = windowWidth
        self.doorHeight = doorHeight
        self.doorWidth = doorWidth
        self.paintThicknessMeters = Decimal('0.00005')
        self.paintThicknessFeet = self.paintThicknessMeters / Decimal('0.3048')

    def calculatePaintRequired(self, isWindowPainted=False, isDoorPainted=True):
        if self.unit == 'metric':
            # find surface area in m^2
            surfaceArea = Decimal(self.height) * Decimal(self.width)

            # find volume in m^3
            # internet searching estimates layer is 0.05mm when dry
            # source - https://www.quora.com/If-someone-painted-a-coat-of-paint-on-the-walls-of-their-house-a-hundred-times-would-the-walls-become-thicker
            paintVolume = (surfaceArea * self.paintThicknessMeters)
            
            # convert from m^3 to liters
            paintVolume = paintVolume * Decimal('1000')
            units = 'liters of paint'

        else:
            # find surface area in feet^2
            surfaceArea = Decimal(self.height) * Decimal(self.width)

            # find volume in feet^3
            paintVolume = surfaceArea * self.paintThicknessFeet

            # convert feet^3 to gallons
            paintVolume = paintVolume * Decimal('7.48052')
            units = 'gallons of paint'

        # deduct areas of unpainted windows and doors
        if not isWindowPainted:
            windowArea = self.calculateWindowArea(self.windowHeight, self.windowWidth)
            paintVolume -= windowArea

        if not isDoorPainted:
            doorArea = self.calculateDoorArea(self.doorHeight, self.doorWidth)  # Calculate door area
            paintVolume -= doorArea

        # Round the paint volume to two decimal places
        paintVolume = paintVolume.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


        # update the user's profile with the calculated paint used
        if self.unit == 'metric':
            self.profile.paintUsedLiters += paintVolume
        else:
            self.profile.paintUsedGallons += paintVolume

        # return array containing [magnitude, unitType]
        return [paintVolume, units]
    
    def calculateWindowArea(self, windowHeight, windowWidth):
        windowArea = Decimal(windowHeight) * Decimal(windowWidth)
        return windowArea

    def calculateDoorArea(self, doorHeight, doorWidth):
        doorArea = Decimal(doorHeight) * Decimal(doorWidth)
        return doorArea