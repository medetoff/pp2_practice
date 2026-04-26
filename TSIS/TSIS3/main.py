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

default_settings = {"sound": True, "car_color": "red", "difficulty": 2}
settings = load_json("settings.json", default_settings)  # грузим настройки из файла, если нет — берём дефолт
leaderboard = load_json("leaderboard.json", [])  # таблица лидеров, если файла нет — пустой список

ui = UI(screen, font, big_font)

# ==================== ИГРОВЫЕ ОБЪЕКТЫ ====================
def create_game_objects():  # создаём все объекты заново (при старте или рестарте)
    global player, enemies, obstacles, powerups, coins
    player = Player(settings)

    enemies = pygame.sprite.Group()  # группа вражеских машин
    obstacles = pygame.sprite.Group()  # группа препятствий
    powerups = pygame.sprite.Group()  # группа бонусов
    coins = pygame.sprite.Group()  # группа монет

    for _ in range(3):  # спавним 3 врага далеко сверху чтобы не умереть сразу
        e = Enemy()
        e.rect.y = random.randint(-900, -500)
        enemies.add(e)

    for _ in range(2):  # 2 препятствия
        o = Obstacle()
        o.rect.y = random.randint(-1000, -600)
        obstacles.add(o)

    for _ in range(2):  # 2 бонуса
        p = PowerUp()
        p.rect.y = random.randint(-1100, -700)
        powerups.add(p)

    for _ in range(4):  # 4 монеты разного размера (чем больше — тем ценнее)
        coin = pygame.sprite.Sprite()
        size = random.choice([25, 40, 55])
        coin.image = pygame.transform.smoothscale(pygame.image.load("assets/images/coin.png"), (size, size))
        coin.rect = coin.image.get_rect()
        coin.rect.x = random.randint(50, 550)
        coin.rect.y = random.randint(-600, -100)
        coin.value = size // 20  # маленькая монета = 1 очко, большая = 2-3
        coins.add(coin)

create_game_objects()

bg = pygame.transform.smoothscale(pygame.image.load("assets/images/road.png"), (700, 700))
bg_y = 0  # для скроллинга фона дороги

score = 0
coins_collected = 0
distance = 0  # пройденная дистанция
speed = 5  # начальная скорость
active_powerup = None  # какой бонус сейчас активен
powerup_timer = 0
player_name = ""
game_state = "menu"  # начинаем с главного меню

def reset_game():  # полный сброс игры к начальному состоянию
    global score, coins_collected, distance, speed, active_powerup, powerup_timer, bg_y
    score = coins_collected = distance = 0
    speed = 5
    active_powerup = None
    powerup_timer = 0
    bg_y = 0
    create_game_objects()

def draw_leaderboard():
    screen.blit(big_font.render("LEADERBOARD", True, (255, 215, 0)), (155, 70))

    if not leaderboard:
        screen.blit(font.render("No records yet", True, (200, 200, 200)), (240, 280))
    else:
        for i, entry in enumerate(leaderboard[:10]):  # показываем максимум 10 записей
            y = 170 + i * 45
            rank = f"{i+1}."
            name = entry["name"][:15].ljust(15)  # обрезаем имя до 15 символов
            score_text = str(entry["score"]).rjust(6)
            dist_text = f"{entry['distance']}m"

            screen.blit(font.render(rank, True, (255, 255, 255)), (80, y))
            screen.blit(font.render(name, True, (255, 255, 255)), (150, y))
            screen.blit(font.render(score_text, True, (0, 255, 100)), (430, y))
            screen.blit(font.render(dist_text, True, (255, 200, 0)), (580, y))

    back_rect = pygame.Rect(280, 620, 140, 55)  # кнопка "назад"
    pygame.draw.rect(screen, (50, 50, 80), back_rect, border_radius=12)
    pygame.draw.rect(screen, (255, 255, 255), back_rect, 2, border_radius=12)
    screen.blit(font.render("BACK", True, (255, 255, 255)), (325, 630))
    return back_rect  # возвращаем rect чтобы потом проверить клик по нему

