from Code.Util.GameObjects.BarObject import BarObject
from Code.Util.GameObjects.GameObject import GameObject
from Code.Util.GameObjects.LabelObject import LabelObject
from Code.Util.SettingsGlobal import SettingsGlobal
from Code.Util.Visuals.Shapes import CircleShape, MultiLine


class Base(GameObject):
    def __init__(self, scene):
        cx, cy = scene.game.camera.getCenter()
        cy /= 3
        visual = CircleShape(cx, cy, 10 * SettingsGlobal.Scale, scene.batch, scene.Group.Foreground)

        super().__init__(scene, visual, cx, cy)

        # self.bar = BarObject(scene, 0, 0, self)

        # self.labelObject = LabelObject(scene, "Base", self)

    def update(self, dt):
        return

    def onMessage(self, obj, message):
        pass
