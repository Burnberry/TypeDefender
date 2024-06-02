from pyglet.sprite import Sprite

from Code.Util.Visuals.Visual import Visual


class SpriteVisual(Visual):
    def __init__(self, asset, batch, group):
        super().__init__()
        self.sprite = Sprite(asset.get(), batch=batch, group=group)

    def remove(self):
        if self.sprite:
            self.sprite.delete()
            self.sprite = None

    def getPosition(self):
        return self.sprite.x, self.sprite.y

    def setPosition(self, x, y):
        self.sprite.x, self.sprite.y = x, y

    def getDimensions(self):
        return self.sprite.width, self.sprite.height

    def getRotation(self):
        return self.sprite.rotation

    def setRotation(self, rotation):
        self.sprite.rotation = rotation

    def getColor(self):
        return self.sprite.color

    def updateColor(self, color):
        self.sprite.color = color

    def getOpacity(self):
        return self.sprite.opacity

    def setOpacity(self, opacity):
        self.sprite.opacity = opacity

    def getVisible(self):
        return self.sprite.visible

    def setVisible(self, visible):
        self.sprite.visible = visible

    def getScale(self):
        return self.sprite.scale

    def setScale(self, scale):
        self.sprite.scale = scale
