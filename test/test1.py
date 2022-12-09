import pygame, sys

pygame.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Damath')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill('grey')

    pygame.display.update()