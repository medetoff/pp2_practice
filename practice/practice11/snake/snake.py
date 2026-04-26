import pygame, sys, random

pygame.init()

# Константы
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game: Extended")
clock = pygame.time.Clock()

# Цвета (оставил как в прошлом "крутом" варианте)
BG, HEAD, BODY = (232, 244, 248), (21, 101, 192), (66, 165, 245)
FOOD_COLOR, TEXT = (229, 57, 53), (21, 101, 192)
font = pygame.font.SysFont("Verdana", 24)

# Начальные настройки
snake = [(100, 100), (80, 100), (60, 100)]
direction = (CELL_SIZE, 0)
score, level, foods_eaten, speed = 0, 1, 0, 10
FOOD_LIMIT = 80 # Время существование еды

def generate_food():
    """Создаем еду с разным весом"""
    while True:
        x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        if (x, y) not in snake:
            weight = random.randint(1, 3)      
            size = weight * 10    
            return (x, y, weight, size)

food = generate_food()
food_timer = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, CELL_SIZE): direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE): direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0): direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0): direction = (CELL_SIZE, 0)

    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    if (new_head[0] < 0 or new_head[0] >= WIDTH or 
        new_head[1] < 0 or new_head[1] >= HEIGHT or 
        new_head in snake):
        pygame.quit(); sys.exit()

    snake.insert(0, new_head)
    
    food_timer += 1
    if food_timer >= FOOD_LIMIT:
        food = generate_food()
        food_timer = 0

    if new_head[0] == food[0] and new_head[1] == food[1]:
        score += food[2]       
        foods_eaten += 1       
        food = generate_food() 
        food_timer = 0
        
        if foods_eaten % 3 == 0:
            level += 1
            speed += 2
    else:
        snake.pop() 

    # Отрисовка
    screen.fill(BG)
    

    for block in snake:
        pygame.draw.rect(screen, BODY, (block[0], block[1], CELL_SIZE, CELL_SIZE))
    
    # Рисуем голову чуть другим цветом, чтобы понимать направление (тоже полный квадрат)
    pygame.draw.rect(screen, HEAD, (snake[0][0], snake[0][1], CELL_SIZE, CELL_SIZE))

    
    # Рисуем еду
    pygame.draw.rect(screen, FOOD_COLOR, (food[0], food[1], food[3], food[3]))
    
    # Статистика
    screen.blit(font.render(f"Score: {score}", True, TEXT), (10, 10))
    screen.blit(font.render(f"Level: {level}", True, TEXT), (10, 40))
    screen.blit(font.render(f"Weight: {food[2]}", True, FOOD_COLOR), (WIDTH - 150, 10))

    pygame.display.update()
    clock.tick(speed)