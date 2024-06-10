from Code.Factories.Factories import Factory


class Upgrade:
    def __init__(self, scene, name, x, y, baseCost=0, level=1):
        self.scene = scene
        self.name = name
        self.cost, self.baseCost = baseCost, baseCost
        self.level, self.baseLevel = level, level
        self.updateCost()

        self.button = Factory.createButton(scene, name, x, y, self.action, self.check)
        self.gameState = self.scene.game.gameState
        self.gameState.setValue(self.name, self.level)
        self.gameState.listen('gems', self.call)

    def call(self, subject, message):
        if subject == 'gems':
            self.button.check()

    def action(self):
        self.level += 1
        self.updateCost()
        self.gameState.setValue('gems', self.gameState.getValue('gems') - self.cost)
        self.gameState.setValue(self.name, self.level)

        button = self.button
        if button.check():
            button.gameObject.setColor((255, 255, 255))
            button.gameObject.addColors({'highlight': (255, 255, 0)})
        else:
            button.gameObject.setColor((100, 100, 100))
            button.gameObject.addColors({'highlight': (100, 100, 100)})

    def check(self):
        return self.gameState.getValue('gems') >= self.cost

    def updateCost(self):
        self.cost = self.level*self.baseCost

    def reset(self):
        self.level = self.baseLevel
        self.gameState.setValue(self.name, self.level)


class Damage(Upgrade):
    def __init__(self, scene):
        super().__init__(scene, 'damage', 160, 90, 5)
