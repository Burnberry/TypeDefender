from abc import ABC, abstractmethod


class Visual(ABC):
    def __init__(self):
        pass

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
    def getRotation(self):
        pass

    @abstractmethod
    def setRotation(self, rotation):
        pass

    @abstractmethod
    def getColor(self):
        pass

    @abstractmethod
    def setColor(self, color):
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
