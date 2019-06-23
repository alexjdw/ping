import pygame
import pygame.gfxdraw
from pingpong.testobjs import player, table
from pingpong.drawable import Ball3D
from math import copysign

WIDTH = 2560 // 4
HEIGHT = 1440 // 4

pygame.init()
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Ping Pong')
clock = pygame.time.Clock()

player_exited = False
black = (0, 0, 0)

ball = Ball3D(gameDisplay, 400, 20, 20, 20, pygame.Color(255,255,255,1))
ball.vector = (0, 0, 1)
# Ordered!
drawables = [table, ball, player]

while not player_exited:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            player_exited = True

    dist = pygame.mouse.get_pos()[0] - player.pos[0]
    if (abs(dist) > 100):
        player.vector = (dist / 100, 0)
    else:
        player.vector = (0, 0)

    gameDisplay.fill(black)
    for d in drawables:
        if (hasattr(d, 'draw')):
            d.draw(gameDisplay)
        elif (hasattr(d, 'surface')):
            gameDisplay.blit(d.surface, d.pos)
        else:
            raise TypeError("Drawable " + repr(d) + " has no applicable drawing methods.")
        if (hasattr(d, 'move')):
            d.move()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
