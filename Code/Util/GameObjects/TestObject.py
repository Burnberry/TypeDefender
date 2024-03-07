from Code.Util.GameObjects.GameObject import GameObject


class TestObject(GameObject):
    def __init__(self, scene, visual, x, y):
        super().__init__(scene, visual, x, y)

    def update(self, dt):
        pass

    def onMessage(self, obj, message):
        pass
