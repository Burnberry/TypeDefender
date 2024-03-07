from abc import ABC, abstractmethod


class GameObject(ABC):
    def __init__(self, scene, visual, x=0, y=0, parent=None):
        self.removed = False
        self.scene = scene
        self.visual = visual
        self.scene.addGameObject(self)

        self.setParent(parent)
        self.children: list[GameObject] = []

        self.listeners = set()

        self.setPosition(x, y)

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

    def setRemoved(self, removed):
        self.removed = removed

    def addListener(self, listener):
        self.listeners.add(listener)

    def removeListener(self, listener):
        if listener in self.listeners:
            self.listeners.remove(listener)

    def addChild(self, child: 'GameObject'):
        self.children.append(child)

    def setParent(self, parent: 'GameObject'):
        self.parent = parent
        if parent:
            parent.addChild(self)

    def onParentSetPosition(self, x, y):
        self.setPosition(x, y)
