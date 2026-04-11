import pygame
from player import play,stop,next_track,previous_track,current_track
pygame.init()
screen=pygame.display.set_mode((500, 200))
font=pygame.font.Font(None, 36)
r=True
while r:
    screen.fill((30, 30, 30))
    text=font.render(f"Current: {current_track()}", True, (255, 255, 255))
    screen.blit(text, (20, 80))
    pygame.display.flip()
    for i in pygame.event.get():
        if i.type==pygame.QUIT:
            r=False
        elif i.type==pygame.KEYDOWN:
            if i.key== pygame.K_p:
                play()
            elif i.key==pygame.K_s:
                stop()
            elif i.key==pygame.K_n:
                next_track()
            elif i.key==pygame.K_b:
                previous_track()
            elif i.key==pygame.K_q:
                r=False
pygame.quit()