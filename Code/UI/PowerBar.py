from Code.Util.GameObjects.BarObject import BarObject
from Code.Util.SettingsGlobal import SettingsGlobal


class PowerBar(BarObject):
    def __init__(self, scene):
        x = SettingsGlobal.Width/2
        y = SettingsGlobal.Height/64
        w = SettingsGlobal.Width*3/4
        h = SettingsGlobal.Height/80
        super().__init__(scene, x, y, None, w, h, progress=0)

        self.innerBar.setColor((255, 255, 255))
