import sys
import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
screen.fill((255, 255, 255))

player_image = pygame.image.load("ball.gif")
player = player_image.get_rect()
x, y = 0, 0
while 1:
    player.center = (x, y)

    screen.fill((0, 0, 255))
    screen.blit(player_image, player)

    x += 1
    y += 1
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
