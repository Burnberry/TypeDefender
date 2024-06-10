from abc import ABC, abstractmethod


class Visual(ABC):
    def __init__(self, colors=None, color=(255,255,255)):
        self.colors: dict[str, tuple[int, int, int]] = colors or {}
        self.color = color
        self.activeColor = color
        self.activeColorKey = False

    @abstractmethod
    def remove(self):
        pass

    @abstractmethod
    def getPosition(self):
        pass

    @abstractmethod
    def setPosition(self, x, y):
        pass

    def getCenter(self):
        return self.getPosition()

    @abstractmethod
    def getDimensions(self):
        pass

    @abstractmethod
    def getAnchoredDimensions(self):
        pass

    @abstractmethod
    def getRotation(self):
        pass

    @abstractmethod
    def setRotation(self, rotation):
        pass

    @abstractmethod
    def getColor(self):
        pass

    @abstractmethod
    def updateColor(self, color):
        pass

    @abstractmethod
    def getOpacity(self):
        pass

    @abstractmethod
    def setOpacity(self, opacity):
        pass

    @abstractmethod
    def getVisible(self):
        pass

    @abstractmethod
    def setVisible(self, visible):
        pass

    @abstractmethod
    def getScale(self):
        pass

    @abstractmethod
    def setScale(self, scale):
        pass

    def setColor(self, color):
        self.color = color
        if not self.activeColorKey:
            self.activeColor = self.color
        self._updateColor()

    def getActiveColor(self):
        return self.activeColor

    def _updateColor(self):
        color = self.getActiveColor()
        self.updateColor(color)

    def highlight(self, on=True):
        self.activateColor('highlight', on)

    def activateColor(self, colorKey, on=True):
        if on and self.colors.get(colorKey, False):
            self.activeColor = self.colors.get(colorKey)
            self.activeColorKey = colorKey
        elif not on:
            self.activeColor = self.color
            self.activeColorKey = False
        self._updateColor()

    def addColors(self, colors):
        self.colors.update(colors)
        if self.activeColorKey in colors:
            self.activateColor(self.activeColorKey)
