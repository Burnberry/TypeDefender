from Code.Util.GameObjects.BackgroundObject import BackgroundObject
from Code.Util.GameObjects.TextObject import TextObject
from Code.Util.ObjectLogic.Button import Button
from Code.Util.Visuals.Shapes import RectangleShape


class Factory:
    @staticmethod
    def createButton(scene, name, x, y, action, check=lambda: True):
        obj = TextObject(scene, name, x, y)
        obj2 = BackgroundObject(scene, obj, shape=RectangleShape, x_offset=3)
        return Button(obj, action, check=check)
