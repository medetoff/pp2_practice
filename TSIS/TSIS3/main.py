import pygame, sys, random
from pygame.locals import *
from racer import Player, Enemy, Obstacle, PowerUp
from ui import UI
from persistence import load_json, save_json

pygame.init()
screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Racer - TSIS 3")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 32)
big_font = pygame.font.SysFont("Verdana", 60)

# Настройки
default_settings = {"sound": True, "car_color": "red", "difficulty": 2}
settings = load_json("settings.json", default_settings)
leaderboard = load_json("leaderboard.json", [])

ui = UI(screen, font, big_font)

# ==================== ИГРОВЫЕ ОБЪЕКТЫ ====================
def create_game_objects():
    global player, enemies, obstacles, powerups, coins
    player = Player(settings)
    
    enemies = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    coins = pygame.sprite.Group()

    # Спавн далеко сверху (чтобы не врезался сразу)
    for _ in range(3):
        e = Enemy()
        e.rect.y = random.randint(-900, -500)
        enemies.add(e)

    for _ in range(2):
        o = Obstacle()
        o.rect.y = random.randint(-1000, -600)
        obstacles.add(o)

    for _ in range(2):
        p = PowerUp()
        p.rect.y = random.randint(-1100, -700)
        powerups.add(p)

    for _ in range(4):
        coin = pygame.sprite.Sprite()
        size = random.choice([25, 40, 55])
        coin.image = pygame.transform.smoothscale(pygame.image.load("assets/images/coin.png"), (size, size))
        coin.rect = coin.image.get_rect()
        coin.rect.x = random.randint(50, 550)
        coin.rect.y = random.randint(-600, -100)
        coin.value = size // 20
        coins.add(coin)

create_game_objects()

bg = pygame.transform.smoothscale(pygame.image.load("assets/images/road.png"), (700, 700))
bg_y = 0

# Переменные игры
score = 0
coins_collected = 0
distance = 0
speed = 5
active_powerup = None
powerup_timer = 0
player_name = ""
game_state = "menu"

def reset_game():
    global score, coins_collected, distance, speed, active_powerup, powerup_timer, bg_y
    score = coins_collected = distance = 0
    speed = 5
    active_powerup = None
    powerup_timer = 0
    bg_y = 0
    create_game_objects()        # Полный перезапуск всех объектов

def draw_leaderboard():
    screen.blit(big_font.render("LEADERBOARD", True, (255, 215, 0)), (155, 70))
    
    if not leaderboard:
        screen.blit(font.render("No records yet", True, (200,200,200)), (240, 280))
    else:
        for i, entry in enumerate(leaderboard[:10]):
            y = 170 + i * 45
            rank = f"{i+1}."
            name = entry["name"][:15].ljust(15)
            score_text = str(entry["score"]).rjust(6)
            dist_text = f"{entry['distance']}m"
            
            screen.blit(font.render(rank, True, (255,255,255)), (80, y))
            screen.blit(font.render(name, True, (255,255,255)), (150, y))
            screen.blit(font.render(score_text, True, (0, 255, 100)), (430, y))
            screen.blit(font.render(dist_text, True, (255, 200, 0)), (580, y))

    # Кнопка Back
    back_rect = pygame.Rect(280, 620, 140, 55)
    pygame.draw.rect(screen, (50, 50, 80), back_rect, border_radius=12)
    pygame.draw.rect(screen, (255,255,255), back_rect, 2, border_radius=12)
    screen.blit(font.render("BACK", True, (255,255,255)), (325, 630))
    return back_rect

# ====================== ГЛАВНЫЙ ЦИКЛ ======================
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos

            if game_state == "menu":
                btns = ui.main_menu()
                if btns["play"].collidepoint(pos):
                    game_state = "name_input"
                    player_name = ""
                elif btns["leaderboard"].collidepoint(pos):
                    game_state = "leaderboard"
                elif btns["settings"].collidepoint(pos):
                    game_state = "settings"
                elif btns["quit"].collidepoint(pos):
                    pygame.quit()
                    sys.exit()

            elif game_state == "leaderboard":
                if draw_leaderboard().collidepoint(pos):   # Back
                    game_state = "menu"

            elif game_state == "game_over":
                btns = ui.game_over(score, distance, coins_collected)
                if btns["retry"].collidepoint(pos):
                    reset_game()
                    game_state = "playing"
                elif btns["menu"].collidepoint(pos):
                    game_state = "menu"

        if event.type == KEYDOWN and game_state == "name_input":
            if event.key == K_RETURN and player_name.strip():
                reset_game()
                game_state = "playing"
            elif event.key == K_BACKSPACE:
                player_name = player_name[:-1]
            else:
                player_name += event.unicode

    # ====================== ИГРА ======================
    if game_state == "playing":
        player.update()

        for e in enemies: e.move(speed)
        for o in obstacles: o.move(speed)
        for p in powerups: p.move(speed)
        for c in coins:
            c.rect.y += speed
            if c.rect.top > 700:
                c.rect.y = -100

        distance += speed * 0.35
        score = coins_collected * 15 + int(distance) // 3
        speed = min(13, 5 + int(distance) // 800)

        # Столкновения
        if pygame.sprite.spritecollideany(player, enemies) or pygame.sprite.spritecollideany(player, obstacles):
            if active_powerup == "shield":
                active_powerup = None
            else:
                leaderboard.append({"name": player_name, "score": score, "distance": int(distance)})
                leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]
                save_json("leaderboard.json", leaderboard)
                game_state = "game_over"

        # Сбор монет и power-up'ов
        for c in pygame.sprite.spritecollide(player, coins, False):
            coins_collected += c.value
            c.rect.y = -200

        for p in pygame.sprite.spritecollide(player, powerups, False):
            active_powerup = p.type
            powerup_timer = 300 if p.type == "nitro" else 999
            if p.type == "repair":
                score += 150
                active_powerup = None
            p.reset()

        if active_powerup and powerup_timer > 0:
            powerup_timer -= 1
            if powerup_timer <= 0:
                active_powerup = None

    # ====================== ОТРИСОВКА ======================
    screen.blit(bg, (0, bg_y))
    screen.blit(bg, (0, bg_y - 700))
    bg_y = (bg_y + (speed if game_state == "playing" else 4)) % 700

    if game_state == "playing":
        screen.blit(player.image, player.rect)
        enemies.draw(screen)
        obstacles.draw(screen)
        powerups.draw(screen)
        coins.draw(screen)

        screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (20, 15))
        screen.blit(font.render(f"Distance: {int(distance)}m", True, (255,255,255)), (20, 55))
        screen.blit(font.render(f"Coins: {coins_collected}", True, (255,255,255)), (480, 15))

        if active_powerup:
            screen.blit(font.render(active_powerup.upper(), True, (255,215,0)), (290, 15))

    elif game_state == "menu":
        ui.main_menu()
    elif game_state == "name_input":
        ui.name_input(player_name)
    elif game_state == "game_over":
        ui.game_over(score, distance, coins_collected)
    elif game_state == "leaderboard":
        draw_leaderboard()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()