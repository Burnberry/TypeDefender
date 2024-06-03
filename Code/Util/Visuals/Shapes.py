from Code.Util.Visuals.ShapeVisual import ShapeVisual
import pyglet

from PygEdits.Shapes.MyShapes import MyRectangle, MyMultiLine


class CircleShape(ShapeVisual):
    def __init__(self, x, y, r, batch, group):
        circle = pyglet.shapes.Arc(x, y, r, batch=batch, group=group)
        self.r = r
        super().__init__(circle)

    def getDimensions(self):
        r = self.r
        return 2*r, 2*r

    def getAnchoredDimensions(self):
        r = self.r
        x, y = self.getPosition()
        return x-r, y-r, 2*r, 2*r


class RectangleShape(ShapeVisual):
    def __init__(self, x, y, w, h, batch, group):
        rectangle = pyglet.shapes.Box(x, y, w, h, batch=batch, group=group)
        rectangle.anchor_x, rectangle.anchor_y = w/2, h/2
        super().__init__(rectangle)


class BoxShape(ShapeVisual):
    def __init__(self, x, y, w, h, batch, group):
        box = MyRectangle(x, y, w, h, batch=batch, group=group)  # pyglet.shapes.Rectangle(x, y, w, h, batch=batch, group=group)
        box.anchor_x, box.anchor_y = w / 2, h / 2
        super().__init__(box)


class MultiLine(ShapeVisual):
    def __init__(self, points, ax, ay, batch, group, thickness=1, w=0, h=0):
        shape = MyMultiLine(*points, thickness=thickness, closed=True, batch=batch, group=group)
        shape.anchor_x, shape.anchor_y = ax, ay
        shape.width, shape.height = w, h
        super().__init__(shape)


class PolygonShape(ShapeVisual):
    def __init__(self, points, batch, group, w=0, h=0):
        shape = pyglet.shapes.Polygon(*points, batch=batch, group=group)
        shape.width, shape.height = w, h
        super().__init__(shape)

    def getAnchoredDimensions(self):
        w, h = self.getDimensions()
        x, y = self.getPosition()
        return x, y, w, h
