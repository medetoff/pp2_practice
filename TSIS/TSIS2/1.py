import pygame
import math
from datetime import datetime

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    canvas = pygame.Surface(screen.get_size())
    canvas.fill((255, 255, 255))
    
    # Настройки
    brush_size = 2  # размер кисти (2, 5, 10)
    mode = "pencil"
    color = (0, 0, 255)
    drawing = False
    start_pos = None
    last_pos = None
    temp_canvas = None  # для превью
    
    # Текстовый режим
    text_mode = False
    text_pos = None
    text_input = ""
    font = pygame.font.SysFont("Arial", 24)

    # Заливка (flood fill)
    def flood_fill(surf, pos, target_color, fill_color):
        if target_color == fill_color:
            return
        w, h = surf.get_size()
        stack = [pos]
        visited = set()
        
        while stack:
            x, y = stack.pop()
            if (x, y) in visited or x < 0 or x >= w or y < 0 or y >= h:
                continue
            if surf.get_at((x, y))[:3] != target_color:
                continue
            
            surf.set_at((x, y), fill_color)
            visited.add((x, y))
            stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                
                # Сохранение (Ctrl+S)
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"paint_{timestamp}.png"
                    pygame.image.save(canvas, filename)
                    print(f"Сохранено: {filename}")
                
                # Инструменты
                if event.key == pygame.K_p: mode = "pencil"      # карандаш
                elif event.key == pygame.K_l: mode = "line"      # прямая линия
                elif event.key == pygame.K_t: mode = "rect"
                elif event.key == pygame.K_c: mode = "circle"
                elif event.key == pygame.K_e: mode = "eraser"
                elif event.key == pygame.K_o: mode = "square"
                elif event.key == pygame.K_q: mode = "right_triangle"
                elif event.key == pygame.K_w: mode = "equilateral_triangle"
                elif event.key == pygame.K_z: mode = "rhombus"
                elif event.key == pygame.K_f: mode = "fill"      # заливка
                elif event.key == pygame.K_x: mode = "text"      # текст
                elif event.key == pygame.K_d: canvas.fill((255, 255, 255))
                
                # Размер кисти
                elif event.key == pygame.K_1: brush_size = 2
                elif event.key == pygame.K_2: brush_size = 5
                elif event.key == pygame.K_3: brush_size = 10
                
                # Цвета
                elif event.key == pygame.K_r: color = (255, 0, 0)
                elif event.key == pygame.K_g: color = (0, 200, 0)
                elif event.key == pygame.K_b: color = (0, 0, 255)
                elif event.key == pygame.K_k: color = (0, 0, 0)  # черный
                
                # Текстовый ввод
                if text_mode:
                    if event.key == pygame.K_RETURN:
                        if text_input:
                            text_surf = font.render(text_input, True, color)
                            canvas.blit(text_surf, text_pos)
                        text_mode = False
                        text_input = ""
                    elif event.key == pygame.K_ESCAPE:
                        text_mode = False
                        text_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    else:
                        text_input += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos
                    
                    # Заливка - выполняем сразу
                    if mode == "fill":
                        target = canvas.get_at(event.pos)[:3]
                        flood_fill(canvas, event.pos, target, color)
                        drawing = False
                    
                    # Текст - включаем режим ввода
                    elif mode == "text":
                        text_mode = True
                        text_pos = event.pos
                        text_input = ""
                        drawing = False
                    
                    # Для фигур создаем временный холст (для превью)
                    if mode in ["line", "rect", "circle", "square", "right_triangle", 
                                "equilateral_triangle", "rhombus"]:
                        temp_canvas = canvas.copy()

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    # Карандаш - свободное рисование
                    if mode == "pencil":
                        if last_pos:
                            pygame.draw.line(canvas, color, last_pos, event.pos, brush_size)
                        last_pos = event.pos
                    
                    # Ластик
                    elif mode == "eraser":
                        if last_pos:
                            pygame.draw.line(canvas, (255, 255, 255), last_pos, event.pos, brush_size * 2)
                        last_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing and start_pos and event.button == 1:
                    end_pos = event.pos
                    
                    # Рисуем финальные фигуры
                    if mode == "line":
                        pygame.draw.line(canvas, color, start_pos, end_pos, brush_size)
                    
                    elif mode == "rect":
                        rect = pygame.Rect(start_pos, (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                        pygame.draw.rect(canvas, color, rect, brush_size)
                    
                    elif mode == "circle":
                        dx = end_pos[0] - start_pos[0]
                        dy = end_pos[1] - start_pos[1]
                        r = int((dx**2 + dy**2) ** 0.5)
                        if r > 0:
                            pygame.draw.circle(canvas, color, start_pos, r, brush_size)
                    
                    elif mode == "square":
                        dx = end_pos[0] - start_pos[0]
                        dy = end_pos[1] - start_pos[1]
                        side = int((dx**2 + dy**2) ** 0.5)
                        pygame.draw.rect(canvas, color, pygame.Rect(start_pos[0], start_pos[1], side, side), brush_size)
                    
                    elif mode == "right_triangle":
                        p1, p2, p3 = start_pos, (end_pos[0], start_pos[1]), (start_pos[0], end_pos[1])
                        pygame.draw.polygon(canvas, color, [p1, p2, p3], brush_size)
                    
                    elif mode == "equilateral_triangle":
                        dx = end_pos[0] - start_pos[0]
                        dy = end_pos[1] - start_pos[1]
                        side = (dx**2 + dy**2) ** 0.5
                        p1 = (start_pos[0], start_pos[1] - int(side * math.sqrt(3) / 2))
                        p2 = (start_pos[0] - int(side / 2), start_pos[1])
                        p3 = (start_pos[0] + int(side / 2), start_pos[1])
                        pygame.draw.polygon(canvas, color, [p1, p2, p3], brush_size)
                    
                    elif mode == "rhombus":
                        dx = end_pos[0] - start_pos[0]
                        dy = end_pos[1] - start_pos[1]
                        p1 = (start_pos[0], start_pos[1] - abs(dy))
                        p2 = (start_pos[0] + abs(dx), start_pos[1])
                        p3 = (start_pos[0], start_pos[1] + abs(dy))
                        p4 = (start_pos[0] - abs(dx), start_pos[1])
                        pygame.draw.polygon(canvas, color, [p1, p2, p3, p4], brush_size)
                
                drawing = False
                temp_canvas = None

        # Отрисовка
        screen.fill((255, 255, 255))
        screen.blit(canvas, (0, 0))
        
        # Превью для линий и фигур
        if drawing and temp_canvas and start_pos and mode in ["line", "rect", "circle", "square", 
                                                                "right_triangle", "equilateral_triangle", "rhombus"]:
            preview = temp_canvas.copy()
            mouse_pos = pygame.mouse.get_pos()
            
            if mode == "line":
                pygame.draw.line(preview, color, start_pos, mouse_pos, brush_size)
            elif mode == "rect":
                rect = pygame.Rect(start_pos, (mouse_pos[0]-start_pos[0], mouse_pos[1]-start_pos[1]))
                pygame.draw.rect(preview, color, rect, brush_size)
            elif mode == "circle":
                dx = mouse_pos[0] - start_pos[0]
                dy = mouse_pos[1] - start_pos[1]
                r = int((dx**2 + dy**2) ** 0.5)
                if r > 0:
                    pygame.draw.circle(preview, color, start_pos, r, brush_size)
            
            screen.blit(preview, (0, 0))
        
        # Превью текста
        if text_mode and text_pos:
            cursor_text = font.render(text_input + "|", True, color)
            screen.blit(cursor_text, text_pos)
        
        # Подсказки
        hints = [
            f"P-Pencil L-Line T-Rect C-Circle O-Square Q-RTriangle W-ETriangle Z-Rhombus | Size:{brush_size}px (1/2/3)",
            "F-Fill X-Text E-Eraser D-Clear | R-Red G-Green B-Blue K-Black | Ctrl+S-Save"
        ]
        y = 10
        for hint in hints:
            text = font.render(hint, True, (80, 80, 80))
            screen.blit(text, (10, y))
            y += 25
        
        pygame.display.flip()
        clock.tick(60)

main()