import pygame
import numpy as np
import glm
import os, sys

sys.path.append(os.getcwd)

from OpenGL.GL import *
from OpenGL.GLU import *

from engine.gl.drawable import cube, box, Point3D
from engine.gl.shader import Shader, Pipeline
from engine.gl.camera import Camera
from engine.gl.obj_loader import OBJ_to_shape
from engine.gl.constants import WIDTH, HEIGHT
from engine.gameloop.VBOGameLoop import VBOGameLoop
from engine.gameloop.GameLoop import GameLoop

from game.drawables import drawables, collision_system, gravity

# Game Variables
GAME_PACE_SCALAR = 1.

# PyGame Init
pygame.init()
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF|pygame.OPENGL)
pygame.display.set_caption('Ping Pong')
clock = pygame.time.Clock()

model = r'C:\Users\Alex\Documents\pingpong\assets\pingponggame\Paddle.obj'
paddle = OBJ_to_shape(model)
paddle.gen_normals()
# paddle.center_and_normalize()
c = cube(.5, Point3D(-.25, -.25, .25))
c.gen_normals()


vert = Shader('litvert', GL_VERTEX_SHADER)
frag = Shader('litfrag', GL_FRAGMENT_SHADER)
pipeline = Pipeline(vert, frag)
pipeline.vao = ''
camera = Camera()
camera.move(0, .1, -1.2)
camera.rotate(0, 0, 20)

for d in drawables.values():
    pipeline.add_model(d)

with VBOGameLoop([pipeline], cameras=[camera]) as loop:
    loop.animators.append(gravity)
    loop.collision_systems.append(collision_system)

    def handle_mouse(loop, event):
        if not pygame.mouse.get_pressed()[0]:
            return

        loop.state['pos'].append(glm.vec2(event.pos))

        if len(loop.state['pos']) > 25:
            pos = loop.state['pos'].popleft()
        else:
            pos = loop.state['pos'][0]
        pos = event.pos - pos
        loop.view.rotate(pos[0], pos[1], 0, degrees=True)

    def handle_kbd(loop, event):
        mv = .1
        mmv = -.1
        if event.key == pygame.K_LEFT:
            for d in drawables.values():
                d.offset = glm.translate(d.offset, glm.vec3(mv, 0., 0.))
        if event.key == pygame.K_RIGHT:
            for d in drawables.values():
                d.offset = glm.translate(d.offset, glm.vec3(mmv, 0., 0.))
        if event.key == pygame.K_DOWN:
            for d in drawables.values():
                d.offset = glm.translate(d.offset, glm.vec3(0., mv, 0.))
        if event.key == pygame.K_UP:
            for d in drawables.values():
                d.offset = glm.translate(d.offset, glm.vec3(0., mmv, 0.))
        if event.key == pygame.K_z:
            for d in drawables.values():
                d.offset = glm.translate(d.offset, glm.vec3(0., 0., mv))
        if event.key == pygame.K_x:
            for d in drawables.values():
                d.offset = glm.translate(d.offset, glm.vec3(0., 0., mmv))

        if event.key == pygame.K_SPACE:
            pass

    from collections import deque
    loop.state['pos'] = deque()
    loop.define_handler(pygame.MOUSEMOTION, handle_mouse)
    loop.define_handler(pygame.KEYDOWN, handle_kbd)
    loop.begin(gameDisplay, clock, 60)

pygame.quit()
quit()
