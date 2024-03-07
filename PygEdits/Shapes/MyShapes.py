import math

import pyglet
from pyglet.gl import GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
from pyglet.graphics import Batch
from pyglet.math import Vec2
from pyglet.shapes import ShapeBase, Rectangle, vertex_source, fragment_source


def get_default_shader():
    return pyglet.gl.current_context.create_program((vertex_source, 'vertex'),
                                                    (fragment_source, 'fragment'))


def _get_segment(p0, p1, p2, p3, thickness=1, prev_miter=None, prev_scale=None):
    """Computes a line segment between the points p1 and p2.

    If points p0 or p3 are supplied then the segment p1->p2 will have the correct "miter" angle
    for each end respectively.  This returns computed miter and scale values which can be supplied
    to the next call of the method for a minor performance improvement.  If they are not supplied
    then they will be computed.

    :Parameters:
        `p0` : (float, float)
            The "previous" point for the segment p1->p2 which is used to compute the "miter"
            angle of the start of the segment.  If None is supplied then the start of the line
            is 90 degrees to the segment p1->p2.
        `p1` : (float, float)
            The origin of the segment p1->p2.
        `p2` : (float, float)
            The end of the segment p1->p2
        `p3` : (float, float)
            The "following" point for the segment p1->p2 which is used to compute the "miter"
            angle to the end of the segment.  If None is supplied then the end of the line is
            90 degrees to the segment p1->p2.
        `prev_miter`: pyglet.math.Vec2
            The miter value to be used.

    :type: (pyglet.math.Vec2, pyglet.math.Vec2, float, float, float, float, float, float)
    """
    v_np1p2 = Vec2(p2[0] - p1[0], p2[1] - p1[1]).normalize()
    v_normal = Vec2(-v_np1p2.y,v_np1p2.x)

    # Prep the miter vectors to the normal vector in case it is only one segment
    v_miter2 = v_normal
    scale1 = scale2 = thickness / 2.0

    # miter1 is either already computed or the normal
    v_miter1 = v_normal
    if prev_miter and prev_scale:
        v_miter1 = prev_miter
        scale1 = prev_scale
    elif p0:
        # Compute the miter joint vector for the start of the segment
        v_np0p1 = Vec2(p1[0] - p0[0], p1[1] - p0[1]).normalize()
        v_normal_p0p1 = Vec2(-v_np0p1.y,v_np0p1.x)
        # Add the 2 normal vectors and normalize to get miter vector
        v_miter1 = Vec2(v_normal_p0p1.x + v_normal.x, v_normal_p0p1.y + v_normal.y).normalize()
        scale1 = scale1 / math.sin(math.acos(v_np1p2.dot(v_miter1)))

    if p3:
        # Compute the miter joint vector for the end of the segment
        v_np2p3 = Vec2(p3[0] - p2[0], p3[1] - p2[1]).normalize()
        v_normal_p2p3 = Vec2(-v_np2p3.y,v_np2p3.x)
        # Add the 2 normal vectors and normalize to get miter vector
        v_miter2 = Vec2(v_normal_p2p3.x + v_normal.x, v_normal_p2p3.y + v_normal.y).normalize()
        scale2 = scale2 / math.sin(math.acos(v_np2p3.dot(v_miter2)))

    # Make these tuples instead of Vec2 because accessing
    # members of Vec2 is suprisingly slow
    miter1ScaledP = (v_miter1.x * scale1, v_miter1.y * scale1)
    miter2ScaledP = (v_miter2.x * scale2, v_miter2.y * scale2)

    v1 = (p1[0] + miter1ScaledP[0], p1[1] + miter1ScaledP[1])
    v2 = (p2[0] + miter2ScaledP[0], p2[1] + miter2ScaledP[1])
    v3 = (p1[0] - miter1ScaledP[0], p1[1] - miter1ScaledP[1])
    v4 = (p2[0] + miter2ScaledP[0], p2[1] + miter2ScaledP[1])
    v5 = (p2[0] - miter2ScaledP[0], p2[1] - miter2ScaledP[1])
    v6 = (p1[0] - miter1ScaledP[0], p1[1] - miter1ScaledP[1])

    return (v_miter2, scale2, v1[0], v1[1], v2[0], v2[1], v3[0], v3[1], v4[0], v4[1], v5[0], v5[1], v6[0], v6[1])


