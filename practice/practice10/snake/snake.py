import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# основные цвета игры
BG = (232, 244, 248)
HEAD = (21, 101, 192)
BODY = (66, 165, 245)
FOOD = (229, 57, 53)
TEXT = (21, 101, 192)

font = pygame.font.SysFont("Verdana", 24)

# змейка хранится как список координат (первая — голова)
snake = [(100, 100), (80, 100), (60, 100)]
direction = (CELL_SIZE, 0)  # начальное движение вправо

# генерация еды в случайном месте (не внутри змейки)
def generate_food():
    while True:
        x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        if (x, y) not in snake:
            return (x, y)

food = generate_food()

score = 0
level = 1
foods_to_next_level = 3
speed = 12

# проверка столкновений
def check_wall_collision(head):
    return head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT

def check_self_collision(head):
    return head in snake[1:]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # управление змейкой (нельзя двигаться назад)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                direction = (CELL_SIZE, 0)

    # создаем новую позицию головы
    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])

    # если столкновение — игра заканчивается
    if check_wall_collision(new_head) or check_self_collision(new_head):
        pygame.quit()
        sys.exit()

    snake.insert(0, new_head)

    # если съели еду — растем, иначе двигаемся
    if new_head == food:
        score += 1
        foods_to_next_level -= 1
        food = generate_food()
    else:
        snake.pop()

    # повышение уровня и увеличение скорости
    if foods_to_next_level == 0:
        level += 1
        foods_to_next_level = 3
        speed += 2

    # отрисовка
    screen.fill(BG)

    for block in snake:
        pygame.draw.rect(screen, BODY, (block[0], block[1], CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, HEAD, (snake[0][0], snake[0][1], CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, FOOD, (food[0], food[1], CELL_SIZE, CELL_SIZE))

    # отображение счета и уровня
    screen.blit(font.render(f"Score: {score}", True, TEXT), (10, 10))
    screen.blit(font.render(f"Level: {level}", True, TEXT), (10, 40))

    pygame.display.update()
    clock.tick(speed)  # регулирует скорость игры