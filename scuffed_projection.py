import pygame
from math import *
import numpy as np

WIDTH = 1000
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))

FOV = 90

clock = pygame.time.Clock()

# def cart2sph(x, y, z):
#     hxy = np.hypot(x, y)
#     r = np.hypot(hxy, z)
#     el = np.arctan2(z, hxy)
#     az = np.arctan2(y, x)
#     return az, el, r

class Camera:

    def __init__(self, *pos):
        self.pos = np.array(pos)
    
    # def get_2d_projection(self, point):
    #     az, el, r = cart2sph(*(point - self.pos))
    #     mult = WIDTH / (FOV * pi/180)
    #     return (WIDTH/2 + az*mult, HEIGHT/2 + el*mult)

    def get_2d_projection(self, point):
        offset = point - self.pos

        if offset[0] <= 0:
            angle = atan2(offset[2], offset[1])
            return (WIDTH/2 + 1000000*cos(angle), HEIGHT/2 + 1000000*sin(angle))

        _, x, y = offset/offset[0]
        mult = WIDTH/2/tan(FOV*pi/360)
        return (WIDTH/2 + mult*x, HEIGHT/2 + mult*y)

points0 = [(-1, -1, -1), (-1, -1, 1), (-1, 1, -1), (-1, 1, 1), (1, -1, -1), (1, -1, 1), (1, 1, -1), (1, 1, 1)]
edges = [(0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3), (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7)]

p = (sqrt(5) + 1)/2

# points0 = [(1/p, 0, p), (-1/p, 0, p),
#            (1, 1, 1), (-1, 1, 1), (-1, -1, 1), (1, -1, 1),
#            (0, p, 1/p), (0, -p, 1/p),
#            (p, 1/p, 0), (-p, 1/p, 0), (-p, -1/p, 0), (p, -1/p, 0),
#            (0, p, -1/p), (0, -p, -1/p),
#            (1, 1, -1), (-1, 1, -1), (-1, -1, -1), (1, -1, -1),
#            (1/p, 0, -p), (-1/p, 0, -p)]
# edges = [(0, 1), (0, 2), (0, 5), (1, 3), (1, 4),
#          (2, 6), (2, 8), (3, 6), (3, 9), (4, 7),
#          (4, 10), (5, 7), (5, 11), (6, 12), (7, 13),
#          (8, 11), (8, 14), (9, 10), (9, 15), (10, 16),
#          (11, 17), (12, 14), (12, 15), (13, 16), (13, 17),
#          (14, 18), (15, 19), (16, 19), (17, 18), (18, 19)]

points = points0[:]
camera = Camera(-2.0, 0.0, 0.0)

angle = 2*pi/5

while True:

    screen.fill((0, 0, 0))
    # FOV += 0.1

    points = [(x*cos(angle)-y*sin(angle), x*sin(angle)+y*cos(angle), z) for x, y, z in points0]
    screen_space = list(map(camera.get_2d_projection, points))

    for a, b in edges:
        pygame.draw.line(screen, (255, 0, 0), screen_space[a], screen_space[b])
    for ptx, pty in screen_space:
        pygame.draw.circle(screen, (255, 0, 0), (int(ptx), int(pty)), 3)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        camera.pos[0] += 0.03
    elif keys[pygame.K_s]:
        camera.pos[0] -= 0.03
    if keys[pygame.K_a]:
        camera.pos[1] -= 0.03
    elif keys[pygame.K_d]:
        camera.pos[1] += 0.03
    if keys[pygame.K_UP]:
        FOV += 0.5
    elif keys[pygame.K_DOWN]:
        FOV -= 0.5
    print(FOV)

    # angle += 0.01

    pygame.event.pump()
    pygame.display.flip()
    clock.tick(60)