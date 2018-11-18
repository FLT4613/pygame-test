import sys
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("ball.gif")
        self.rect = self.image.get_rect()
        self.vx = 0
        self.vy = 0
        self.brake = 0.2
        self.speed = 5.0

    def update(self):
        self.rect.move_ip(self.vx, self.vy)
        if self.vx > 0.0:
            self.vx = max(self.vx-self.brake, 0)
        if self.vx < 0.0:
            self.vx = min(self.vx+self.brake, 0)
        if self.vy > 0.0:
            self.vy = max(self.vy-self.brake, 0)
        if self.vy < 0.0:
            self.vy = min(self.vy+self.brake, 0)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


pygame.init()
screen = pygame.display.set_mode((640, 480))
player = Player()
screen.fill((255, 255, 255))

while 1:
    screen.fill((0, 0, 255))
    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[pygame.K_a]:
        player.vx = -player.speed
    elif pressed_keys[pygame.K_d]:
        player.vx = player.speed
    elif pressed_keys[pygame.K_w]:
        player.vy = -player.speed
    elif pressed_keys[pygame.K_s]:
        player.vy = player.speed

    player.update()
    player.draw(screen)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
