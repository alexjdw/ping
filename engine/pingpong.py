import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GL import glRotatef
from OpenGL.GLU import *
# from pingpong.game_objects.testobjs import player, table, net, ball
from gl.drawable import cube, Point3D
from gl.shader import Shader, Pipeline
from gl.camera import Camera
from gl.obj_loader import OBJ_to_shape
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

model = r'C:\Users\Alex\Documents\pingpong\engine\gl\assets\pingponggame\PingPongPaddle.obj'
drawables = {OBJ_to_shape(model), cube(30, Point3D(-15, -15, -15))}


vert = Shader('vertex_default', GL_VERTEX_SHADER)
frag = Shader('fragment_default', GL_FRAGMENT_SHADER)
pipeline = Pipeline(vert, frag)
camera = 
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
        glRotatef(15, pos[1], pos[0], 0)

    def handle_kbd(loop, event):
        if event.key == pygame.K_LEFT:
            for d in drawables:
                offset = np.identity(4)
                offset[0][3] = .1
                d.offset = d.offset + offset

    from collections import deque
    loop.state['pos'] = deque()
    loop.define_handler(pygame.MOUSEMOTION, handle_mouse)
    loop.define_handler(pygame.KEYDOWN, handle_kbd)
    loop.begin(gameDisplay, clock, 60)

pygame.quit()
quit()
