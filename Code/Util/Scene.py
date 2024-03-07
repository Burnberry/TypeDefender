from abc import ABC, abstractmethod
from pyglet import graphics

import Code.Game


class Scene(ABC):
    def __init__(self, game):
        self.game: Code.Game.Game = game
        self.switchState = None
        self.gameObjects, self.visualObjects = [], []

        # render stuff
        self.batch = graphics.Batch()
        self.window = game.window

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def handleInput(self, dt):
        pass

    def draw(self):
        self.window.clear()
        self.batch.draw()
        self.window.flip()

    def clear(self):
        for visualObject in self.visualObjects:
            visualObject.remove()

    def setSwitchState(self, state):
        self.switchState = state

    def addGameObject(self, gameObject):
        self.gameObjects.append(gameObject)

    def addVisualObject(self, visualObject):
        self.visualObjects.append(visualObject)

    def getController(self):
        return self.game.controller

    class Group:
        Background = graphics.Group(order=10)
        Foreground = graphics.Group(order=100)
        InnerBar = graphics.Group(order=210)
        OuterBar = graphics.Group(order=220)
        Text = graphics.Group(order=500)
        TextBackground = graphics.Group(order=450)

