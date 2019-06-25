import pygame
from ..drawable import Mobile, Point3D, Shape3D
from ..pallette import C_TABLE_GREEN, C_TAN, C_DARK_TAN, C_BLACK, C_WHITE, C_WHITESMOKE

WIDTH = 2560 // 4
HEIGHT = 1440 // 4

table_color = C_TABLE_GREEN

player = Mobile(200, 300, 0, 0)
player.drag = 1
player_rect = pygame.Rect(0, 0, 100, 150)
player_pad = pygame.Rect(100, 60, 50, 50)
pygame.draw.rect(player.surface, C_DARK_TAN, player_rect)
pygame.draw.rect(player.surface, C_TAN, player_pad)
player.surface.set_colorkey(C_BLACK)
player.pos = ((WIDTH - 100) / 2, HEIGHT - 150)

# table = Drawable(WIDTH, HEIGHT, 0, 0)
# table.surface.set_colorkey((0, 0, 0))

# points = [(WIDTH / 2 - 200, HEIGHT * 2 / 3),
#           (WIDTH / 2 + 200, HEIGHT * 2 / 3),
#           (WIDTH / 2 + 100, HEIGHT / 3),
#           (WIDTH / 2 - 100, HEIGHT / 3),
#           ]
# pygame.draw.polygon(table.surface, table_color, points)

table_scale = 280
table_h = .76 * table_scale
table_w = 1.525 * table_scale
table_z = 2.74 * table_scale
table_offset_x = WIDTH // 2 - table_w // 2
table_offset_y = HEIGHT // 2 + table_h
table_offset_z = 25
net_height = .1525 * table_scale
net_z = table_offset_z + table_z // 2

s = pygame.Surface((WIDTH, HEIGHT))
table_points = [
        Point3D(s, table_offset_x, table_offset_y, table_offset_z),
        Point3D(s, table_offset_x + table_w, table_offset_y, table_offset_z),
        Point3D(s, table_offset_x + table_w, table_offset_y, table_offset_z + table_z),
        Point3D(s, table_offset_x, table_offset_y, table_offset_z + table_z)
        ]

net_points = [
        Point3D(s, table_offset_x, table_offset_y - net_height, net_z),
        Point3D(s, table_offset_x + table_w, table_offset_y - net_height, net_z),
        Point3D(s, table_offset_x + table_w, table_offset_y, net_z),
        Point3D(s, table_offset_x, table_offset_y, net_z)
        ]

table = Shape3D(table_points, C_TABLE_GREEN)
net = Shape3D(net_points, C_WHITESMOKE)
