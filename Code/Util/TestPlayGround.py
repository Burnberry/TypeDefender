from pyglet.graphics.shader import ShaderProgram
from pyglet.shapes import _ShapeGroup, get_default_shader
from pyglet import gl


def test():
    print("testing")
    _ShapeGroup(gl.GL_SRC_ALPHA   , gl.GL_DST_ALPHA  , get_default_shader()).set_state()




