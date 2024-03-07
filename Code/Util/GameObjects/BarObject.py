from Code.Util.GameObjects.GameObject import GameObject
from Code.Util.SettingsGlobal import SettingsGlobal
from Code.Util.Visuals.MultiVisual import MultiVisual
from Code.Util.Visuals.Shapes import RectangleShape, BoxShape


class BarObject(GameObject):
    def __init__(self, scene, x, y, parent=None, w=10, h=1.5, progress=1):
        self.w, self.h = w, h
        w *= SettingsGlobal.Scale
        h *= SettingsGlobal.Scale
        self.outerBar = RectangleShape(x, y, w, h, scene.batch, scene.Group.OuterBar)
        self.innerBar = BoxShape(x, y, w, h, scene.batch, scene.Group.InnerBar)
        self.innerBar.setColor((255, 0, 0))

        visual = MultiVisual([self.outerBar, self.innerBar], primaryVisual=self.outerBar)

        super().__init__(scene, visual, x, y, parent)

        if self.parent is not None:
            self.onParentSetPosition(*self.parent.getPosition())

        self.setProgress(progress)

    def update(self, dt):
        pass

    def onMessage(self, obj, message):
        pass

    def setProgress(self, progress):
        progress = min(progress, 1)
        self.progress = progress
        self.innerBar.shape.setXScale(progress)

    def onParentSetPosition(self, x, y):
        w, h = self.parent.getDimensions()
        y -= h/2 + self.h/2 + 0.5

        self.setPosition(x, y)

