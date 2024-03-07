from Code.Entities.Enemy import Enemy
from Code.Util.SettingsGlobal import SettingsGlobal
from Code.Util.Visuals.Shapes import RectangleShape


class SquareEnemy(Enemy):
    def __init__(self, scene, x, y):
        w, h = 10, 10
        w *= SettingsGlobal.Scale
        h *= SettingsGlobal.Scale

        visual = RectangleShape(x, y, w, h, scene.batch, scene.Group.Foreground)

        super().__init__(scene, visual, x, y)

    def update(self, dt):
        super().update(dt)
