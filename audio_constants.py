import pygame
pygame.mixer.init()

CAPTURE_SOUND = pygame.mixer.Sound('audio\capture.wav')
INVALID_SOUND = pygame.mixer.Sound('audio\pop.wav')
MOVE_SOUND = pygame.mixer.Sound('audio\move.wav')
POP_SOUND = pygame.mixer.Sound('audio\pop.wav')
SELECT_SOUND = pygame.mixer.Sound('audio\select.wav')
SWEEP_SOUND = pygame.mixer.Sound('audio\sweep.wav')
TRANSITION_IN_SOUND = pygame.mixer.Sound('audio\\transition_in.wav')
TRANSITION_OUT_SOUND = pygame.mixer.Sound('audio\\transition_out.wav')
SWIPE_SOUND = pygame.mixer.Sound('audio\\swipe.wav')
THEME_SELECTED_SOUND = pygame.mixer.Sound('audio\\theme_selected.wav')
#VICTORY_SOUND = pygame.mixer.Sound('audio\\ROUTE_209.wav')