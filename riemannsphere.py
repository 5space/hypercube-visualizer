import pygame
from math import *
import numpy as np
import itertools

from shapes import *

WIDTH = 500
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))

FOV = 60

clock = pygame.time.Clock()

class Camera:

    def __init__(self, *pos):
        self.pos = np.array(pos)

    def get_2d_projection(self, point):
        offset = point - self.pos

        if offset[0] <= 0:
            a = atan2(offset[2], offset[1])
            return (WIDTH/2 + 1000000*cos(a), HEIGHT/2 + 1000000*sin(a))

        _, x, y = offset/offset[0]
        mult = WIDTH/2/tan(FOV*pi/360)
        return (WIDTH/2 + mult*x, HEIGHT/2 + mult*y)

p = (sqrt(5) + 1)/2

# edge_colors = {1:np.array([255, 0, 0]), 2:np.array([0, 255, 0]), 4:np.array([0, 0, 255]), 8:np.array([255, 255, 0])}

camera = Camera(-2., 0., 0.)

points, edges = [(0, 0, 0), (1, 0, 0), (0, 1, 0)], [(0, 1), (0, 2), (1, 2)]

angles = [0., 0., 0.]  # XY, XZ, YZ in that order

def get_rotated_position(p):
    p = list(p)
    key = [(0, 1), (0, 2), (1, 2)]
    for i in range(3):
        a1, a2 = key[i]
        angle = angles[i]
        sign_flipper = -1 if ((a2 - a1) % 2 == 0) else 1

        p[a1], p[a2] = p[a1]*cos(angle) - sign_flipper*p[a2]*sin(angle), sign_flipper*p[a1]*sin(angle) + p[a2]*cos(angle)
    return tuple(p)

mouse_down = False
drag_start_pos = (0, 0)
drag_offset = (0, 0)

scroll_velocity = 1

while True:

    screen.fill((0, 0, 0))

    points_rotated = list(map(get_rotated_position, points))
    screen_space = list(map(camera.get_2d_projection, points_rotated))

    def distance_from_camera(x):
        return np.linalg.norm((np.array(points_rotated[x[0]])+points_rotated[x[1]])/2 - camera.pos)

    def color_of_edge(edge):

        color = np.array([255, 255, 255.])  # edge_colors[abs(b-a)]
        distance_mult = max(0.1, min(1, 10/(e**(-3*distance_from_camera(edge)/camera.pos[0]))))
        color *= distance_mult
        return tuple(np.around(color))

    edges_sorted = sorted(edges, key=distance_from_camera)[::-1]

    for a, b in edges_sorted:
        pygame.draw.line(screen, color_of_edge((a, b)), screen_space[a], screen_space[b], 5)
    # for ptx, pty in screen_space:
    #     pygame.draw.circle(screen, (255, 0, 0), (int(ptx), int(pty)), 3)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        FOV += 0.5
    elif keys[pygame.K_DOWN]:
        FOV -= 0.5

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_down = True
                drag_start_pos = event.pos
                drag_start_angles = np.array(angles)
            elif event.button == 4:
                scroll_velocity = 1/3
            elif event.button == 5:
                scroll_velocity = 3
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_down = False
    
    if mouse_down:
        x, y = pygame.mouse.get_pos()
        drag_offset = (x - drag_start_pos[0], y - drag_start_pos[1])
        angles = list(drag_start_angles + [-pi*drag_offset[0]/WIDTH, pi*drag_offset[1]/HEIGHT, 0])
    
    angles = [((a+pi) % (2*pi)) - pi for a in angles]
    angles[1] = min(pi/2, max(-pi/2, angles[1]))
    camera.pos[0] *= scroll_velocity**0.02
    scroll_velocity **= 0.95

    # print(angles[0]-pi/4, angles[1]-pi/4, angles[2]-pi/4)

    pygame.display.flip()
    clock.tick(60)