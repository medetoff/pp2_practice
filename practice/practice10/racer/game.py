import pygame, sys
from pygame.locals import *
import random

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Размеры экрана и цвета
SCREEN_WIDTH  = 700
SCREEN_HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")
font = pygame.font.SysFont("Verdana", 30)

# Игровые переменные
score           = 0
coins_collected = 0
speed           = 5


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load("images/enemy.png")
        self.image = pygame.transform.smoothscale(img, (110, 140))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = 0

    def move(self):
        global score, speed
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:  # Враг вышел за экран — очко игроку
            score += 1
            speed += 0.2
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = 0


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load("images/car.png")
        self.image = pygame.transform.smoothscale(img, (110, 140))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 0:       # Движение влево
            self.rect.move_ip(-7, 0)
        if keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:  # Движение вправо
            self.rect.move_ip(7, 0)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load("images/coin.png")
        self.image = pygame.transform.smoothscale(img, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-300, -50)

    def move(self):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:  # Монета вышла — сбрасываем наверх
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-300, -50)


P1 = Player()
E1 = Enemy()
C1 = Coin()

# Главный игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    P1.update()
    E1.move()
    C1.move()

    if P1.rect.inflate(-40, -40).colliderect(E1.rect.inflate(-40, -40)):  # Столкновение с врагом — конец игры
        text = font.render("GAME OVER", True, BLACK)
        DISPLAYSURF.blit(text, text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    if pygame.sprite.collide_rect(P1, C1):  # Подбор монеты
        coins_collected += 1
        C1.rect.x = random.randint(0, SCREEN_WIDTH - C1.rect.width)
        C1.rect.y = random.randint(-300, -50)

    bg = pygame.transform.smoothscale(pygame.image.load("images/road.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
    DISPLAYSURF.blit(bg, (0, 0))
    DISPLAYSURF.blit(P1.image, P1.rect)
    DISPLAYSURF.blit(E1.image, E1.rect)
    DISPLAYSURF.blit(C1.image, C1.rect)
    DISPLAYSURF.blit(font.render(f"Score: {score}", True, WHITE), (20, 20))
    DISPLAYSURF.blit(font.render(f"Coins: {coins_collected}", True, WHITE), (SCREEN_WIDTH - 200, 20))

    pygame.display.update()
    FramePerSec.tick(FPS)