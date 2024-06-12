from Code.Util.GameObjects.BarObject import BarObject
from Code.Util.GameObjects.GameObject import GameObject
from Code.Util.GameObjects.LabelObject import LabelObject


class Building(GameObject):
    def __init__(self, scene, visual, x, y, word=""):
        super().__init__(scene, visual, x, y)
        self.word = word

        self.label = LabelObject(scene, self.word, self)
        self.label.setColor((255, 200, 0))

    def update(self, dt):
        pass

    def onMessage(self, obj, message):
        pass

    def onEnter(self, line):
        if line == self.word:
            self.onWordHit()

    def onWordHit(self):
        self.word = self.scene.wordGen.getWord()
        self.label.setText(self.word)

