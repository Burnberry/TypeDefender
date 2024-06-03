from pyglet.text import Label

from Code.Util.SettingsGlobal import SettingsGlobal
from Code.Util.Visuals.Visual import Visual


class LabelVisual(Visual):
    def __init__(self, x, y, text, batch, group, scale=1, anchorX="center", anchorY="bottom"):
        self.scale = scale
        size = self.getFontSize()
        self.label = Label(x=x, y=y, text=text, font_size=size, batch=batch, group=group, anchor_x=anchorX, anchor_y=anchorY)
        super().__init__()

    def remove(self):
        if self.label:
            self.label.delete()
            self.label = None

    def getPosition(self):
        return self.label.x, self.label.y

    def setPosition(self, x, y):
        self.label.x, self.label.y = x, y

    def getCenter(self):
        x, y = self.getPosition()
        w, h = self.getDimensions()

        if self.label.anchor_x == "left":
            x += w/2
        elif self.label.anchor_x == "right":
            x -= w/2

        if self.label.anchor_y == "bottom":
            y += h/2
        elif self.label.anchor_y == "top":
            y -= h/2

        return x, y

    def getDimensions(self):
        return self.label.content_width, self.label.content_height

    def getAnchoredDimensions(self):
        w, h = self.getDimensions()
        x, y = self.getPosition()
        x += self.label._get_left_anchor()
        y += self.label._get_bottom_anchor()
        return x, y, w, h

    def getRotation(self):
        return self.label.rotation

    def setRotation(self, rotation):
        self.label.rotation = rotation

    def getColor(self, RGBA=False):
        if RGBA:
            return self.label.color
        R, G, B, _ = self.label.color
        return R, G, B

    def updateColor(self, color):
        if len(color) == 4:
            self.label.color = color
            return
        R, G, B = color
        _, _, _, A = self.getColor(RGBA=True)
        self.updateColor((R, G, B, A))

    def getOpacity(self):
        _, _, _, opacity = self.getColor(RGBA=True)
        return opacity

    def setOpacity(self, opacity):
        R, G, B = self.getColor()
        self.updateColor((R, G, B, opacity))

    def getVisible(self):
        return self.label.visible

    def setVisible(self, visible):
        self.label.visible = visible

    def getScale(self):
        return 1

    def setScale(self, scale):
        pass

    def getFontSize(self):
        return self.scale*SettingsGlobal.Scale*SettingsGlobal.FontSize

    def getText(self):
        return self.label.text

    def setText(self, text):
        self.label.text = text
