import pygame
import math

# Заливка (Flood Fill)
def flood_fill(surface, pos, target_color, fill_color):
    """Заливает область одного цвета другим цветом"""
    if target_color == fill_color:
        return
    
    width, height = surface.get_size()
    stack = [pos]
    visited = set()
    
    while stack:
        x, y = stack.pop()
        
        # Проверки границ
        if (x, y) in visited or x < 0 or x >= width or y < 0 or y >= height:
            continue
        
        # Проверяем цвет пикселя
        if surface.get_at((x, y))[:3] != target_color:
            continue
        
        # Закрашиваем и добавляем соседей
        surface.set_at((x, y), fill_color)
        visited.add((x, y))
        stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])

# Прямая линия
def draw_line(surface, color, start, end, width):
    """Рисует прямую линию"""
    pygame.draw.line(surface, color, start, end, width)

# Прямоугольник
def draw_rectangle(surface, color, start, end, width):
    """Рисует прямоугольник"""
    rect = pygame.Rect(start, (end[0] - start[0], end[1] - start[1]))
    pygame.draw.rect(surface, color, rect, width)

# Круг
def draw_circle(surface, color, start, end, width):
    """Рисует круг по двум точкам"""
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    radius = int(math.sqrt(dx**2 + dy**2))
    if radius > 0:
        pygame.draw.circle(surface, color, start, radius, width)

# Квадрат
def draw_square(surface, color, start, end, width):
    """Рисует квадрат"""
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    side = int(math.sqrt(dx**2 + dy**2))
    rect = pygame.Rect(start[0], start[1], side, side)
    pygame.draw.rect(surface, color, rect, width)

# Прямоугольный треугольник
def draw_right_triangle(surface, color, start, end, width):
    """Рисует прямоугольный треугольник"""
    p1 = start
    p2 = (end[0], start[1])
    p3 = (start[0], end[1])
    pygame.draw.polygon(surface, color, [p1, p2, p3], width)

# Равносторонний треугольник
def draw_equilateral_triangle(surface, color, start, end, width):
    """Рисует равносторонний треугольник"""
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    side = math.sqrt(dx**2 + dy**2)
    height = int(side * math.sqrt(3) / 2)
    
    p1 = (start[0], start[1] - height)
    p2 = (start[0] - int(side / 2), start[1])
    p3 = (start[0] + int(side / 2), start[1])
    pygame.draw.polygon(surface, color, [p1, p2, p3], width)

# Ромб
def draw_rhombus(surface, color, start, end, width):
    """Рисует ромб"""
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    
    p1 = (start[0], start[1] - abs(dy))
    p2 = (start[0] + abs(dx), start[1])
    p3 = (start[0], start[1] + abs(dy))
    p4 = (start[0] - abs(dx), start[1])
    pygame.draw.polygon(surface, color, [p1, p2, p3, p4], width)

# Карандаш (свободное рисование)
def draw_pencil(surface, color, last_pos, current_pos, width):
    """Рисует линию между двумя точками (для свободного рисования)"""
    if last_pos:
        pygame.draw.line(surface, color, last_pos, current_pos, width)

# Ластик
def draw_eraser(surface, last_pos, current_pos, width):
    """Стирает (рисует белым)"""
    if last_pos:
        pygame.draw.line(surface, (255, 255, 255), last_pos, current_pos, width * 2)

# Рендер текста
def render_text(surface, font, text, position, color):
    """Выводит текст на холст"""
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

# Сохранение холста
def save_canvas(surface, filename):
    """Сохраняет surface в PNG файл"""
    pygame.image.save(surface, filename)
    print(f"✓ Файл сохранен: {filename}")