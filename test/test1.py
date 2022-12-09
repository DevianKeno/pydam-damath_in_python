import pygame, sys

pygame.init()

reso = pygame.display.Info() # gets the video display information object

screen = pygame.display.set_mode((reso.current_w/2, reso.current_h/2))
pygame.display.set_caption('Damath') # window caption

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill('grey')

    pygame.display.update()