from decimal import ROUND_HALF_UP, Decimal

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