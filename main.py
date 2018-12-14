import sys
import pygame
import random
from pykakasi import kakasi

pygame.init()


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

        self.frame_size = (img_src.get_width() / frame_num[0], img_src.get_height() / frame_num[1])
        for x in range(0, frame_num[0]):
            for y in range(0, frame_num[1]):
                surface = pygame.Surface(self.frame_size)
                surface.blit(
                    img_src,
                    (0, 0),
                    (x * self.frame_size[0], y * self.frame_size[1]) + self.frame_size,
                    pygame.BLEND_ADD
                )
                surface.set_colorkey((0, 0, 0))
                self.images.append(surface)

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self):
        self.frame += 0.3
        frame_num = int(self.frame)
        if frame_num == len(self.images):
            self.kill()
            return
        self.image = self.images[frame_num]


class Phrase(pygame.sprite.Sprite):
    font = pygame.font.Font('migu-1m-regular.ttf', 32)
    kakasi = kakasi()
    kakasi.setMode("H", "a")
    kakasi.setMode("K", "a")
    kakasi.setMode("J", "a")
    kakasi.setMode("r", "Kunrei")
    conv = kakasi.getConverter()

    def __init__(self, y, string):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.characters_roman = [c for c in self.conv.do(string)]

        # 日本語/ローマ字のうち、より幅の大きい方に画像の幅を合わせる
        character_size = self.font.size(max(self.conv.do(string), string, key=lambda x: len(x)))

        surface = pygame.Surface((character_size[0], character_size[1] * 2))
        surface.set_colorkey((0, 0, 0))

        self.characters = self.font.render(string, True, (1, 1, 1), (255, 255, 255))

        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.midleft = (640, y)
        self.speed = -2.0
        # 文字列内の文字の参照位置
        self.next_character_pos = 0

    def update(self):
        self.rect.move_ip(self.speed, 0)
        self.image.fill((255, 255, 255))
        self.image.blit(self.characters, (0, 0))

        if len(self.characters_roman) == self.next_character_pos:
            self.kill()

        for i, c in enumerate(self.characters_roman):
            if not c:
                continue
            self.image.blit(self.font.render(c, True, (1, 1, 1), (255, 255, 255)), (i * 16, 32))
        if self.rect.right < 0:
            self.rect.left = 640

    def input(self, character):
        if self.characters_roman[self.next_character_pos] == character:
            self.characters_roman[self.next_character_pos] = ''
            self.next_character_pos += 1
            Explosion((self.rect.left + (self.next_character_pos * 16), self.rect.centery))


screen = pygame.display.set_mode((640, 480))

group = pygame.sprite.RenderUpdates()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

Player.containers = group
Bullet.containers = group, enemies
Enemy.containers = group, bullets
Explosion.containers = group
Phrase.containers = group

# player = Player()
# enemy = Enemy()
# enemy.rect.center = (240, 300)

input_chrs = []
remain_chrs = []

sentences = ['庭に埴輪ニワトリがいる', '猿も木から落ちる', '隣の芝生は青い']
target = Phrase(200 + random.randint(1, 100), random.choice(sentences))

while 1:
    screen.fill((255, 255, 255))
    pressed_keys = pygame.key.get_pressed()
    if not target.alive():
        target.remove()
        target = Phrase((200 + random.randint(0, 200)), random.choice(sentences))
    # if pressed_keys[pygame.K_LEFT]:
    #     player.vx = -player.speed
    # if pressed_keys[pygame.K_RIGHT]:
    #     player.vx = player.speed
    # if pressed_keys[pygame.K_UP]:
    #     player.vy = -player.speed
    # if pressed_keys[pygame.K_DOWN]:
    #     player.vy = player.speed
    # if pressed_keys[pygame.K_z]:
    #     Bullet(player.rect.center, (10, 0))

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
            elif str.isalnum(event.unicode):
                target.input(event.unicode)
