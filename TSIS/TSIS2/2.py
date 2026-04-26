import pygame
import math
from datetime import datetime
from collections import deque

def flood_fill(surface, x, y, new_color):
    target = surface.get_at((x, y))
    if target == new_color:
        return

    w, h = surface.get_size()
    stack = [(x, y)]

    while stack:
        px, py = stack.pop()

        if px < 0 or px >= w or py < 0 or py >= h:
            continue
        if surface.get_at((px, py)) != target:
            continue

        surface.set_at((px, py), new_color)

        stack.append((px+1, py))
        stack.append((px-1, py))
        stack.append((px, py+1))
        stack.append((px, py-1))


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    canvas = pygame.Surface(screen.get_size())
    canvas.fill((255, 255, 255))

    radius = 5   # толщина по умолчанию
    mode = "brush"
    color = (0, 0, 255)

    drawing = False
    start_pos = None
    last_pos = None

    # Текст
    typing = False
    text_input = ""
    text_pos = None
    font = pygame.font.Font(None, 24)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # -------- КЛАВИАТУРА --------
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return

                # Размер кисти
                if event.key == pygame.K_1:
                    radius = 2
                elif event.key == pygame.K_2:
                    radius = 5
                elif event.key == pygame.K_3:
                    radius = 10

                # Инструменты
                elif event.key == pygame.K_l:
                    mode = "line"
                elif event.key == pygame.K_f:
                    mode = "fill"
                elif event.key == pygame.K_x:
                    mode = "text"

                # Сохранение Ctrl+S
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    name = datetime.now().strftime("image_%Y%m%d_%H%M%S.png")
                    pygame.image.save(canvas, name)
                    print("Saved:", name)

                # Ввод текста
                if typing:
                    if event.key == pygame.K_RETURN:
                        txt = font.render(text_input, True, color)
                        canvas.blit(txt, text_pos)
                        typing = False
                        text_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    else:
                        text_input += event.unicode

            # -------- МЫШЬ НАЖАТА --------
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos

                    if mode == "fill":
                        flood_fill(canvas, event.pos[0], event.pos[1], color)

                    if mode == "text":
                        typing = True
                        text_pos = event.pos
                        text_input = ""

            # -------- МЫШЬ ОТПУЩЕНА --------
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    end_pos = event.pos

                    if mode == "line":
                        pygame.draw.line(canvas, color, start_pos, end_pos, radius)

                    elif mode == "rect":
                        rect = pygame.Rect(start_pos,
                                           (end_pos[0]-start_pos[0],
                                            end_pos[1]-start_pos[1]))
                        pygame.draw.rect(canvas, color, rect, radius)

                    elif mode == "circle":
                        dx = end_pos[0] - start_pos[0]
                        dy = end_pos[1] - start_pos[1]
                        r = int((dx**2 + dy**2) ** 0.5)
                        pygame.draw.circle(canvas, color, start_pos, r, radius)

            # -------- ДВИЖЕНИЕ МЫШИ --------
            if event.type == pygame.MOUSEMOTION:
                if drawing and (mode == "brush" or mode == "eraser"):
                    draw_color = (255, 255, 255) if mode == "eraser" else color
                    pygame.draw.line(canvas, draw_color, last_pos, event.pos, radius)
                    last_pos = event.pos

        # -------- ПРЕДПРОСМОТР ЛИНИИ --------
        screen.fill((255, 255, 255))
        screen.blit(canvas, (0, 0))

        if drawing and mode == "line":
            pygame.draw.line(screen, color, start_pos,
                             pygame.mouse.get_pos(), radius)

        # Предпросмотр текста
        if typing:
            preview = font.render(text_input, True, color)
            screen.blit(preview, text_pos)

        pygame.display.flip()
        clock.tick(60)

main()