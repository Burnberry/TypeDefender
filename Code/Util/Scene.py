from abc import ABC, abstractmethod
from pyglet import graphics

import Code.Game
from Code.Util.Camera import Camera


class Scene(ABC):
    def __init__(self, game):
        self.game: Code.Game.Game = game
        self.gameState = self.game.gameState
        self.gameObjects, self.visualObjects = [], []
        self.buttons = set()

        # render stuff
        self.batch = graphics.Batch()
        self.window = game.window

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def handleInput(self, dt):
        pass

    def updateButtons(self, dt):
        for button in self.getOrderedButtons():
            if button.updateButton(dt):
                return

    def getOrderedButtons(self):
        """return copy of buttons, should return an ordered list instead, preferably saved"""
        return list(self.buttons)

    def draw(self):
        self.window.clear()
        self.batch.draw()
        self.window.flip()

    def clear(self):
        for visualObject in self.visualObjects:
            visualObject.remove()

    def setSwitchState(self, state):
        self.switchState = state

    def onSceneSwitch(self):
        pass

    def addGameObject(self, gameObject):
        self.gameObjects.append(gameObject)

    def addVisualObject(self, visualObject):
        self.visualObjects.append(visualObject)

    def addButton(self, button):
        self.buttons.add(button)

    def removeButton(self, button):
        if button in self.buttons:
            self.buttons.remove(button)

    def getCamera(self) -> Camera:
        return self.game.camera

    def getController(self):
        return self.game.controller

    def getMousePosition(self, gameCoordinates=True):
        x, y = self.getController().mousePosition
        if gameCoordinates:
            x, y = self.getCamera().screenToGameCoords(x, y)
        return x, y

    class Group:
        Background = graphics.Group(order=10)
        Foreground = graphics.Group(order=100)
        InnerBar = graphics.Group(order=210)
        OuterBar = graphics.Group(order=220)
        Text = graphics.Group(order=500)
        TextBackground = graphics.Group(order=450)

