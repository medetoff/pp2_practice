import pygame, sys, random
from pygame.locals import *

pygame.init()

# ----------- НАСТРОЙКИ ИГРЫ -----------
SCREEN_WIDTH, SCREEN_HEIGHT = 700, 700
WHITE, BLACK = (255,255,255), (0,0,0)
FPS = 60

speed = 5                 # начальная скорость врага
score = 0                 # очки за пропущенных врагов
coins_collected = 0       # сколько монет собрано
COINS_TO_LEVEL_UP = 5     # каждые 5 монет увеличиваем скорость

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 30)

# Загружаем картинки один раз (чтобы не грузить каждый кадр)
bg = pygame.transform.smoothscale(pygame.image.load("images/road.png"), (700,700))
car_img = pygame.transform.smoothscale(pygame.image.load("images/car.png"), (110,140))
enemy_img = pygame.transform.smoothscale(pygame.image.load("images/enemy.png"), (110,140))
coin_img = pygame.image.load("images/coin.png")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = car_img
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT-120)) # ставим машину по центру внизу

    def update(self):
        # движение влево и вправо
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= 7
        if keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += 7

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()

        self.reset()  # сразу ставим в начальную позицию
    def reset(self):
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        # появление сверху в случайном месте

        self.rect.y = 0
    def move(self):
        self.rect.y += speed  # двигаем вниз
        global score

        # если враг вышел за экран — добавляем очко
        if self.rect.top > SCREEN_HEIGHT:
            score += 1
            self.reset()
class Coin(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        # случайный размер монеты

        self.size = random.choice([20,40,60])

        self.value = self.size // 20   # 1, 2 или 3 очка
        self.image = pygame.transform.smoothscale(coin_img,(self.size,self.size))
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        # появляется сверху в случайном месте
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-300,-50)

    def move(self):
        self.rect.y += speed

        # если улетела вниз — возвращаем обратно наверх
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

player = Player()
enemy = Enemy()

# создаём сразу 3 монеты
coins = pygame.sprite.Group(Coin(), Coin(), Coin())


while True: # цикл игры
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # обновляем движение
    player.update()
    enemy.move()
    for coin in coins:
        coin.move()

    # проверка столкновения с врагом
    if player.rect.inflate(-60,-60).colliderect(enemy.rect.inflate(-60,-60)):
        text = font.render("GAME OVER",True,BLACK)
        screen.blit(text, text.get_rect(center=(350,350)))
        pygame.display.update()
        pygame.time.delay(2000)
        break

    # проверка сбора монет
    for coin in coins:
        if player.rect.colliderect(coin.rect):
            coins_collected += coin.value
            coin.reset()

            # каждые 5 монет увеличиваем скорость
            if coins_collected % COINS_TO_LEVEL_UP == 0:
                speed += 1

    # отрисовка
    screen.blit(bg,(0,0))
    screen.blit(player.image,player.rect)
    screen.blit(enemy.image,enemy.rect)

    for coin in coins:
        screen.blit(coin.image,coin.rect)

    # вывод информации на экран
    screen.blit(font.render(f"Score: {score}",True,WHITE),(20,20))
    screen.blit(font.render(f"Coins: {coins_collected}",True,WHITE),(500,20))
    screen.blit(font.render(f"Speed: {speed}",True,WHITE),(20,60))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()