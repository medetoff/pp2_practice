import pygame  # библиотека для игры
import random  # для случайных позиций
from pygame.locals import *  # чтобы писать K_LEFT, K_RIGHT и т.д. без pygame.

class Player(pygame.sprite.Sprite):  # класс машины игрока
    def __init__(self, settings):
        super().__init__()  # инициализация родительского класса Sprite
        self.original = pygame.transform.smoothscale(pygame.image.load("assets/images/car.png"), (110, 140))  # загружаем картинку машины и меняем размер
        self.image = self.original.copy()  # рабочая копия изображения
        self.rect = self.image.get_rect(center=(350, 580))  # позиция машины по центру снизу
        self.settings = settings  # сохраняем настройки
        self.apply_color()  # сразу применяем цвет машины из настроек

    def apply_color(self):
        color = self.settings["car_color"]  # берём выбранный цвет из настроек
        if color == "red":
            self.image = self.original.copy()  # сначала сбрасываем картинку к оригиналу
            self.image.fill((255, 60, 60), special_flags=pygame.BLEND_MULT)  # накладываем красный оттенок
        elif color == "blue":
            self.image = self.original.copy()  # снова берём оригинал
            self.image.fill((60, 120, 255), special_flags=pygame.BLEND_MULT)  # накладываем синий оттенок

    def update(self):
        keys = pygame.key.get_pressed()  # получаем все нажатые клавиши
        if keys[K_LEFT] and self.rect.left > 0:   self.rect.x -= 8  # если нажата стрелка влево и не упёрлись в край — едем влево
        if keys[K_RIGHT] and self.rect.right < 700: self.rect.x += 8  # если нажата стрелка вправо и не вышли за границу — едем вправо


class Enemy(pygame.sprite.Sprite):  # класс вражеской машины
    def __init__(self):
        super().__init__()  # инициализация Sprite
        self.image = pygame.transform.smoothscale(pygame.image.load("assets/images/enemy.png"), (110, 140))  # загружаем и уменьшаем/увеличиваем картинку врага
        self.rect = self.image.get_rect()  # создаём прямоугольник для позиции и столкновений
        self.reset()  # сразу ставим врага в случайное место сверху

    def reset(self):
        self.rect.x = random.randint(50, 540)  # случайная позиция по X в пределах дороги
        self.rect.y = random.randint(-700, -150)  # случайная позиция сверху за экраном

    def move(self, speed):
        self.rect.y += speed  # двигаем врага вниз
        if self.rect.top > 700:  # если враг полностью ушёл вниз за экран
            self.reset()  # отправляем его снова наверх


class Obstacle(pygame.sprite.Sprite):  # класс препятствия на дороге
    def __init__(self):
        super().__init__()  # инициализация Sprite
        self.image = pygame.Surface((100, 35))  # создаём простую прямоугольную поверхность
        self.image.fill((90, 90, 90))  # заливаем серым цветом
        pygame.draw.rect(self.image, (40, 40, 40), self.image.get_rect(), 6)  # рисуем тёмную рамку, чтобы выглядело объёмнее
        self.rect = self.image.get_rect()  # прямоугольник объекта
        self.reset()  # ставим в случайное место

    def reset(self):
        self.rect.x = random.randint(40, 560)  # случайная позиция по X
        self.rect.y = random.randint(-900, -300)  # случайная позиция сверху, вне экрана

    def move(self, speed):
        self.rect.y += speed  # препятствие едет вниз
        if self.rect.top > 700:  # если ушло за нижнюю границу
            self.reset()  # создаём заново сверху


class PowerUp(pygame.sprite.Sprite):  # класс бонуса
    def __init__(self):
        super().__init__()  # инициализация Sprite
        self.types = {'nitro': (255, 215, 0), 'shield': (0, 255, 255), 'repair': (0, 255, 120)}  # типы бонусов и их цвета
        self.type = random.choice(list(self.types.keys()))  # случайно выбираем тип бонуса
        self.image = pygame.Surface((55, 55), pygame.SRCALPHA)  # создаём прозрачную поверхность
        pygame.draw.circle(self.image, self.types[self.type], (27, 27), 27)  # рисуем круг нужного цвета
        font = pygame.font.SysFont("Verdana", 28, bold=True)  # шрифт для буквы внутри бонуса
        self.image.blit(font.render(self.type[0].upper(), True, (0,0,0)), (18, 13))  # рисуем первую букву типа: N, S или R
        self.rect = self.image.get_rect()  # прямоугольник бонуса
        self.reset()  # ставим в случайное место сверху

    def reset(self):
        self.rect.x = random.randint(60, 520)  # случайная позиция по X
        self.rect.y = random.randint(-1200, -400)  # случайная позиция далеко сверху

    def move(self, speed):
        self.rect.y += speed  # двигаем бонус вниз
        if self.rect.top > 700:  # если бонус ушёл за экран
            self.reset()  # возвращаем его наверх