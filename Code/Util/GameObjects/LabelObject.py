from Code.Util.GameObjects.GameObject import GameObject
from Code.Util.GameObjects.TextObject import TextObject


class LabelObject(TextObject):
    def __init__(self, scene, text, parent: GameObject, anchorParentX="center", anchorParentY="top"):
        self.anchorParent = (anchorParentX, anchorParentY)
        anchorX, anchorY = self.getAnchor()
        super().__init__(scene, text, 0, 0, parent, anchorX=anchorX, anchorY=anchorY)

        self.onParentSetPosition(*parent.getPosition())

    def onParentSetPosition(self, x, y):
        w, h = self.parent.getDimensions()
        dx, dy = 0, 0
        anchorParentX, anchorParentY = self.anchorParent

        if anchorParentX == "left":
            dx -= w/2
        elif anchorParentX == "right":
            dx += w/2

        if anchorParentY == "bottom":
            dy -= h/2
        elif anchorParentY == "top":
            dy += h/2

        self.setPosition(x+dx, y+dy)

    def getAnchor(self):
        anchorX, anchorY = self.anchorParent

        if anchorX == "left":
            anchorX = "right"
        elif anchorX == "right":
            anchorX = "left"

        if anchorY == "top":
            anchorY = "bottom"
        elif anchorY == "bottom":
            anchorY = "top"

        return anchorX, anchorY
