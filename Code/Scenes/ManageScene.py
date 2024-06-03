from Code.Util.GameObjects.BackgroundObject import BackgroundObject
from Code.Util.GameObjects.TextObject import TextObject
from Code.Util.ObjectLogic.Button import Button
from Code.Util.Scene import Scene
from Code.Util.Visuals.Shapes import RectangleShape


class ManageScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        obj = TextObject(self, "APPEL", *self.getCamera().getCenter())
        BackgroundObject(self, obj, shape=RectangleShape, x_offset=3)
        self.buttonBack = Button(obj, self.buttonPress)

    def update(self, dt):
        self.handleInput(dt)

    def handleInput(self, dt):
        self.updateButtons(dt)
        controller = self.getController()
        if controller.isControlPressed(controller.space):
            self.game.switchScene("wave")

    def buttonPress(self):
        print(self.game.gameState.gems)
