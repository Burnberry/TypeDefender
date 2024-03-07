import math
import random

from Code.Entities.Enemy import Enemy
from Code.Util.SettingsGlobal import SettingsGlobal
from Code.Util.Visuals.Shapes import RectangleShape, MultiLine


def degreeAngle(dx, dy):
    return -math.degrees(math.atan2(dy, dx))


class TriangleEnemy(Enemy):
    def __init__(self, scene, x, y):
        w, h = 10, 10
        w *= SettingsGlobal.Scale
        h *= SettingsGlobal.Scale

        points = [[0, 0], [0, h], [w, h/2]]
        ax, ay = w/3, h/2
        visual = MultiLine(points, ax, ay, scene.batch, scene.Group.Foreground, w=w*1.4, h=h*1.4)

        self.moveState = "rotate"
        self.state = "move"
        self.rotateSpeed = 100
        self.acceleration = 5
        self.slowdown = 0.1
        self.idleDelay, self.idleTime = 1, 0

        super().__init__(scene, visual, x, y)
        self.setPosition(160, 100)
        self.speed = 0
        self.setAttackSpot()
        gx, gy = self.goal
        self.setDirection(gx-x, gy-y)

    def update(self, dt):
        self.speed *= 1 - self.slowdown*dt

        if self.moveState == "idle":
            self.updateIdle(dt)
        elif self.moveState == "rotate":
            self.updateRotate(dt)
        elif self.moveState == "accelerate":
            self.updateAccelerate(dt)
        elif self.moveState == "brake":
            self.updateBrake(dt)

        super().update(dt)

    def getDirection(self):
        return self.direction

    def setDirection(self, dx, dy):
        d = math.hypot(dx, dy)
        dx /= d
        dy /= d

        self.direction = (dx, dy)
        self.visual.setRotation(degreeAngle(dy, dx))

    def attack(self):
        print("pew pew")

    def updateMoveState(self):
        if self.state == "move":
            if self.moveState == "idle":
                self.moveState = "rotate"
            elif self.moveState == "rotate":
                self.moveState = "accelerate"
            elif self.moveState == "accelerate":
                self.moveState = "brake"
            elif self.moveState == "brake":
                self.state = "attack"
                self.moveState = "rotate"
                self.goal = self.scene.base.getPosition()
            return

        if self.state == "attack":
            if self.moveState == "rotate":
                self.moveState = "idle"
            elif self.moveState == "idle":
                self.attack()
                self.setAttackSpot()
                self.state = "move"

    def updateIdle(self, dt):
        self.idleTime += dt

        if self.idleTime > self.idleDelay:
            self.idleTime = 0
            self.updateMoveState()

    def updateRotate(self, dt):
        gx, gy = self.goal
        dx, dy = self.getDirection()

        ga, a = degreeAngle(gx, gy), degreeAngle(dx, dy)

        if abs(ga - a) < min(abs(ga - 360 - a), abs(ga + 360 - a)):
            da = ga-a
        elif abs(ga - 360 - a) < abs(ga + 360 - a):
            da = ga - 360 - a
        else:
            da = ga + 360 - a

        sign = [-1, 1][da > 0]
        dw = sign*self.rotateSpeed*dt
        if abs(dw) > abs(da):
            dw = da
            self.updateMoveState()
        print(self.moveState, self.state, self.goal, self.getPosition(), dw, da, a)

        dx, dy = math.cos(math.radians((a+dw))), math.sin(-math.radians((a+dw)))
        self.setDirection(dx, dy)

    def updateAccelerate(self, dt):
        x, y = self.getPosition()
        gx, gy = self.goal
        if abs(gx-x) + abs(gy-y) < 3:
            self.updateMoveState()
            return
        self.speed += self.acceleration*dt

    def updateBrake(self, dt):
        self.speed -= self.acceleration*7*dt
        if self.speed < 0:
            self.speed = 0
            self.updateMoveState()

    def setAttackSpot(self):
        y = 150
        x = random.randint(20, 300)
        self.goal = (x, y)
