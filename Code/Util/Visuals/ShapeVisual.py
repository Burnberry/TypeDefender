from Code.Util.Visuals.Visual import Visual


class ShapeVisual(Visual):
    def __init__(self, shape):
        super().__init__()
        self.shape = shape

    def remove(self):
        if self.shape:
            self.shape.delete()
            self.shape = None

    def getPosition(self):
        return self.shape.x, self.shape.y

    def setPosition(self, x, y):
        self.shape.x, self.shape.y = x, y

    def getDimensions(self):
        return self.shape.width, self.shape.height

    def getRotation(self):
        return self.shape.rotation

    def setRotation(self, rotation):
        self.shape.rotation = rotation

    def getColor(self):
        return self.shape.color

    def updateColor(self, color):
        self.shape.color = color

    def getOpacity(self):
        return self.shape.opacity

    def setOpacity(self, opacity):
        self.shape.opacity = opacity

    def getVisible(self):
        return self.shape.visible

    def setVisible(self, visible):
        self.shape.visible = visible

    def getScale(self):
        return 1

    def setScale(self, scale):
        pass
