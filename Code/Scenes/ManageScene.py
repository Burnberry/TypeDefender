from Code.Factories.Factories import Factory
from Code.Upgrades.Upgrade import *
from Code.Util.GameObjects.BackgroundObject import BackgroundObject
from Code.Util.GameObjects.TextObject import TextObject
from Code.Util.ObjectLogic.Button import Button
from Code.Util.ObjectLogic.GemCounter import GemCounter
from Code.Util.Scene import Scene
from Code.Util.Visuals.Shapes import RectangleShape


class ManageScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.buttonBack = Factory.createButton(self, "back", 310, 170,  self.actionBack)

        self.upgrades = []
        for upgrade in [Damage]:
            self.upgrades.append(upgrade(self))

        self.gameState.listen('death', self.onDeath)

        self.gemCount = GemCounter(self)

        # self.buttonUpgradeDamage = Factory.createButton(self, "Damage Up", 160, 90,  self.actionUpgradeDamage, check=self.checkUpgradeDamage)
        # self.costUpgradeDamage = 1

    def update(self, dt):
        self.handleInput(dt)

    def onSceneSwitch(self):
        pass
        self.checkButtons()

    def onDeath(self, subject, value):
        for upgrade in self.upgrades:
            upgrade.reset()

    def handleInput(self, dt):
        self.updateButtons(dt)
        controller = self.getController()
        # if controller.isControlPressed(controller.space):
        #     self.game.switchScene("wave")

    def checkButtons(self):
        for button in self.buttons:
            if button.check():
                button.gameObject.setColor((255, 255, 255))
                button.gameObject.addColors({'highlight': (255, 255, 0)})
            else:
                button.gameObject.setColor((100, 100, 100))
                button.gameObject.addColors({'highlight': (100, 100, 100)})

    def spend(self, gems):
        self.game.gameState.gems -= gems
        self.checkButtons()

    def actionBack(self):
        self.game.switchScene("wave")

    def actionUpgradeDamage(self):
        if self.checkUpgradeDamage():
            print("dmg +1")
            self.spend(self.costUpgradeDamage)

    def checkUpgradeDamage(self):
        return self.game.gameState.gems >= self.costUpgradeDamage
