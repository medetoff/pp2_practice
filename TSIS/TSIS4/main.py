import pygame, sys, random, json
from db import save_score, get_top_10, get_personal_best

pygame.init()  # запускаем движок pygame
WIDTH, HEIGHT = 800, 600  # размеры окна
CELL = 20  # размер одной клетки
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # создаём окно
clock = pygame.time.Clock()  # таймер для контроля FPS
font = pygame.font.SysFont("Verdana", 24)  # шрифт для текста

try:
    with open("settings.json", "r") as f:  # пробуем загрузить настройки из файла
        settings = json.load(f)
except:
    settings = {"snake_color": [66, 165, 245], "grid": True, "sound": True}  # если файла нет — дефолтные настройки

username = ""  # имя игрока, пока пустое
state = "MENU"  # текущее состояние игры — начинаем с меню

class Game:
    def __init__(self, user):
        self.user = user  # запоминаем имя игрока
        self.snake = [(100, 100), (80, 100), (60, 100)]  # начальное тело змейки — 3 сегмента
        self.direction = (CELL, 0)  # начальное направление — вправо
        self.score = 0  # очки
        self.level = 1  # уровень
        self.speed = 10  # скорость (кадры в секунду)
        self.obstacles = []  # препятствия — пока пусто
        self.food = self.gen_item()  # генерируем еду
        self.poison = self.gen_item()  # генерируем яд
        self.powerup_item = None  # бонус на поле — пока нет
        self.pu_type = None  # тип бонуса
        self.active_pu = None  # активный бонус
        self.pu_timer = 0  # когда бонус закончится
        self.pu_field_timer = 0  # когда можно спавнить новый бонус
        self.shield_active = False  # щит выключен
        self.personal_best = get_personal_best(user)  # лучший результат игрока из базы

    def gen_item(self):  # генерация случайного предмета (еда/яд/бонус)
        while True:
            x = random.randint(0, (WIDTH - CELL) // CELL) * CELL  # случайная x-координата по сетке
            y = random.randint(0, (HEIGHT - CELL) // CELL) * CELL  # случайная y-координата по сетке
            if (x, y) not in self.snake and (x, y) not in self.obstacles:  # проверяем что место свободно
                return (x, y, random.randint(1, 3))  # возвращаем координаты + очки за предмет (1-3)

    def spawn_obstacles(self):  # расставляем препятствия при повышении уровня
        self.obstacles = []  # очищаем старые
        if self.level >= 3:  # препятствия появляются начиная с 3 уровня
            for _ in range(self.level * 2):  # чем выше уровень — тем больше препятствий
                ox = random.randint(0, (WIDTH - CELL) // CELL) * CELL  # случайная позиция
                oy = random.randint(0, (HEIGHT - CELL) // CELL) * CELL
                if abs(ox - self.snake[0][0]) > CELL * 3:  # не ставим слишком близко к голове
                    self.obstacles.append((ox, oy))

    def update(self):  # основная логика — вызывается каждый кадр
        now = pygame.time.get_ticks()  # текущее время в миллисекундах

        if self.active_pu and now > self.pu_timer:  # если бонус истёк
            self.speed = 10 + (self.level * 2)  # возвращаем нормальную скорость
            self.active_pu = None  # убираем бонус

        if not self.powerup_item and now > self.pu_field_timer:  # если на поле нет бонуса и кулдаун прошёл
            if random.random() < 0.02:  # с вероятностью 2% спавним бонус
                self.powerup_item = self.gen_item()  # создаём предмет
                self.pu_type = random.choice(["SPEED", "SLOW", "SHIELD"])  # случайный тип
                self.pu_field_timer = now + 8000  # следующий бонус не раньше чем через 8 сек

        new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])  # новая позиция головы

        if (new_head[0] < 0 or new_head[0] >= WIDTH or  # врезались в стену слева/справа
            new_head[1] < 0 or new_head[1] >= HEIGHT or  # врезались в стену сверху/снизу
            new_head in self.snake or  # врезались в себя
            new_head in self.obstacles):  # врезались в препятствие
            if self.shield_active:  # если щит включён — спасаемся
                self.shield_active = False  # щит тратится
                if new_head in self.obstacles:  # если врезались в блок — убираем его
                    self.obstacles.remove(new_head)
            else:
                return False  # игра окончена

        self.snake.insert(0, new_head)  # добавляем новую голову

        if new_head[0] == self.food[0] and new_head[1] == self.food[1]:  # если голова на еде
            self.score += self.food[2]  # прибавляем очки (сколько стоит эта еда)
            if self.score // 5 > self.level - 1:  # каждые 5 очков — новый уровень
                self.level += 1  # повышаем уровень
                self.speed += 2  # ускоряемся
                self.spawn_obstacles()  # обновляем препятствия
            self.food = self.gen_item()  # новая еда

        elif new_head[0] == self.poison[0] and new_head[1] == self.poison[1]:  # если голова на яде
            if len(self.snake) <= 3:  # если змейка слишком короткая — конец
                return False
            self.snake.pop(); self.snake.pop(); self.snake.pop()  # откусываем 3 сегмента с хвоста
            self.poison = self.gen_item()  # новый яд

        elif (self.powerup_item and  # если есть бонус на поле
              new_head[0] == self.powerup_item[0] and new_head[1] == self.powerup_item[1]):  # и мы на нём
            self.active_pu = self.pu_type  # активируем бонус
            self.pu_timer = now + 5000  # действует 5 секунд
            if self.active_pu == "SPEED":  # ускорение
                self.speed += 7
            elif self.active_pu == "SLOW":  # замедление
                self.speed = max(5, self.speed - 5)
            elif self.active_pu == "SHIELD":  # щит — одно столкновение бесплатно
                self.shield_active = True
            self.powerup_item = None  # убираем бонус с поля
        else:
            self.snake.pop()  # если ничего не съели — убираем хвост (змейка не растёт)

        return True  # всё ок, игра продолжается

def draw_grid():  # рисуем сетку на фоне
    if settings["grid"]:  # если в настройках сетка включена
        for x in range(0, WIDTH, CELL):  # вертикальные линии
            pygame.draw.line(screen, (220, 220, 220), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL):  # горизонтальные линии
            pygame.draw.line(screen, (220, 220, 220), (0, y), (WIDTH, y))

game = None  # объект игры — пока не создан
while True:  # главный бесконечный цикл
    screen.fill((240, 240, 240))  # заливаем фон светло-серым
    for event in pygame.event.get():  # обрабатываем все события
        if event.type == pygame.QUIT:  # нажали крестик
            pygame.quit(); sys.exit()

        if state == "MENU":  # обработка ввода в меню
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username:  # Enter — начать игру (если имя введено)
                    game = Game(username); state = "GAME"
                elif event.key == pygame.K_BACKSPACE:  # Backspace — стереть символ
                    username = username[:-1]
                elif event.key == pygame.K_l:  # L — таблица лидеров
                    state = "LEADERBOARD"
                elif event.key == pygame.K_s:  # S — настройки
                    state = "SETTINGS"
                else:
                    if len(username) < 12:  # ограничение длины имени
                        username += event.unicode  # добавляем введённый символ

    if state == "MENU":  # отрисовка меню
        screen.blit(font.render("SNAKE ADVENTURE", True, (0, 0, 0)), (280, 100))  # заголовок
        screen.blit(font.render(f"Enter Name: {username}_", True, settings["snake_color"]), (250, 200))  # поле ввода имени
        screen.blit(font.render("Enter: Start | L: Leaderboard | S: Settings", True, (100, 100, 100)), (180, 300))  # подсказки

    elif state == "GAME":  # игровой процесс
        draw_grid()  # рисуем сетку
        keys = pygame.key.get_pressed()  # считываем зажатые клавиши
        if keys[pygame.K_UP] and game.direction != (0, CELL):  # вверх (нельзя развернуться на 180°)
            game.direction = (0, -CELL)
        if keys[pygame.K_DOWN] and game.direction != (0, -CELL):  # вниз
            game.direction = (0, CELL)
        if keys[pygame.K_LEFT] and game.direction != (CELL, 0):  # влево
            game.direction = (-CELL, 0)
        if keys[pygame.K_RIGHT] and game.direction != (-CELL, 0):  # вправо
            game.direction = (CELL, 0)

        if not game.update():  # обновляем игру, если вернула False — конец
            save_score(game.user, game.score, game.level)  # сохраняем результат в базу
            state = "GAMEOVER"

        for b in game.snake:  # рисуем каждый сегмент змейки
            pygame.draw.rect(screen, settings["snake_color"], (b[0], b[1], CELL - 1, CELL - 1))
        for o in game.obstacles:  # рисуем препятствия чёрными квадратами
            pygame.draw.rect(screen, (0, 0, 0), (o[0], o[1], CELL, CELL))
        pygame.draw.rect(screen, (0, 200, 0), (game.food[0], game.food[1], CELL, CELL))  # еда — зелёный квадрат
        pygame.draw.rect(screen, (150, 0, 0), (game.poison[0], game.poison[1], CELL, CELL))  # яд — тёмно-красный квадрат
        if game.powerup_item:  # бонус — жёлтый кружок
            pygame.draw.ellipse(screen, (255, 200, 0), (game.powerup_item[0], game.powerup_item[1], CELL, CELL))

        txt = f"Score: {game.score} | Level: {game.level} | Best: {game.personal_best}"  # строка статуса
        if game.shield_active:  # если щит активен — показываем
            txt += " | SHIELD ON"
        screen.blit(font.render(txt, True, (0, 0, 0)), (10, 10))  # выводим статус сверху
        clock.tick(game.speed)  # ограничиваем FPS скоростью игры

    elif state == "GAMEOVER":  # экран проигрыша
        screen.blit(font.render("GAME OVER", True, (200, 0, 0)), (330, 200))  # надпись красным
        screen.blit(font.render(f"Final Score: {game.score} | Press M", True, (0, 0, 0)), (280, 250))  # итог + подсказка
        if pygame.key.get_pressed()[pygame.K_m]:  # M — вернуться в меню
            state = "MENU"

    elif state == "LEADERBOARD":  # таблица лидеров
        screen.blit(font.render("LEADERBOARD (TOP 10)", True, (0, 0, 0)), (280, 50))  # заголовок
        top = get_top_10()  # получаем топ-10 из базы
        if not top:  # если пусто
            screen.blit(font.render("No data yet", True, (100, 100, 100)), (330, 200))
        for i, r in enumerate(top):  # выводим каждую строчку рейтинга
            screen.blit(font.render(f"{i + 1}. {r[0]} - {r[1]} pts", True, (50, 50, 50)), (280, 100 + i * 35))
        screen.blit(font.render("Press M for Menu", True, (200, 0, 0)), (300, 520))  # подсказка внизу
        if pygame.key.get_pressed()[pygame.K_m]:  # M — назад в меню
            state = "MENU"

    elif state == "SETTINGS":  # экран настроек
        screen.blit(font.render("SETTINGS", True, (0, 0, 0)), (350, 50))  # заголовок
        screen.blit(font.render(f"G: Toggle Grid ({settings['grid']})", True, (0, 0, 0)), (300, 150))  # вкл/выкл сетку
        screen.blit(font.render("M: Save & Exit", True, (0, 0, 0)), (300, 250))  # сохранить и выйти
        if pygame.key.get_pressed()[pygame.K_g]:  # G — переключить сетку
            settings["grid"] = not settings["grid"]
            pygame.time.delay(150)  # задержка чтобы не переключалось 100 раз в секунду
        if pygame.key.get_pressed()[pygame.K_m]:  # M — сохраняем настройки в файл и выходим
            with open("settings.json", "w") as f:
                json.dump(settings, f)
            state = "MENU"

    pygame.display.update()  # обновляем экран — показываем всё нарисованное