# ====================== ГЛАВНЫЙ ЦИКЛ ======================
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN and event.button == 1:  # клик левой кнопкой мыши
            pos = event.pos

            if game_state == "menu":
                btns = ui.main_menu()  # получаем словарь кнопок меню
                if btns["play"].collidepoint(pos):  # нажали "играть"
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
                if draw_leaderboard().collidepoint(pos):  # нажали кнопку Back
                    game_state = "menu"

            elif game_state == "game_over":
                btns = ui.game_over(score, distance, coins_collected)
                if btns["retry"].collidepoint(pos):  # переиграть
                    reset_game()
                    game_state = "playing"
                elif btns["menu"].collidepoint(pos):  # в главное меню
                    game_state = "menu"

        if event.type == KEYDOWN and game_state == "name_input":  # ввод имени с клавиатуры
            if event.key == K_RETURN and player_name.strip():  # Enter — начать игру
                reset_game()
                game_state = "playing"
            elif event.key == K_BACKSPACE:
                player_name = player_name[:-1]
            else:
                player_name += event.unicode

    # ====================== ЛОГИКА ИГРЫ ======================
    if game_state == "playing":
        player.update()  # двигаем машину игрока

        for e in enemies: e.move(speed)  # все враги и объекты двигаются вниз
        for o in obstacles: o.move(speed)
        for p in powerups: p.move(speed)
        for c in coins:
            c.rect.y += speed
            if c.rect.top > 700: c.rect.y = -100  # монета ушла за экран — возвращаем наверх

        distance += speed * 0.35  # считаем пройденное расстояние
        score = coins_collected * 15 + int(distance) // 3  # очки = монеты + дистанция
        speed = min(13, 5 + int(distance) // 800)  # чем дальше проехал — тем быстрее (максимум 13)

        # Проверка столкновений с врагами и препятствиями
        if pygame.sprite.spritecollideany(player, enemies) or pygame.sprite.spritecollideany(player, obstacles):
            if active_powerup == "shield":  # если щит активен — выживаем один раз
                active_powerup = None
            else:  # иначе — конец игры
                leaderboard.append({"name": player_name, "score": score, "distance": int(distance)})
                leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]  # сортируем и обрезаем до топ-10
                save_json("leaderboard.json", leaderboard)  # сохраняем в файл
                game_state = "game_over"

        for c in pygame.sprite.spritecollide(player, coins, False):  # подобрали монету
            coins_collected += c.value
            c.rect.y = -200  # прячем монету обратно наверх

        for p in pygame.sprite.spritecollide(player, powerups, False):  # подобрали бонус
            active_powerup = p.type
            powerup_timer = 300 if p.type == "nitro" else 999  # нитро на 300 тиков, щит подольше
            if p.type == "repair":  # ремонт сразу даёт очки и не остаётся активным
                score += 150
                active_powerup = None
            p.reset()

        if active_powerup and powerup_timer > 0:  # отсчитываем таймер активного бонуса
            powerup_timer -= 1
            if powerup_timer <= 0:
                active_powerup = None

    # ====================== ОТРИСОВКА ======================
    screen.blit(bg, (0, bg_y))  # рисуем фон дороги дважды для бесконечного скролла
    screen.blit(bg, (0, bg_y - 700))
    bg_y = (bg_y + (speed if game_state == "playing" else 4)) % 700  # фон двигается даже в меню (медленнее)

    if game_state == "playing":
        screen.blit(player.image, player.rect)  # рисуем машину игрока
        enemies.draw(screen)  # рисуем врагов
        obstacles.draw(screen)  # препятствия
        powerups.draw(screen)  # бонусы
        coins.draw(screen)  # монеты

        screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (20, 15))  # HUD — очки, дистанция, монеты
        screen.blit(font.render(f"Distance: {int(distance)}m", True, (255, 255, 255)), (20, 55))
        screen.blit(font.render(f"Coins: {coins_collected}", True, (255, 255, 255)), (480, 15))

        if active_powerup:  # если бонус активен — показываем его название
            screen.blit(font.render(active_powerup.upper(), True, (255, 215, 0)), (290, 15))

    elif game_state == "menu":
        ui.main_menu()
    elif game_state == "name_input":
        ui.name_input(player_name)
    elif game_state == "game_over":
        ui.game_over(score, distance, coins_collected)
    elif game_state == "leaderboard":
        draw_leaderboard()

    pygame.display.update()  # обновляем экран
    clock.tick(60)  # 60 кадров в секунду

pygame.quit()
sys.exit()