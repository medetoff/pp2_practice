import pygame, sys
from pygame.locals import *
import random

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

WHITE  = (255, 255, 255)
DARK   = (47, 79, 79)
RED    = (200, 50, 50)
GREEN  = (50, 200, 50)
BLACK  = (0, 0, 0)
YELLOW = (255, 215, 0)

SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 800

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")

font_big   = pygame.font.Font(None, 80)
font_mid   = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)


def draw_text(text, font, color, x, y, center=True):
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    DISPLAYSURF.blit(surf, rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, speed):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.image = pygame.transform.scale(self.image, (90, 120))
        self.rect  = self.image.get_rect()
        self.rect.center = (start_x, start_y)
        self.base_speed = speed
        self.hit_cooldown = 0  # frames until can hit again

    def move(self, multiplier):
        self.rect.move_ip(0, int(self.base_speed * multiplier))
        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0
            self.rect.centerx = random.randint(40, SCREEN_WIDTH - 40)
            return "passed"
        return None

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.image = pygame.transform.scale(self.image, (90, 120))
        self.rect  = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


def make_enemies(n=5):
    step = SCREEN_WIDTH // n
    return [
        Enemy(
            start_x=step * i + step // 2,
            start_y=-i * 150,
            speed=random.randint(5, 15)
        )
        for i in range(n)
    ]


def draw_hud(score, lives, multiplier):
    draw_text(f"Score: {score}",        font_small, WHITE,  10, 10,  center=False)
    draw_text(f"Speed: x{multiplier:.1f}", font_small, WHITE, 10, 44, center=False)
    # lives as red circles (no special characters)
    for i in range(3):
        color = RED if i < lives else (80, 80, 80)
        pygame.draw.circle(DISPLAYSURF, color,
                           (SCREEN_WIDTH - 20 - i * 34, 20), 10)


def start_screen():
    while True:
        DISPLAYSURF.fill(DARK)
        draw_text("RACER",               font_big,   YELLOW, SCREEN_WIDTH//2, 240)
        draw_text("Avoid the enemies!",  font_small, WHITE,  SCREEN_WIDTH//2, 340)
        draw_text("LEFT RIGHT to move",  font_small, WHITE,  SCREEN_WIDTH//2, 385)
        draw_text("ESC to pause",        font_small, WHITE,  SCREEN_WIDTH//2, 425)
        draw_text("SPACE to start",      font_mid,   GREEN,  SCREEN_WIDTH//2, 520)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                return

        pygame.display.update()
        FramePerSec.tick(FPS)


def pause_screen():
    # snapshot current frame so background stays visible
    snapshot = DISPLAYSURF.copy()
    while True:
        DISPLAYSURF.blit(snapshot, (0, 0))
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(140)
        overlay.fill(BLACK)
        DISPLAYSURF.blit(overlay, (0, 0))

        draw_text("PAUSED",              font_big,   YELLOW, SCREEN_WIDTH//2, 300)
        draw_text("SPACE to continue",   font_small, WHITE,  SCREEN_WIDTH//2, 400)
        draw_text("Q to quit",           font_small, WHITE,  SCREEN_WIDTH//2, 445)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE or event.key == K_ESCAPE:
                    return          # back to game
                if event.key == K_q:
                    pygame.quit(); sys.exit()

        pygame.display.update()
        FramePerSec.tick(FPS)


def game_over_screen(score):
    while True:
        DISPLAYSURF.fill(DARK)
        draw_text("GAME OVER",                font_big,   RED,    SCREEN_WIDTH//2, 260)
        draw_text(f"Score: {score}",          font_mid,   YELLOW, SCREEN_WIDTH//2, 380)
        draw_text("SPACE to play again",      font_small, WHITE,  SCREEN_WIDTH//2, 470)
        draw_text("Q to quit",                font_small, WHITE,  SCREEN_WIDTH//2, 515)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return True
                if event.key == K_q:
                    pygame.quit(); sys.exit()

        pygame.display.update()
        FramePerSec.tick(FPS)


def run_game():
    P1      = Player()
    enemies = make_enemies(5)
    score   = 0
    lives   = 3
    frame   = 0
    MAX_MUL = 4.0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pause_screen()

        multiplier = min(1.0 + (frame // 300) * 0.2, MAX_MUL)
        frame += 1

        P1.update()

        for enemy in enemies:
            result = enemy.move(multiplier)

            # enemy passed bottom — lose a life, +0 score
            if result == "passed":
                lives -= 1
                if lives <= 0:
                    return score

            # collision — lose a life, cooldown prevents multi-hit
            elif pygame.sprite.collide_rect(P1, enemy) and enemy.hit_cooldown == 0:
                lives -= 1
                enemy.hit_cooldown = 90   # 1.5 seconds immunity
                enemy.rect.centery = -200
                if lives <= 0:
                    return score
            
            # enemy successfully dodged (passed top→bottom without hitting)
            elif result is None and enemy.rect.top > SCREEN_HEIGHT - 1:
                score += 1  # point per enemy dodged

        # score: 1 point per enemy that passed the player safely
        # recalculate cleanly — count enemies that went off screen this frame
        DISPLAYSURF.fill(DARK)
        P1.draw(DISPLAYSURF)
        for enemy in enemies:
            enemy.draw(DISPLAYSURF)

        draw_hud(score, lives, multiplier)
        pygame.display.update()
        FramePerSec.tick(FPS)


start_screen()

while True:
    final_score = run_game()
    game_over_screen(final_score)