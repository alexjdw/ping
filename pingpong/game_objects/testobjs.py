# import pygame, numpy as np
# from ..drawable import Mobile, Point3D, Ball3D, Shape3D, PingPongBall, Composite
# from ..pallette import C_TABLE_GREEN, C_TAN, C_DARK_TAN, C_BLACK,\
#     C_WHITESMOKE, C_WHITE
# from ..constants import WIDTH, HEIGHT

# table_color = C_TABLE_GREEN

# dummy_surf = pygame.Surface((WIDTH, HEIGHT))

# player_scale = 150
# player_height = 1.7
# player_width = 39.624

# head = Composite()
# polo = Composite()
# player = Composite()

# ball = PingPongBall(dummy_surf, 400, 20, 20, 20, C_WHITE)
# ball.vector = np.array([0, 0, 50])
# ball.pos3d = [50, 50, 100]

# table_scale = 150
# table_h = .76 * table_scale
# table_w = 1.525 * table_scale
# table_z = 2.74 * table_scale
# table_offset_x = WIDTH // 2 - table_w // 2
# table_offset_y = HEIGHT // 2 + table_h
# table_offset_z = 50
# net_height = .1525 * table_scale
# net_z = table_offset_z + table_z // 2

# s = pygame.Surface((WIDTH, HEIGHT))
# table_points = [
#         Point3D(s, table_offset_x, table_offset_y, table_offset_z),
#         Point3D(s, table_offset_x + table_w, table_offset_y, table_offset_z),
#         Point3D(s, table_offset_x + table_w, table_offset_y, table_offset_z + table_z),
#         Point3D(s, table_offset_x, table_offset_y, table_offset_z + table_z)
#         ]

# net_points = [
#         Point3D(s, table_offset_x, table_offset_y - net_height, net_z),
#         Point3D(s, table_offset_x + table_w, table_offset_y - net_height, net_z),
#         Point3D(s, table_offset_x + table_w, table_offset_y, net_z),
#         Point3D(s, table_offset_x, table_offset_y, net_z)
#         ]

# print([(t.pos3d, t.pos) for t in table_points])

# table = Shape3D(table_points, C_TABLE_GREEN)
# net = Shape3D(net_points, C_WHITESMOKE)
