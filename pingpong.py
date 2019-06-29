import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
# from pingpong.game_objects.testobjs import player, table, net, ball
from gl.drawable import cube, Point3D
from gl.pallette import C_WHITE
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

# Ordered!
# drawables = [ball, net, player, table]


drawables = {cube(1, Point3D(-.5, -.5, .2))}
glEnable(GL_POLYGON_SMOOTH)
# glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
glEnable(GL_BLEND)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_PROJECTION)

with VBOGameLoop(drawables) as loop:
    def handle_mouse(loop, event):
        if not pygame.mouse.get_pressed()[0]:
            return

        loop.state['pos'].append(np.array(event.pos))

        if len(loop.state['pos']) > 25:
            pos = loop.state['pos'].popleft()
        else:
            pos = loop.state['pos'][0]
        pos = event.pos - pos
        glRotatef(5, pos[0], pos[1], 0)

    from collections import deque
    loop.state['pos'] = deque()
    loop.define_handler(pygame.MOUSEMOTION, handle_mouse)
    loop.begin(gameDisplay, clock, 60)

pygame.quit()
quit()
