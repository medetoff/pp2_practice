import pygame
from pygame.locals import *

class UI:
    def __init__(self, screen, font, big_font):
        self.screen = screen
        self.font = font
        self.big_font = big_font

    def button(self, text, y, color=(255,255,255)):
        surf = self.font.render(text, True, color)
        rect = surf.get_rect(center=(350, y))
        pygame.draw.rect(self.screen, (40, 40, 60), rect.inflate(60, 20), border_radius=12)
        pygame.draw.rect(self.screen, (255,255,255), rect.inflate(60, 20), 2, border_radius=12)
        self.screen.blit(surf, rect)
        return rect

    def main_menu(self):
        self.screen.blit(self.big_font.render("RACER", True, (255, 215, 0)), (245, 140))
        return {
            "play": self.button("PLAY", 280),
            "leaderboard": self.button("LEADERBOARD", 350),
            "settings": self.button("SETTINGS", 420),
            "quit": self.button("QUIT", 490)
        }

    def game_over(self, score, distance, coins):
        self.screen.blit(self.big_font.render("GAME OVER", True, (200, 0, 0)), (190, 140))
        self.screen.blit(self.font.render(f"Score: {score}", True, (255,255,255)), (240, 260))
        self.screen.blit(self.font.render(f"Distance: {int(distance)} m", True, (255,255,255)), (240, 300))
        self.screen.blit(self.font.render(f"Coins: {coins}", True, (255,255,255)), (240, 340))
        return {
            "retry": self.button("RETRY", 430),
            "menu": self.button("MAIN MENU", 490)
        }

    def name_input(self, name):
        self.screen.blit(self.font.render("Enter your name:", True, (255,255,255)), (200, 280))
        pygame.draw.rect(self.screen, (255,255,255), (180, 340, 340, 60), 3)
        self.screen.blit(self.font.render(name + "_", True, (255, 255, 100)), (200, 355))