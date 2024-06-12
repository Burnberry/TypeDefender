from Code.Util.GameObjects.TextObject import TextObject


class GemCounter:
    def __init__(self, scene):
        self.scene = scene
        self.gameState = scene.gameState

        self.obj = TextObject(scene, "", 10, 10)
        self.updateGemCount("gems", self.gameState.getValue("gems"))
        self.gameState.listen("gems", self.updateGemCount)

    def updateGemCount(self, subject, count):
        self.obj.setText(str(count))
