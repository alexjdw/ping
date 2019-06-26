import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
# from pingpong.game_objects.testobjs import player, table, net, ball
from pingpong.drawable import PingPongBall, Point3D, Shape3D
from pingpong.pallette import C_WHITE
from pingpong.constants import WIDTH, HEIGHT

# Game Variables
GAME_PACE_SCALAR = 1.

# PyGame Init
pygame.init()
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF|pygame.OPENGL)
pygame.display.set_caption('Ping Pong')
clock = pygame.time.Clock()

# OpenGL Init
gluPerspective(45, (WIDTH / HEIGHT), 0.2, 50.)
glTranslatef(0., 0., -10.)
glRotatef(0, 0, 0, 0)
black = (0, 0, 0)

# Ordered!
# drawables = [ball, net, player, table]
drawables = [Shape3D([Point3D(0.1, 0.1, .5), 
                      Point3D(0.3, 0.1, .5),
                      Point3D(0.3, 0.2, .5),
                      Point3D(0.1, 0.2, .5)], 
                      (120,120,15)),
             Point3D(0.2, 0.2, .5)]

exit_flag = False

while not exit_flag:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  # clear the screen
    for d in drawables:
        if (hasattr(d, 'GLDraw')):
            d.GLDraw()
        elif (hasattr(d, 'surface')):
            gameDisplay.blit(d.surface, d.pos)
        else:
            raise TypeError("Drawable " + repr(d) + " can't be drawn. Please add a .survace or .draw() method.")
        if (hasattr(d, 'move')):
            d.move()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
quit()
