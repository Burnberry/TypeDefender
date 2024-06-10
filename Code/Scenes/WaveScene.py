import math
import random

from pyglet.shapes import Line, BezierCurve, Box

from Code.Entities.Base import Base
from Code.Entities.Enemies.SquareEnemy import SquareEnemy
from Code.Entities.Enemies.TriangleEnemy import TriangleEnemy
from Code.Logic.WaveHandler import WaveHandler
from Code.Logic.WordGen import WordGen
from Code.UI.PowerBar import PowerBar
from Code.Util.GameObjects.TestObject import TestObject
from Code.Util.GameObjects.TextObject import TextObject
from Code.Util.Scene import Scene
from Code.Util.SettingsGlobal import SettingsGlobal
from Code.Util.Visuals.Shapes import MultiLine
from PygEdits.Shapes.MyShapes import MyMultiLine


class WaveScene(Scene):

    def __init__(self, game):
        super().__init__(game)
        self.inputLine = ""
        self.enemies = []
        self.gems = []
        self.base = None
        self.powerBar = None
        self.power, self.maxPower = 0, 100

        ### upgrades
        self.gameState.listen('damage', self.onUpgrade)
        self.damage = self.gameState.getValue('damage')

        self.wordGen = WordGen()
        self.waveHandler = WaveHandler(self)

        self.start()

    def start(self):
        self.inputLine = ""
        self.enemies = []
        self.gems = []
        self.base = None
        self.line = None
        self.isDead = False
        self.power = 0

        self.createBase()
        self.powerBar = PowerBar(self)
        for i in range(0):
            self.spawnEnemy()

    def restart(self):
        print("you died")
        self.clear()
        self.start()

    def clear(self):
        for enemy in self.enemies:
            enemy.remove()
        for gem in self.gems:
            gem.remove()
        self.base.remove()
        self.powerBar.remove()
        self.line.remove()

    def update(self, dt):
        self.base.update(dt)
        for enemy in self.enemies:
            enemy.update(dt)
        for gem in self.gems:
            gem.update(dt)
        self.waveHandler.update(dt)

        self.handleInput(dt)

        self.updateEnd(dt)

    def handleInput(self, dt):
        controller = self.getController()
        if len(controller.getText()) > 0:
            self.inputLine += controller.getText()
            self.onTextChanged()
        if controller.isControlPressed(controller.backspace):
            if len(self.inputLine) > 0:
                self.inputLine = self.inputLine[:-1]
                self.onTextChanged()
        if controller.isControlPressed(controller.space):
            self.powerPressed()
        if controller.isControlPressed(controller.enter):
            self.onEnter()

    def updateEnd(self, dt):
        if self.isDead:
            self.restart()

    def onTextChanged(self):
        self.inputLine = self.inputLine.replace('\r', '').replace(' ', '')
        self.line.setText(self.inputLine)

    def onEnter(self):
        self.onAttack(self.inputLine)

        self.inputLine = ""
        self.onTextChanged()

    def onAttack(self, line):
        enemies = [enemy for enemy in self.enemies]
        for enemy in enemies:
            if enemy.getWord() == line:
                enemy.onAttackedByLine(self.damage)

    def onBaseAttack(self):
        self.gameState.setValue('death', True)
        self.isDead = True

    def onEnemyKilled(self, enemy):
        self.addPower(10)

    def onEnemyDied(self, enemy):
        self.enemies.remove(enemy)

    def onGemCollected(self, gem):
        self.gems.remove(gem)
        self.game.gameState.setValue('gems', self.game.gameState.getValue('gems') + gem.value)

    def addGem(self, gem):
        self.gems.append(gem)

    def onUpgrade(self, upgrade, value):
        if upgrade == 'damage':
            self.damage = value


    def setPower(self, power):
        self.power = power
        self.powerBar.setProgress(self.power / self.maxPower)

    def addPower(self, energy):
        self.power += energy
        self.setPower(min(self.power, self.maxPower))

    def powerPressed(self):
        if self.power >= self.maxPower or True:
            self.setPower(0)
            self.game.switchScene("manage")

    def spawnEnemy(self):
        w, h = SettingsGlobal.Width, SettingsGlobal.Height
        p = random.random()*(w+2*h*(1/2))
        delta = 10

        if p < h:
            if p < h/2:
                x = -delta
                y = h/2 + p
            else:
                y = p
                x = w + delta
        else:
            x = p - h
            y = h + delta

        self.enemies.append(SquareEnemy(self, x, y))

    def createBase(self):
        self.base = Base(self)
        self.line = TextObject(self, "APPEL", 0, 0)
        _, h = self.line.getDimensions()
        x, y = self.base.getPosition()
        _, d = self.base.getDimensions()
        self.line.setPosition(x, y - h - d / 2 - 2.5)
        self.line.setText("")

    def createTest(self):
        self.testLine = Line(100, 100, 150, 100, width=10, batch=self.batch, group=self.Group.Foreground)

        self.test2 = MyMultiLine([200, 100], [250, 100], [250, 150], batch=self.batch, group=self.Group.Foreground, thickness=10)
        self.test2.anchor_y = 20
        self.test3 = Line(200, 120, 250, 120, batch=self.batch, group=self.Group.Foreground, width=10)

        self.test3 = Box(300, 120, 50, 40, batch=self.batch, group=self.Group.Foreground, thickness=10)


        self.testObjects = []

        # points = [[0, 0], [50, 50], [100, 0], [50, -50], [0, 0], [50, 50], [100, 0]]
        points = []
        r1, r2 = 30, 50
        n = 10
        for i in range(n+3):
            r = [r1, r2][i%2]
            x = r*math.cos(2*math.pi*(i/n))
            y = r*math.sin(2 * math.pi * (i / n))
            points += [[x, y]]

        points = []
        r1, r2 = 30, 50
        n = 5
        for i in range(n):
            x = r2 * math.cos(0.1 + 4 * math.pi * (i / n))
            y = r2 * math.sin(0.1 + 4 * math.pi * (i / n))
            points += [[x, y]]

        visual = MultiLine(points, self.batch, self.Group.Foreground, widthLeft=5, widthRight=0)
        visual.setColor((255, 0, 0))
        self.testObjects.append(TestObject(self, visual, 50, 100))

        visual = MultiLine(points, self.batch, self.Group.Foreground, widthLeft=0.5, widthRight=0.5)
        self.testObjects.append(TestObject(self, visual, 80, 100))

        visual = MultiLine(points, self.batch, self.Group.Foreground, widthLeft=0, widthRight=5)
        visual.setColor((0, 255, 0))
        self.testObjects.append(TestObject(self, visual, 110, 100))

        visual = MultiLine(points, self.batch, self.Group.Foreground, widthLeft=5, widthRight=0)
        visual.setColor((255, 0, 0))
        self.testObjects.append(TestObject(self, visual, 80, 70))

        visual = MultiLine(points, self.batch, self.Group.Foreground, widthLeft=0, widthRight=5)
        visual.setColor((0, 255, 0))
        self.testObjects.append(TestObject(self, visual, 80, 70))

        visual = MultiLine(points, self.batch, self.Group.Foreground, widthLeft=0.5, widthRight=0.5)
        self.testObjects.append(TestObject(self, visual, 80, 70))

        points = []
        r1, r2 = 30, 50
        n = 5
        for i in range(n + 3):
            x = r2 * math.cos(4 * math.pi * (i / n))
            y = r2 * math.sin(4 * math.pi * (i / n))
            points += [[x, y]]

            x = r2 * math.cos(math.pi/3 + 2 * math.pi * (i / n))
            y = r2 * math.sin(math.pi/3 + 2 * math.pi * (i / n))
            #points += [[x, y]]
        print(points)

        visual = MultiLine(points, self.batch, self.Group.Foreground, widthLeft=1, widthRight=0)
        self.testObjects.append(TestObject(self, visual, 200, 100))


