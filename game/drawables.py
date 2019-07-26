from engine.gl.drawable import box, sphere, Point3D
from engine.gl.collision import CollisionBox, CollisionFrame, CollisionSystem
from engine.gl.collision_handlers import bounce
from engine.gl.animations import GravityAnimator
import glm

METRE_CONV = .3

drawables = {}
collisions = {}


drawables['table'] = box(.1 * METRE_CONV, 1.525 * METRE_CONV, 2.74 * METRE_CONV, Point3D(-.5, -.5, -1), color=(.8, .2, .2))
drawables['ball'] = sphere(.02, Point3D(0., 3., 0.), color=(.8, .8, .8))
drawables['floor'] = box(.001, 10, 5, Point3D(-5, -2, -3), color=(.5, .6, .7))
drawables['back_wall'] = box(25, 25, .001, Point3D(-12.5, -12.5, -2), color=(1, .2, .2))
gravity = GravityAnimator(.003)
gravity.apply_to(drawables['ball'])

ball_collision = CollisionBox.from_shape(drawables['ball'])
ball_collision.handler = bounce
ball_collision.handler_targets.append(gravity)

table_collision = CollisionBox.from_shape(drawables['table'])
floor_collision = CollisionBox.from_shape(drawables['floor'])
back_wall_collision = CollisionBox.from_shape(drawables['back_wall'])

table_collision.bounce_normal = floor_collision.bounce_normal = glm.vec3(1, -1, 1)
back_wall_collision.bounce_normal = glm.vec3(1, 1, -1)
floor_collision.bounce_rebound = .7
back_wall_collision.bounce_rebound = .7
table_collision.bounce_rebound = .95

collision_system = CollisionSystem()
collision_system.add(ball_collision)
collision_system.add(table_collision)
collision_system.add(floor_collision)
collision_system.add(back_wall_collision)
