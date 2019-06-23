import pygame
from .drawable import Drawable, Mobile, Ball3D, Point3D

WIDTH = 2560 // 4
HEIGHT = 1440 // 4

table_color = pygame.Color(0, 120, 120, 1)

player = Mobile(200, 300, 0, 0)
player.drag = 1
player_rect = pygame.Rect(0, 0, 100, 150)
player_pad = pygame.Rect(100, 60, 50, 50)
pygame.draw.rect(player.surface, pygame.Color(120, 90, 80, 1), player_rect)
pygame.draw.rect(player.surface, pygame.Color(200, 25, 25, 1), player_pad)
player.surface.set_colorkey((0, 0, 0))
player.pos = ((WIDTH - 100) / 2, HEIGHT - 150)

# table = Drawable(WIDTH, HEIGHT, 0, 0)
# table.surface.set_colorkey((0, 0, 0))

# points = [(WIDTH / 2 - 200, HEIGHT * 2 / 3),
#           (WIDTH / 2 + 200, HEIGHT * 2 / 3),
#           (WIDTH / 2 + 100, HEIGHT / 3),
#           (WIDTH / 2 - 100, HEIGHT / 3),
#           ]
# pygame.draw.polygon(table.surface, table_color, points)

table_scale = 50
table_h = .76 * table_scale
table_w = 1.525 * table_scale
table_z = 2.74 * table_scale
table_offset_x = 200
table_offset_y = 400
table_offset_z = 25

table_points = [
        Point3D(table_offset_x, table_offset_y + table_h, table_offset_z),
        Point3D(table_offset_x + table_w, table_offset_y + table_h, table_offset_z),
        Point3D(table_offset_x + table_w, table_offset_y + table_h, table_offset_z + table_z),
        Point3D(table_offset_x, table_offset_y + table_h, table_offset_z + table_z)
        ]
