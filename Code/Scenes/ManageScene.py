from Code.Util.GameObjects.TextObject import TextObject
from Code.Util.ObjectLogic.Button import Button
from Code.Util.Scene import Scene


class ManageScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        obj = TextObject(self, "APPEL", *self.getCamera().getCenter())
        self.buttonBack = Button(obj, print, actionArgs=('test',))

    def update(self, dt):
        self.handleInput(dt)

    def handleInput(self, dt):
        self.updateButtons(dt)
        controller = self.getController()
        if controller.isControlPressed(controller.space):
            self.game.switchScene("wave")
