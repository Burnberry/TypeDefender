from Code.Util.GameObjects.GameObject import GameObject
from Code.Util.Visuals.LabelVisual import LabelVisual


class TextObject(GameObject):
    def __init__(self, scene, text, x, y, parent=None, anchorX="center", anchorY="bottom"):
        self.text = text
        visual = LabelVisual(x, y, self.getDisplayText(), scene.batch, scene.Group.Text, anchorX=anchorX, anchorY=anchorY)
        visual.colors['highlight'] = (255, 255, 0)
        super().__init__(scene, visual, x, y, parent)

    def update(self, dt):
        pass

    def onMessage(self, obj, message):
        pass

    def getText(self):
        return self.text

    def setText(self, text):
        self.text = text

        self.visual: LabelVisual
        self.visual.setText(self.getDisplayText())

    def getDisplayText(self):
        return self.getText()
