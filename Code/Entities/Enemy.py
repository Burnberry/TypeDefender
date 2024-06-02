from Code.Entities.Gem import Gem
from Code.Util.GameObjects.BarObject import BarObject
from Code.Util.GameObjects.GameObject import GameObject
from Code.Util.GameObjects.LabelObject import LabelObject


class Enemy(GameObject):
    def __init__(self, scene, visual, x, y, maxSpeed=15, health=1):
        super().__init__(scene, visual, x, y)
        self.maxSpeed = maxSpeed
        self.speed = maxSpeed
        self.maxHealth = health
        self.health = self.maxHealth

        self.word = ""
        self.goal = self.getTargetLocation()

        self.label = LabelObject(scene, self.word, self)
        self.bar = BarObject(scene, 0, 0, self)

        self.setNewWord()

    def update(self, dt):
        x, y = self.getPosition()

        dx, dy = self.getDirection()
        dx, dy = dt * self.speed * dx, dt * self.speed * dy

        self.setPosition(x + dx, y + dy)
        self.checkCollision()

    def onMessage(self, obj, message):
        pass

    def getHealth(self):
        return self.health

    def setHealth(self, health):
        self.health = max(0, health)
        self.bar.setProgress(self.health/self.maxHealth)

    def getDirection(self):
        x, y = self.getPosition()
        gx, gy = self.goal

        dx, dy = gx - x, gy - y
        d = (dx ** 2 + dy ** 2) ** (1 / 2)
        dx, dy = dx / d, dy / d
        return dx, dy

    def onAttackedByLine(self):
        self.onAttacked(1)
        if self.getHealth() > 0:
            self.setNewWord()

    def onAttacked(self, damage):
        self.setHealth(self.getHealth() - damage)
        if self.getHealth() <= 0:
            self.onKilled()

    def onKilled(self):
        self.scene.onEnemyKilled(self)
        for i in range(3):
            Gem(self.scene, *self.getPosition())
        self.onDied()

    def onDied(self):
        self.scene.onEnemyDied(self)
        self.remove()

    def getWord(self):
        return self.word

    def setWord(self, word):
        self.word = word
        self.label.setText(self.word)

    def getNewWord(self):
        return self.scene.wordGen.getWord()

    def setNewWord(self):
        word = self.getNewWord()
        self.setWord(word)

    def getTargetLocation(self):
        return self.scene.base.getPosition()

    def checkCollision(self):
        if self.isCollidingWithBase():
            self.onDied()
            self.scene.onBaseAttack()

    def isCollidingWithBase(self):
        x1, y1 = self.scene.base.getPosition()
        x, y = self.getPosition()
        dx, dy = x - x1, y - y1

        w, h = self.getDimensions()
        dx = min([dx, dx - w / 2, dx + w / 2])
        dy = min([dy, dy - h / 2, dy + h / 2])

        d, _ = self.scene.base.getDimensions()

        return dx**2 + dy**2 <= d**2
