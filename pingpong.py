import pygame
import numpy as np
# from pingpong.game_objects.testobjs import player, table, net, ball
from gl.drawable import PingPongBall, Point3D, Shape3D
from gl.pallette import C_WHITE
from gl.constants import WIDTH, HEIGHT
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
drawables = {Shape3D([Point3D(0.1, 0.1, .5), 
                      Point3D(0.3, 0.1, .5),
                      Point3D(0.3, 0.2, .5),
                      Point3D(0.1, 0.2, .5)], 
                      (120,120,15)),
             Point3D(0.2, 0.2, .5)}

with GameLoop(drawables) as loop:
    loop.begin(gameDisplay, clock, 60)

pygame.quit()
quit()
