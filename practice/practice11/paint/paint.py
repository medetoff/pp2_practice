import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    canvas = pygame.Surface(screen.get_size())
    canvas.fill((255, 255, 255))  # белый фон
    radius = 10  # толщина кисти
    mode = "brush"
    color = (0, 0, 255)  # цвет кисти
    drawing = False
    start_pos = None
    last_pos = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                # Режимы рисования
                if event.key == pygame.K_1:
                    mode = "brush"       # кисть
                elif event.key == pygame.K_t:
                    mode = "rect"        # прямоугольник
                elif event.key == pygame.K_c:
                    mode = "circle"      # круг
                elif event.key == pygame.K_e:
                    mode = "eraser"      # ластик
                elif event.key == pygame.K_s:
                    mode = "square"      # квадрат
                elif event.key == pygame.K_q:
                    mode = "right_triangle"  # прямоугольный треугольник
                elif event.key == pygame.K_w:
                    mode = "equilateral_triangle"  # равносторонний треугольник
                elif event.key == pygame.K_z:
                    mode = "rhombus"     # ромб
                # Дополнительные функции
                elif event.key == pygame.K_d:
                    canvas.fill((255, 255, 255))  # очистить холст
                # Выбор цвета
                elif event.key == pygame.K_r:
                    color = (255, 0, 0)  # красный
                elif event.key == pygame.K_g:
                    color = (0, 200, 0)  # зеленый
                elif event.key == pygame.K_b:
                    color = (0, 0, 255)  # синий

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # зажали левую кнопку мыши
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    end_pos = event.pos
                    
                    if mode == "rect":        # Прямоугольник
                        rect = pygame.Rect(start_pos, (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                        pygame.draw.rect(canvas, color, rect, 2)
                    
                    elif mode == "circle":      # Круг
                        dx = end_pos[0] - start_pos[0]
                        dy = end_pos[1] - start_pos[1]
                        r = int((dx**2 + dy**2) ** 0.5)
                        pygame.draw.circle(canvas, color, start_pos, r, 2)
                    
                    elif mode == "square":      # Квадрат
                        dx = end_pos[0] - start_pos[0]
                        dy = end_pos[1] - start_pos[1]
                        side = int((dx**2 + dy**2) ** 0.5)  # длина стороны
                        # Рисуем квадрат от начальной точки
                        square_rect = pygame.Rect(start_pos[0], start_pos[1], side, side)
                        pygame.draw.rect(canvas, color, square_rect, 2)
                    
                    elif mode == "right_triangle":      # Прямоугольный треугольник 
                        # Три точки: начальная, горизонталь вправо, вертикаль вниз
                        point1 = start_pos
                        point2 = (end_pos[0], start_pos[1])  # горизонталь
                        point3 = (start_pos[0], end_pos[1])  # вертикаль
                        pygame.draw.polygon(canvas, color, [point1, point2, point3], 2)
                    
                    elif mode == "equilateral_triangle":     
                        dx = end_pos[0] - start_pos[0] # Равносторонний треугольник
                        dy = end_pos[1] - start_pos[1]
                        side = (dx**2 + dy**2) ** 0.5  # длина стороны
                        # Считаем три вершины равностороннего треугольника
                        # Верхняя точка
                        point1 = (start_pos[0], start_pos[1] - int(side * math.sqrt(3) / 2))
                        # Левая нижняя
                        point2 = (start_pos[0] - int(side / 2), start_pos[1])
                        # Правая нижняя
                        point3 = (start_pos[0] + int(side / 2), start_pos[1])
                        
                        pygame.draw.polygon(canvas, color, [point1, point2, point3], 2)
                    
                    elif mode == "rhombus":      # Ромб
                        dx = end_pos[0] - start_pos[0]
                        dy = end_pos[1] - start_pos[1]
                        # Четыре вершины ромба относительно начальной точки
                        # Верхняя точка
                        point1 = (start_pos[0], start_pos[1] - abs(dy))
                        # Правая точка
                        point2 = (start_pos[0] + abs(dx), start_pos[1])
                        # Нижняя точка
                        point3 = (start_pos[0], start_pos[1] + abs(dy))
                        # Левая точка
                        point4 = (start_pos[0] - abs(dx), start_pos[1])
                        pygame.draw.polygon(canvas, color, [point1, point2, point3, point4], 2)

            if event.type == pygame.MOUSEMOTION:
                # Рисуем кистью или стираем ластиком
                if drawing and (mode == "brush" or mode == "eraser"):
                    draw_color = (255, 255, 255) if mode == "eraser" else color
                    pygame.draw.line(canvas, draw_color, last_pos, event.pos, radius)
                    last_pos = event.pos

        # Обновляем экран
        screen.fill((255, 255, 255))
        screen.blit(canvas, (0, 0))
        # Показываем подсказки по управлению
        font = pygame.font.Font(None, 24)
        hints = [
            "1-Кисть | T-Прямоугольник | C-Круг | S-Квадрат",
            "Q-Прямоуг.треугольник | W-Равносторон.треугольник | Z-Ромб",
            "E-Ластик | D-Очистить | R-Красный | G-Зеленый | B-Синий"
        ]
        y_offset = 10
        for hint in hints:
            text = font.render(hint, True, (100, 100, 100))
            screen.blit(text, (10, y_offset))
            y_offset += 25
        
        pygame.display.flip()
        clock.tick(60)

main()