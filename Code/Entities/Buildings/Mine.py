from Code.Entities.Buildings.Building import Building
from Code.Util.SettingsGlobal import SettingsGlobal
from Code.Util.Visuals.Shapes import RectangleShape


class Mine(Building):
    def __init__(self, scene, x, y):
        w, h = 15, 15
        w *= SettingsGlobal.Scale
        h *= SettingsGlobal.Scale

        visual = RectangleShape(x, y, w, h, scene.batch, scene.Group.Foreground)
        super().__init__(scene, visual, x, y)

        self.onWordHit()
