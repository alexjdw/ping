import pygame
import pygame.gfxdraw
import numpy as np
from pingpong.game_objects.testobjs import player, table, net
from pingpong.drawable import PingPongBall
from pingpong.pallette import C_WHITE

WIDTH = 2560 // 4
HEIGHT = 1440 // 4

GAME_PACE = 1.

pygame.init()
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Ping Pong')
clock = pygame.time.Clock()

player_exited = False
black = (0, 0, 0)

ball = PingPongBall(gameDisplay, 400, 20, 20, 20, C_WHITE)
ball.vector = np.array([.3, .7, 6])
# Ordered!
drawables = [table, net, ball, player]

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
            raise TypeError("Drawable " + repr(d) + " can't be drawn. Please add a .survace or .draw() method.")
        if (hasattr(d, 'move')):
            d.move()

    ball.check_collision(table)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
