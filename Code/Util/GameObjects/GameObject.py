from abc import ABC, abstractmethod

from Code.Util.Controller import Controller
from Code.Util.Scene import Scene


class GameObject(ABC):
    def __init__(self, scene, visual, x=0, y=0, parent=None):
        self.removed = False
        self.scene: Scene = scene
        self.visual = visual
        self.scene.addGameObject(self)

        self.children: list[GameObject] = []

        self.listeners = set()

        self.setPosition(x, y)
        self.setParent(parent)

    @abstractmethod
    def update(self, dt):
        pass

    def remove(self):
        self.setRemoved(True)
        for listener in self.listeners:
            listener.onMessage(self, "removed")

        for child in self.children:
            child.remove()

        if self.visual:
            self.visual.remove()
            self.visual = None

    @abstractmethod
    def onMessage(self, obj, message):
        pass

    def getPosition(self):
        return self.x, self.y

    def setPosition(self, x, y):
        self.x, self.y = x, y
        sx, sy = self.scene.game.camera.gameToScreenCoords(x, y)

        self.visual.setPosition(sx, sy)

        for child in self.children:
            child.onParentSetPosition(x, y)

    def getDimensions(self):
        sw, sh = self.visual.getDimensions()
        return self.scene.game.camera.screenToGameCoords(sw, sh)

    def getAnchoredDimensions(self):
        sx, sy, sw, sh = self.visual.getAnchoredDimensions()
        x, y = self.scene.game.camera.screenToGameCoords(sx, sy)
        w, h = self.scene.game.camera.screenToGameCoords(sw, sh)
        return x, y, w, h

    def setRemoved(self, removed):
        self.removed = removed

    def addListener(self, listener):
        self.listeners.add(listener)

    def removeListener(self, listener):
        if listener in self.listeners:
            self.listeners.remove(listener)

    def addChild(self, child: 'GameObject'):
        self.children.append(child)
        child.onParentSetPosition(*self.getPosition())

    def setParent(self, parent: 'GameObject'):
        self.parent = parent
        if parent:
            parent.addChild(self)

    def onParentSetPosition(self, x, y):
        self.setPosition(x, y)

    def isInside(self, x, y):
        x0, y0, w, h = self.getAnchoredDimensions()
        if (x0 <= x <= x0+w) and (y0 <= y <= y0+h):
            return True
        for child in self.children:
            if child.isInside(x, y):
                return True
        return False

    def highlight(self, on=True):
        self.visual.highlight(on)
        for child in self.children:
            child.visual.highlight(on)

    def setColor(self, color, passOn=True):
        self.visual.setColor(color)
        if not passOn:
            return
        for child in self.children:
            child.setColor(color, passOn)

    def addColors(self, colors,  passOn=True):
        self.visual.addColors(colors)
        if not passOn:
            return
        for child in self.children:
            child.addColors(colors, passOn)