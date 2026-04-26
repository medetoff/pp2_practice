import pygame
from datetime import datetime
from tools import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # окно 800x600
    clock = pygame.time.Clock()
    canvas = pygame.Surface(screen.get_size())  # отдельная поверхность для рисования
    canvas.fill((255, 255, 255))  # белый холст

    brush_size = 2  # начальный размер кисти
    mode = "pencil"  # текущий инструмент
    color = (0, 0, 255)  # начальный цвет — синий
    drawing = False  # сейчас рисуем или нет
    start_pos = None  # откуда начали тянуть фигуру
    last_pos = None  # предыдущая позиция мыши (для карандаша)
    temp_canvas = None  # временная копия холста для превью фигуры

    text_mode = False  # режим ввода текста активен или нет
    text_pos = None  # куда кликнули для текста
    text_input = ""  # то что пользователь сейчас набирает
    font = pygame.font.SysFont("Arial", 24)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                # Сохранение Ctrl+S — имя файла содержит дату и время
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"paint_{timestamp}.png"
                    save_canvas(canvas, filename)

                # Переключение инструментов по клавишам
                if event.key == pygame.K_p: mode = "pencil"
                elif event.key == pygame.K_l: mode = "line"
                elif event.key == pygame.K_t: mode = "rect"
                elif event.key == pygame.K_c: mode = "circle"
                elif event.key == pygame.K_e: mode = "eraser"
                elif event.key == pygame.K_o: mode = "square"
                elif event.key == pygame.K_q: mode = "right_triangle"
                elif event.key == pygame.K_w: mode = "equilateral_triangle"
                elif event.key == pygame.K_z: mode = "rhombus"
                elif event.key == pygame.K_f: mode = "fill"
                elif event.key == pygame.K_x: mode = "text"
                elif event.key == pygame.K_d: canvas.fill((255, 255, 255))  # D — очистить холст

                # Размер кисти: 1 — тонкая, 3 — толстая
                elif event.key == pygame.K_1: brush_size = 2
                elif event.key == pygame.K_2: brush_size = 5
                elif event.key == pygame.K_3: brush_size = 10

                # Быстрая смена цвета
                elif event.key == pygame.K_r: color = (255, 0, 0)
                elif event.key == pygame.K_g: color = (0, 200, 0)
                elif event.key == pygame.K_b: color = (0, 0, 255)
                elif event.key == pygame.K_k: color = (0, 0, 0)

                # Обработка ввода текста когда text_mode активен
                if text_mode:
                    if event.key == pygame.K_RETURN:  # Enter — рендерим текст на холст
                        if text_input:
                            render_text(canvas, font, text_input, text_pos, color)
                        text_mode = False
                        text_input = ""
                    elif event.key == pygame.K_ESCAPE:  # Escape — отменяем текст
                        text_mode = False
                        text_input = ""
                    elif event.key == pygame.K_BACKSPACE:  # стираем последний символ
                        text_input = text_input[:-1]
                    else:
                        text_input += event.unicode  # добавляем напечатанный символ

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # левая кнопка мыши
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos

                    if mode == "fill":  # заливка — берём цвет пикселя под курсором и заполняем
                        target = canvas.get_at(event.pos)[:3]
                        flood_fill(canvas, event.pos, target, color)
                        drawing = False  # рисование не нужно, заливка мгновенная

                    elif mode == "text":  # текстовый режим — запоминаем куда кликнули
                        text_mode = True
                        text_pos = event.pos
                        text_input = ""
                        drawing = False

                    # Для фигур сохраняем копию холста — чтобы показывать превью без следов
                    if mode in ["line", "rect", "circle", "square", "right_triangle",
                                "equilateral_triangle", "rhombus"]:
                        temp_canvas = canvas.copy()

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if mode == "pencil":  # карандаш рисует линию от прошлой до текущей точки
                        draw_pencil(canvas, color, last_pos, event.pos, brush_size)
                        last_pos = event.pos

                    elif mode == "eraser":  # ластик рисует белым поверх холста
                        draw_eraser(canvas, last_pos, event.pos, brush_size)
                        last_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing and start_pos and event.button == 1:
                    end_pos = event.pos

                    # Финальная отрисовка фигуры от начальной до конечной точки
                    if mode == "line":
                        draw_line(canvas, color, start_pos, end_pos, brush_size)
                    elif mode == "rect":
                        draw_rectangle(canvas, color, start_pos, end_pos, brush_size)
                    elif mode == "circle":
                        draw_circle(canvas, color, start_pos, end_pos, brush_size)
                    elif mode == "square":
                        draw_square(canvas, color, start_pos, end_pos, brush_size)
                    elif mode == "right_triangle":
                        draw_right_triangle(canvas, color, start_pos, end_pos, brush_size)
                    elif mode == "equilateral_triangle":
                        draw_equilateral_triangle(canvas, color, start_pos, end_pos, brush_size)
                    elif mode == "rhombus":
                        draw_rhombus(canvas, color, start_pos, end_pos, brush_size)

                drawing = False
                temp_canvas = None  # убираем превью

        screen.fill((255, 255, 255))
        screen.blit(canvas, (0, 0))  # рисуем холст на экран

        # Превью фигуры во время перетаскивания — рисуем на копии чтобы не пачкать холст
        if drawing and temp_canvas and start_pos:
            preview = temp_canvas.copy()
            mouse_pos = pygame.mouse.get_pos()

            if mode == "line":
                draw_line(preview, color, start_pos, mouse_pos, brush_size)
            elif mode == "rect":
                draw_rectangle(preview, color, start_pos, mouse_pos, brush_size)
            elif mode == "circle":
                draw_circle(preview, color, start_pos, mouse_pos, brush_size)

            screen.blit(preview, (0, 0))  # показываем превью поверх холста

        # Показываем что пользователь печатает — с мигающим курсором "|"
        if text_mode and text_pos:
            cursor_text = font.render(text_input + "|", True, color)
            screen.blit(cursor_text, text_pos)

        # Подсказки по инструментам — две строки внизу сверху экрана
        hints = [
            f"P-Pencil L-Line T-Rect C-Circle O-Square Q-R.Triangle W-E.Triangle Z-Rhombus | Size:{brush_size}px",
            "F-Fill X-Text E-Eraser D-Clear | R-Red G-Green B-Blue K-Black | Ctrl+S-Save"
        ]
        y = 10
        for hint in hints:
            text = font.render(hint, True, (80, 80, 80))
            screen.blit(text, (10, y))
            y += 25

        pygame.display.flip()  # обновляем экран
        clock.tick(60)  # 60 кадров в секунду

main()