from Code.Util.Visuals.Visual import Visual


class MultiVisual(Visual):
    def __init__(self, visuals, primaryVisual=None):
        self.visuals = visuals
        if primaryVisual is None:
            primaryVisual = visuals[0]
        self.primaryVisual: Visual = primaryVisual
        super().__init__()

    def remove(self):
        for visual in self.visuals:
            visual.remove()

    def getPosition(self):
        return self.primaryVisual.getPosition()

    def setPosition(self, x, y):
        for visual in self.visuals:
            visual.setPosition(x, y)

    def getDimensions(self):
        return self.primaryVisual.getDimensions()

    def getAnchoredDimensions(self):
        return self.primaryVisual.getAnchoredDimensions()

    def getRotation(self):
        return self.primaryVisual.getRotation()

    def setRotation(self, rotation):
        for visual in self.visuals:
            visual.setRotation(rotation)

    def getColor(self):
        return self.primaryVisual.getColor()

    def updateColor(self, color):
        for visual in self.visuals:
            visual.updateColor(color)

    def getOpacity(self):
        return self.primaryVisual.getOpacity()

    def setOpacity(self, opacity):
        for visual in self.visuals:
            visual.setOpacity(opacity)

    def getVisible(self):
        return self.primaryVisual.getVisible()

    def setVisible(self, visible):
        for visual in self.visuals:
            visual.setVisible(visible)

    def getScale(self):
        return self.primaryVisual.getScale()

    def setScale(self, scale):
        for visual in self.visuals:
            visual.setScale(scale)
