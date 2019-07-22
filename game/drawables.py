from engine.gl.drawable import box, sphere, Point3D

METRE_CONV = .4

drawables = {}

drawables['table'] = box(.1 * METRE_CONV, 1.54 * METRE_CONV, 2.15 * METRE_CONV, Point3D(-.2, -.2, 0.), color=(.2, .2, .8))
drawables['ball'] = sphere(.05, Point3D(0., 0., 0.), color=(.8, .8, .8))
