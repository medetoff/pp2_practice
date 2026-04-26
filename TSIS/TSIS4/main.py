import pygame, sys, random, json
from db import save_score, get_top_10, get_personal_best

# Инициализация
pygame.init()
WIDTH, HEIGHT = 800, 600
CELL = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 24)

# Загрузка настроек
try:
    with open("settings.json", "r") as f:
        settings = json.load(f)
except:
    settings = {"snake_color": [66, 165, 245], "grid": True, "sound": True}

username = ""
state = "MENU"

class Game:
    def __init__(self, user):
        self.user = user
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = (CELL, 0)
        self.score = 0
        self.level = 1
        self.speed = 10
        
        # Сначала инициализируем препятствия, потом генерим еду!
        self.obstacles = []
        self.food = self.gen_item()
        self.poison = self.gen_item()
        
        # Бонусы
        self.powerup_item = None
        self.pu_type = None
        self.active_pu = None
        self.pu_timer = 0
        self.pu_field_timer = 0
        
        self.shield_active = False
        self.personal_best = get_personal_best(user)

    def gen_item(self):
        while True:
            x = random.randint(0, (WIDTH-CELL)//CELL)*CELL
            y = random.randint(0, (HEIGHT-CELL)//CELL)*CELL
            if (x,y) not in self.snake and (x,y) not in self.obstacles:
                return (x, y, random.randint(1, 3))

    def spawn_obstacles(self):
        self.obstacles = []
        if self.level >= 3:
            for _ in range(self.level * 2):
                ox = random.randint(0, (WIDTH-CELL)//CELL)*CELL
                oy = random.randint(0, (HEIGHT-CELL)//CELL)*CELL
                # Не ставим рядом с головой змеи
                if abs(ox - self.snake[0][0]) > CELL*3:
                    self.obstacles.append((ox, oy))

    def update(self):
        now = pygame.time.get_ticks()

        # Эффекты бонусов
        if self.active_pu and now > self.pu_timer:
            self.speed = 10 + (self.level * 2)
            self.active_pu = None

        # Появление бонуса на поле
        if not self.powerup_item and now > self.pu_field_timer:
            if random.random() < 0.02:
                self.powerup_item = self.gen_item()
                self.pu_type = random.choice(["SPEED", "SLOW", "SHIELD"])
                self.pu_field_timer = now + 8000 

        # Движение
        new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])

        # Проверка столкновений
        if (new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT 
            or new_head in self.snake or new_head in self.obstacles):
            if self.shield_active:
                self.shield_active = False
                if new_head in self.obstacles: self.obstacles.remove(new_head)
            else:
                return False

        self.snake.insert(0, new_head)

        # Еда
        if new_head[0] == self.food[0] and new_head[1] == self.food[1]:
            self.score += self.food[2]
            if self.score // 5 > self.level - 1:
                self.level += 1
                self.speed += 2
                self.spawn_obstacles()
            self.food = self.gen_item()
        
        # Яд
        elif new_head[0] == self.poison[0] and new_head[1] == self.poison[1]:
            if len(self.snake) <= 3: return False
            self.snake.pop(); self.snake.pop(); self.snake.pop()
            self.poison = self.gen_item()

        # Бонус
        elif self.powerup_item and new_head[0] == self.powerup_item[0] and new_head[1] == self.powerup_item[1]:
            self.active_pu = self.pu_type
            self.pu_timer = now + 5000
            if self.active_pu == "SPEED": self.speed += 7
            elif self.active_pu == "SLOW": self.speed = max(5, self.speed - 5)
            elif self.active_pu == "SHIELD": self.shield_active = True
            self.powerup_item = None
        else:
            self.snake.pop()
        
        return True

def draw_grid():
    if settings["grid"]:
        for x in range(0, WIDTH, CELL): pygame.draw.line(screen, (220, 220, 220), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL): pygame.draw.line(screen, (220, 220, 220), (0, y), (WIDTH, y))

# ГЛАВНЫЙ ЦИКЛ
game = None
while True:
    screen.fill((240, 240, 240))
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        
        if state == "MENU":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username:
                    game = Game(username); state = "GAME"
                elif event.key == pygame.K_BACKSPACE: username = username[:-1]
                elif event.key == pygame.K_l: state = "LEADERBOARD"
                elif event.key == pygame.K_s: state = "SETTINGS"
                else:
                    if len(username) < 12: username += event.unicode

    if state == "MENU":
        screen.blit(font.render("SNAKE ADVENTURE", True, (0,0,0)), (280, 100))
        screen.blit(font.render(f"Enter Name: {username}_", True, settings["snake_color"]), (250, 200))
        screen.blit(font.render("Enter: Start | L: Leaderboard | S: Settings", True, (100,100,100)), (180, 300))

    elif state == "GAME":
        draw_grid()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and game.direction != (0, CELL): game.direction = (0, -CELL)
        if keys[pygame.K_DOWN] and game.direction != (0, -CELL): game.direction = (0, CELL)
        if keys[pygame.K_LEFT] and game.direction != (CELL, 0): game.direction = (-CELL, 0)
        if keys[pygame.K_RIGHT] and game.direction != (-CELL, 0): game.direction = (CELL, 0)

        if not game.update():
            save_score(game.user, game.score, game.level)
            state = "GAMEOVER"
        
        # Отрисовка
        for b in game.snake: pygame.draw.rect(screen, settings["snake_color"], (b[0], b[1], CELL-1, CELL-1))
        for o in game.obstacles: pygame.draw.rect(screen, (0,0,0), (o[0], o[1], CELL, CELL))
        pygame.draw.rect(screen, (0, 200, 0), (game.food[0], game.food[1], CELL, CELL))
        pygame.draw.rect(screen, (150, 0, 0), (game.poison[0], game.poison[1], CELL, CELL))
        if game.powerup_item: pygame.draw.ellipse(screen, (255, 200, 0), (game.powerup_item[0], game.powerup_item[1], CELL, CELL))

        txt = f"Score: {game.score} | Level: {game.level} | Best: {game.personal_best}"
        if game.shield_active: txt += " | SHIELD ON"
        screen.blit(font.render(txt, True, (0,0,0)), (10, 10))
        clock.tick(game.speed)

    elif state == "GAMEOVER":
        screen.blit(font.render("GAME OVER", True, (200, 0, 0)), (330, 200))
        screen.blit(font.render(f"Final Score: {game.score} | Press M", True, (0,0,0)), (280, 250))
        if pygame.key.get_pressed()[pygame.K_m]: state = "MENU"

    elif state == "LEADERBOARD":
        screen.blit(font.render("LEADERBOARD (TOP 10)", True, (0,0,0)), (280, 50))
        top = get_top_10()
        if not top: screen.blit(font.render("No data yet", True, (100,100,100)), (330, 200))
        for i, r in enumerate(top):
            screen.blit(font.render(f"{i+1}. {r[0]} - {r[1]} pts", True, (50,50,50)), (280, 100 + i*35))
        screen.blit(font.render("Press M for Menu", True, (200,0,0)), (300, 520))
        if pygame.key.get_pressed()[pygame.K_m]: state = "MENU"

    elif state == "SETTINGS":
        screen.blit(font.render("SETTINGS", True, (0,0,0)), (350, 50))
        screen.blit(font.render(f"G: Toggle Grid ({settings['grid']})", True, (0,0,0)), (300, 150))
        screen.blit(font.render("M: Save & Exit", True, (0,0,0)), (300, 250))
        if pygame.key.get_pressed()[pygame.K_g]:
            settings["grid"] = not settings["grid"]
            pygame.time.delay(150)
        if pygame.key.get_pressed()[pygame.K_m]:
            with open("settings.json", "w") as f: json.dump(settings, f)
            state = "MENU"

    pygame.display.update()