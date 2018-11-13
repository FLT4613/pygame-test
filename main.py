import sys
import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
screen.fill((255, 255, 255))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.display.flip()
