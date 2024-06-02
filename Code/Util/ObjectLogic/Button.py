from Code.Util.GameObjects.GameObject import GameObject


class Button:
    def __init__(self, gameObject, action, active=True, order=0, actionArgs=None, actionKwargs=None):
        self.gameObject = gameObject
        self.action = action
        self.active = active
        self.order = order
        self.actionArgs, self.actionKwargs = actionArgs or (), actionKwargs or {}

        self.gameObject.scene.addButton(self)
        self.gameObject.addChild(self)

        self.hovered = self.checkHovered()
        if self.hovered:
            self.highlight()

    def remove(self):
        self.gameObject.scene.removeButton(self)

    def updateButton(self, dt):
        if not self.active:
            return False

        hovered = self.checkHovered()
        if self.hovered != hovered:
            self.hovered = hovered
            self.highlight(self.hovered)

        controller = self.gameObject.scene.getController()
        if controller.isControlPressed(controller.click): print("appel", self.hovered)
        if self.hovered and controller.isControlPressed(controller.click):
            self.action(*self.actionArgs, **self.actionKwargs)

        return self.hovered

    def checkHovered(self):
        x, y = self.gameObject.scene.getMousePosition()
        return self.gameObject.isInside(x, y)

    def highlight(self, on=True):
        self.gameObject.visual.highlight(on)
