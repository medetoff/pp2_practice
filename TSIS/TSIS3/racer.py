import pygame
import random
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self, settings):
        super().__init__()
        self.original = pygame.transform.smoothscale(pygame.image.load("assets/images/car.png"), (110, 140))
        self.image = self.original.copy()
        self.rect = self.image.get_rect(center=(350, 580))
        self.settings = settings
        self.apply_color()

    def apply_color(self):
        color = self.settings["car_color"]
        if color == "red":
            self.image = self.original.copy()
            self.image.fill((255, 60, 60), special_flags=pygame.BLEND_MULT)
        elif color == "blue":
            self.image = self.original.copy()
            self.image.fill((60, 120, 255), special_flags=pygame.BLEND_MULT)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 0:   self.rect.x -= 8
        if keys[K_RIGHT] and self.rect.right < 700: self.rect.x += 8


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.smoothscale(pygame.image.load("assets/images/enemy.png"), (110, 140))
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.x = random.randint(50, 540)
        self.rect.y = random.randint(-700, -150)

    def move(self, speed):
        self.rect.y += speed
        if self.rect.top > 700:
            self.reset()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 35))
        self.image.fill((90, 90, 90))
        pygame.draw.rect(self.image, (40, 40, 40), self.image.get_rect(), 6)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.x = random.randint(40, 560)
        self.rect.y = random.randint(-900, -300)

    def move(self, speed):
        self.rect.y += speed
        if self.rect.top > 700:
            self.reset()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.types = {'nitro': (255, 215, 0), 'shield': (0, 255, 255), 'repair': (0, 255, 120)}
        self.type = random.choice(list(self.types.keys()))
        self.image = pygame.Surface((55, 55), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.types[self.type], (27, 27), 27)
        font = pygame.font.SysFont("Verdana", 28, bold=True)
        self.image.blit(font.render(self.type[0].upper(), True, (0,0,0)), (18, 13))
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.x = random.randint(60, 520)
        self.rect.y = random.randint(-1200, -400)

    def move(self, speed):
        self.rect.y += speed
        if self.rect.top > 700:
            self.reset()