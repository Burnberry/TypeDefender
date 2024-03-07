from Code.Util.GameObjects.GameObject import GameObject
from Code.Util.Visuals.Shapes import BoxShape


class BackgroundObject(GameObject):
    def __init__(self, scene, parent: GameObject, thickness=1):
        x, y = parent.visual.getCenter()
        w, h = parent.visual.getDimensions()
        w += 2*thickness
        h += 2*thickness

        visual = BoxShape(x, y, w, h, batch=scene.batch, group=scene.Group.Background)
        visual.setColor((100, 0, 0))
        super().__init__(scene, visual, x, y, parent)

    def update(self, dt):
        pass

    def onMessage(self, obj, message):
        pass

    def setPosition(self, x, y):
        x, y = self.parent.visual.getCenter()
        self.visual.setPosition(x, y)
