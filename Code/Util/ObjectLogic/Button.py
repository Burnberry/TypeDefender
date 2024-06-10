from Code.Util.GameObjects.GameObject import GameObject


class Button:
    def __init__(self, gameObject, action, active=True, order=0, actionArgs=None, actionKwargs=None, check=lambda: True):
        self.gameObject = gameObject
        self.active = active
        self.order = order
        self.action = action
        self.actionArgs, self.actionKwargs = actionArgs or (), actionKwargs or {}
        self.check = check

        self.gameObject.scene.addButton(self)

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
        if self.hovered and controller.isControlPressed(controller.click) and self.check():
            self.action(*self.actionArgs, **self.actionKwargs)

        return self.hovered

    def checkHovered(self):
        x, y = self.gameObject.scene.getMousePosition()
        return self.gameObject.isInside(x, y)

    def highlight(self, on=True):
        self.gameObject.highlight(on)
