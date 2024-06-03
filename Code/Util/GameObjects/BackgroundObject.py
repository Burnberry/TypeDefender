from Code.Util.GameObjects.GameObject import GameObject
from Code.Util.Visuals.Shapes import BoxShape


class BackgroundObject(GameObject):
    def __init__(self, scene, parent: GameObject, x_offset=1, y_offset=1, shape=BoxShape, *args):
        x, y, w, h = parent.visual.getAnchoredDimensions()
        camera = scene.getCamera()
        x_offset, y_offset = camera.gameToScreenCoords(x_offset, y_offset)
        x -= x_offset
        y -= y_offset
        w += x_offset
        h += y_offset

        visual = shape(x, y, w, h, batch=scene.batch, group=scene.Group.Background, *args)
        super().__init__(scene, visual, x, y, parent=parent)

    def update(self, dt):
        pass

    def onMessage(self, obj, message):
        pass

    def setPosition(self, x, y):
        x, y = self.parent.visual.getCenter()
        self.visual.setPosition(x, y)