class MyRectangle(Rectangle):
    def __init__(self, x, y, width, height, color=(255, 255, 255, 255),
                 batch=None, group=None):
        super().__init__(x, y, width, height, color, batch, group)

        self.originalsSet = False
        self.setOriginalValues(False)

        self.xScale, self.yScale = 1.0, 1.0

    def setOriginalValues(self, first=True):
        self.w0 = self._width
        self.h0 = self._height
        self.ax = self._anchor_x
        self.ay = self._anchor_y

        self.originalsSet = first

    def setXScale(self, scale):
        if not self.originalsSet:
            self.setOriginalValues()

        self.xScale = scale

        self._width = self.w0 * scale
        #self._x = self._x + self._anchor_x + 100
        # self._anchor_x = self.ax * scale
        #self._x = self._x - self._anchor_x

        self._update_vertices()
        #self._update_translation()

    def setYScale(self, scale):
        self.yScale = scale

        self._height = self.h0 * scale
        self._y -= self._anchor_y
        self._anchor_y = self.ay * scale
        self._y += self._anchor_y

        self._update_vertices()
        self._update_translation()


class MyMultiLine(ShapeBase):
    def __init__(self, *coordinates, closed=False, thickness=1, color=(255, 255, 255, 255), batch=None, group=None):
        """Create multiple connected lines from a sequence of coordinates

        The shape's anchor point defaults to the first vertex point.

        :Parameters:
            `coordinates` : List[[int, int]]
                The coordinates for each point in the polygon.
            `closed` : bool
                If True, the first and last coordinate will be connected with a line.
                defaults to False.
            `thickness` : float
                The desired thickness or width of the line used for the arc.
            `color` : (int, int, int, int)
                The RGB or RGBA color of the polygon, specified as a
                tuple of 3 or 4 ints in the range of 0-255. RGB colors
                will be treated as having an opacity of 255.
            `batch` : `~pyglet.graphics.Batch`
                Optional batch to add the polygon to.
            `group` : `~pyglet.graphics.Group`
                Optional parent group of the polygon.
        """
        # len(self._coordinates) = the number of vertices in the shape.
        self._thickness = thickness
        self._closed = closed
        self._rotation = 0
        self._coordinates = list(coordinates)
        if closed:
            # connect final point with first
            self._coordinates.append(self._coordinates[0])
        self._x, self._y = self._coordinates[0]
        self._num_verts = (len(self._coordinates) - 1) * 6

        r, g, b, *a = color
        self._rgba = r, g, b, a[0] if a else 255

        program = get_default_shader()
        self._batch = batch or Batch()
        self._group = self.group_class(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, program, group)

        self._create_vertex_list()

    def _create_vertex_list(self):
        self._vertex_list = self._group.program.vertex_list(
            self._num_verts, self._draw_mode, self._batch, self._group,
            position=('f', self._get_vertices()),
            colors=('Bn', self._rgba * self._num_verts),
            translation=('f', (self._x, self._y) * self._num_verts))

    def _get_vertices(self):
        if not self._visible:
            return (0, 0) * self._num_verts
        else:
            trans_x, trans_y = self._coordinates[0]
            trans_x += self._anchor_x
            trans_y += self._anchor_y
            coords = [[x - trans_x, y - trans_y] for x, y in self._coordinates]

            # Create a list of triangles from segments between 2 points:
            triangles = []
            prev_miter = None
            prev_scale = None
            for i in range(len(coords) - 1):
                prevPoint = None
                nextPoint = None
                if i > 0:
                    prevPoint = coords[i - 1]

                if i + 2 < len(coords):
                    nextPoint = coords[i + 2]

                prev_miter, prev_scale, *segment = _get_segment(prevPoint, coords[i], coords[i + 1], nextPoint,
                                                                self._thickness, prev_miter, prev_scale)
                triangles.extend(segment)

            return triangles

    def _update_vertices(self):
        self._vertex_list.position[:] = self._get_vertices()

    @property
    def thickness(self):
        return self._thickness

    @thickness.setter
    def thickness(self, thickness):
        self._thickness = thickness
        self._update_vertices()


