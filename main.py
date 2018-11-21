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


class Explosion(pygame.sprite.Sprite):

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.frame = 0
        frame_num = (8, 1)
        img_src = pygame.image.load("explosion.png")
        self.images = []

        self.frame_size = (img_src.get_width() /
                           frame_num[0], img_src.get_height() / frame_num[1])
        for x in range(0, frame_num[0]):
            for y in range(0, frame_num[1]):
                surface = pygame.Surface(self.frame_size)
                surface.blit(
                    img_src,
                    (0, 0),
                    (x * self.frame_size[0], y *
                     self.frame_size[1]) + self.frame_size
                )
                self.images.append(surface)

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self):
        self.frame += 1
        if self.frame == len(self.images):
            self.kill()
            return
        self.image = self.images[self.frame]


pygame.init()
screen = pygame.display.set_mode((640, 480))

group = pygame.sprite.RenderUpdates()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

Player.containers = group
Bullet.containers = group, enemies
Enemy.containers = group, bullets
Explosion.containers = group

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
        print(dead.rect.center)
        Explosion(dead.rect.center)
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
