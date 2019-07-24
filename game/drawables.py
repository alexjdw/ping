from engine.gl.drawable import box, sphere, Point3D
from engine.gl.collision import CollisionBox, CollisionFrame, CollisionSystem
from engine.gl.collision_handlers import bounce
from engine.gl.animations import GravityAnimator
import glm

METRE_CONV = 1.2

drawables = {}
collisions = {}


drawables['table'] = box(.1 * METRE_CONV, 1.525 * METRE_CONV, 2.74 * METRE_CONV, Point3D(-.5, -.5, -1), color=(.2, .2, .8))
drawables['ball'] = sphere(.05, Point3D(0., 3., 0.), color=(.8, .8, .8))

gravity = GravityAnimator(.003)
gravity.apply_to(drawables['ball'])

ball_collision = CollisionBox.from_shape(drawables['ball'])
ball_collision.handler = bounce
ball_collision.handler_targets.append(gravity)

table_collision = CollisionBox.from_shape(drawables['table'])

collision_system = CollisionSystem()
collision_system.add(ball_collision)
collision_system.add(table_collision)