class MyMultiLineOld(ShapeBase):
    def __init__(self, *coordinates, thickness_left=20, thickness_right=0, color=(255, 255, 255, 255), batch=None, group=None):
        """Create multiple connected lines from a sequence of coordinates

        The shape's anchor point defaults to the first vertex point.

        :Parameters:
            `coordinates` : List[[int, int]]
                The coordinates for each point in the polygon.
            `color` : (int, int, int, int)
                The RGB or RGBA color of the polygon, specified as a
                tuple of 3 or 4 ints in the range of 0-255. RGB colors
                will be treated as having an opacity of 255.
            `batch` : `~pyglet.graphics.Batch`
                Optional batch to add the polygon to.
            `group` : `~pyglet.graphics.Group`
                Optional parent group of the polygon.
        """

        # len(self._coordinates) = the number of vertices in the shape.
        self.thickness_left = thickness_left
        self.thickness_right = thickness_right
        self._rotation = 0
        self._coordinates = list(coordinates)
        self._x, self._y = self._coordinates[0]
        self._num_verts = (len(self._coordinates)-3) * 6

        r, g, b, *a = color
        self._rgba = r, g, b, a[0] if a else 255

        program = get_default_shader()
        self._batch = batch or Batch()
        self._group = self.group_class(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, program, group)

        self._create_vertex_list()

    def __contains__(self, point):
        pass

    def _create_vertex_list(self):
        self._vertex_list = self._group.program.vertex_list(
            self._num_verts, self._draw_mode, self._batch, self._group,
            position=('f', self._get_vertices()),
            colors=('Bn', self._rgba * self._num_verts),
            translation=('f', (self._x, self._y) * self._num_verts))

    def _get_vertices(self):
        if not self._visible:
            return (0, 0) * self._num_verts
        else:
            # Adjust all coordinates by the anchor.
            trans_x, trans_y = self._coordinates[0]
            trans_x += self._anchor_x
            trans_y += self._anchor_y
            coords = [[x - trans_x, y - trans_y] for x, y in self._coordinates]

            doubles = []

            x, y = coords[0]
            #doubles = +=[]
            for n in range(len(coords)-2):
                x0, y0 = coords[n]
                x1, y1 = coords[n + 1]
                x2, y2 = coords[n + 2]
                xl, yl, xr, yr = self._get_double(x0, y0, x1, y1, x2, y2)
                doubles += [[xl, yl], [xr, yr]]
            x, y = coords[-1]
            # doubles += [x, y]

            # Triangulate the convex polygon.
            triangles = []
            for n in range(len(doubles) - 2):
                triangles += [doubles[n]]
                triangles += [doubles[n+1]]
                triangles += [doubles[n+2]]

            # Flattening the list before setting vertices to it.
            print(tuple(value for coordinate in triangles for value in coordinate))
            print(len(tuple(value for coordinate in triangles for value in coordinate)), self._num_verts)
            return tuple(value for coordinate in triangles for value in coordinate)


    def _get_double(self, x0, y0, x1, y1, x2, y2):
        dx0, dy0 = self._get_dir(x0, y0, x1, y1)
        dx1, dy1 = self._get_dir(x1, y1, x2, y2)

        xl0, yl0 = x0 - dy0*self.thickness_left, y0 + dx0*self.thickness_left
        xr0, yr0 = x0 + dy0*self.thickness_right, y0 - dx0*self.thickness_right
        xl2, yl2 = x2 - dy1 * self.thickness_left, y2 + dx1 * self.thickness_left
        xr2, yr2 = x2 + dy1 * self.thickness_right, y2 - dx1 * self.thickness_right

        xl1, yl1 = self._get_intersect(xl0, yl0, dx0, dy0, xl2, yl2, dx1, dy1)
        xr1, yr1 = self._get_intersect(xr0, yr0, dx0, dy0, xr2, yr2, dx1, dy1)

        return xl1, yl1, xr1, yr1

    def _get_dir(self, x0, y0, x1, y1):
        dx0, dy0 = x1 - x0, y1 - y0
        l = (dx0 ** 2 + dy0 ** 2) ** (1 / 2)
        if l <= 0:
            l = 1
        dx0 /= l
        dy0 /= l

        return dx0, dy0

    def _get_intersect(self, x0, y0, dx0, dy0, x1, y1, dx1, dy1):
        # ax + b = y
        # cx + d = y
        # x = (d-b)/(a-c)
        a, c = dy0/dx0, dy1/dx1
        b = y0 - a * x0
        d = y1 - c * x1
        print(a-c, d-b)
        x = (d-b)/(a-c)
        y = b + a*x

        return x, y


    def _update_vertices(self):
        self._vertex_list.position[:] = self._get_vertices()

