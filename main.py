import sys
import pygame
import random


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
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


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load("ball.gif")
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.move_ip(0, random.randint(-5, 5))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, start, velocity, speed=5.0):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load("ball.gif")
        self.rect = self.image.get_rect()
        self.rect.center = start
        self.vx = velocity[0]
        self.vy = velocity[1]
        self.speed = 5.0

    def update(self):
        self.rect.move_ip(self.vx, self.vy)
        if not pygame.Rect(0, 0, 640, 480).contains(self.rect):
            self.kill()


pygame.init()
screen = pygame.display.set_mode((640, 480))

group = pygame.sprite.RenderUpdates()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

Player.containers = group
Bullet.containers = group, enemies
Enemy.containers = group, bullets

player = Player()
enemy = Enemy()
enemy.rect.center = (240, 300)

while 1:
    screen.fill((255, 255, 255))
    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[pygame.K_a]:
        player.vx = -player.speed
    if pressed_keys[pygame.K_d]:
        player.vx = player.speed
    if pressed_keys[pygame.K_w]:
        player.vy = -player.speed
    if pressed_keys[pygame.K_s]:
        player.vy = player.speed
    if pressed_keys[pygame.K_z]:
        Bullet(player.rect.center, (10, 0))

    for dead in pygame.sprite.groupcollide(bullets, enemies, True, False):
        enemy = Enemy()
        enemy.rect.center = (random.randint(200, 600), random.randint(0, 400))

    group.update()
    group.draw(screen)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
