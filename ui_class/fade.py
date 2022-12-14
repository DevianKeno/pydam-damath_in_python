import pygame
from display_constants import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR
# --------- Fade function ---------
def fade(screen,width, height, delay=6): 
    fade = pygame.Surface((width, height))
    fade.fill('#CEB89E')
    pygame.mixer.music.load("audio/sweep.wav")
    pygame.mixer.music.play()
    for alpha in range(0, 80):
        fade.set_alpha(alpha)
        redrawWindow(screen)
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(delay)

def fade_whole_screen(screen, delay=6):
    fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade.fill('#CEB89E')
    pygame.mixer.music.load("audio/sweep.wav")
    pygame.mixer.music.play()
    for alpha in range(0, 80):
        fade.set_alpha(alpha)
        redrawWindow(screen)
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(delay)

# --------- Screen Reset function ---------
def redrawWindow(screen):
    screen.fill(BG_COLOR)