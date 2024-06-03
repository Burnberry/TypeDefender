import math
import random

from Code.Util.GameObjects.GameObject import GameObject
from Code.Util.SettingsGlobal import SettingsGlobal
from Code.Util.Visuals.MultiVisual import MultiVisual
from Code.Util.Visuals.Shapes import PolygonShape


class Gem(GameObject):
    def __init__(self, scene, x, y, value=1, spread=8, color=(20, 220, 60)):
        self.color = color
        visual = MultiVisual(self.createVisuals(scene))
        super().__init__(scene, visual, x, y)

        self.value = value
        self.idleTime = 1

        angle, r = random.random(), random.random()*spread
        dx, dy = math.cos(r*2*math.pi), math.sin(r*2*math.pi)
        self.direction = dx, dy
        self.goal = x+dx*r, y+dy*r
        self.speed = 10*r

        self.state = "spread"

        self.scene.addGem(self)

    def update(self, dt):
        self.idleTime -= dt
        if self.state == "spread" or self.state == "collect":
            gx, gy = self.goal
            x, y = self.getPosition()

            dx, dy = self.direction
            dx, dy = dx*dt*self.speed, dy*dt*self.speed

            if abs(dx) >= abs(gx-x):
                self.setPosition(gx, gy)
                self.updateState()
            else:
                self.setPosition(x+dx, y+dy)
        elif self.state == "idle":
            if self.idleTime <= 0:
                self.updateState()

    def updateState(self):
        if self.state == "spread":
            self.state = "idle"
        elif self.state == "idle":
            self.speed = 150
            self.state = "collect"
            gx, gy = self.scene.base.getPosition()
            self.goal = gx, gy

            x, y = self.getPosition()
            dx, dy = gx-x, gy-y
            d = math.hypot(dx, dy)
            d = max(d, 0.0001)
            dx, dy = dx / d, dy / d
            self.direction = dx, dy

        elif self.state == "collect":
            self.state = "finish"
            self.scene.onGemCollected(self)
            self.remove()

    def onMessage(self, obj, message):
        pass

    def createVisuals(self, scene):
        scale = SettingsGlobal.Scale
        w, h = 1.5*scale, 2.25*scale
        visuals = []

        color = self.color
        points = [[0, 0], [w, 0], [0, h]]
        visual = PolygonShape(points, scene.batch, scene.Group.Foreground)
        visual.setColor(color)
        visuals.append(visual)

        d = 0.7
        r, g, b = self.color
        r, g, b = int(d*r), int(d*g), int(d*b)
        color = r, g, b

        points = [[0, 0], [-w, 0], [0, h]]
        visual = PolygonShape(points, scene.batch, scene.Group.Foreground)
        visual.setColor(color)
        visuals.append(visual)

        points = [[0, 0], [w, 0], [0, -h]]
        visual = PolygonShape(points, scene.batch, scene.Group.Foreground)
        visual.setColor(color)
        visuals.append(visual)

        d = 0.4
        r, g, b = self.color
        r, g, b = int(d*r), int(d*g), int(d*b)
        color = r, g, b

        points = [[0, 0], [-w, 0], [0, -h]]
        visual = PolygonShape(points, scene.batch, scene.Group.Foreground)
        visual.setColor(color)
        visuals.append(visual)

        return visuals
