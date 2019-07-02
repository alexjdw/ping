import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GL import glRotatef
from OpenGL.GLU import *
# from pingpong.game_objects.testobjs import player, table, net, ball
from gl.drawable import cube, Point3D
from gl.shader import Shader, Pipeline
from gl.constants import WIDTH, HEIGHT
from gameloop.VBOGameLoop import VBOGameLoop
from gameloop.GameLoop import GameLoop

# Game Variables
GAME_PACE_SCALAR = 1.

# PyGame Init
pygame.init()
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF|pygame.OPENGL)
pygame.display.set_caption('Ping Pong')
clock = pygame.time.Clock()


drawables = {cube(.2, Point3D(-.3, -.3, .3))}
vert = Shader('vertex_default', GL_VERTEX_SHADER)
frag = Shader('fragment_default', GL_FRAGMENT_SHADER)
pipeline = Pipeline(vert, frag)
for d in drawables:
    pipeline.add_model(d)

with VBOGameLoop([pipeline]) as loop:
    def handle_mouse(loop, event):
        if not pygame.mouse.get_pressed()[0]:
            return

        loop.state['pos'].append(np.array(event.pos))

        if len(loop.state['pos']) > 25:
            pos = loop.state['pos'].popleft()
        else:
            pos = loop.state['pos'][0]
        pos = event.pos - pos
        glRotatef(5, pos[1], pos[0], 0)

    from collections import deque
    loop.state['pos'] = deque()
    loop.define_handler(pygame.MOUSEMOTION, handle_mouse)
    loop.begin(gameDisplay, clock, 60)

pygame.quit()
quit()
