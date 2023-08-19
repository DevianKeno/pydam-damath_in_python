import pygame
pygame.mixer.init()

# sound volume
SOUND_VOLUME = 1.0
MUSIC_VOLUME = 1.0

CAPTURE_SOUND = pygame.mixer.Sound('audio\capture.wav')
INVALID_SOUND = pygame.mixer.Sound('audio\invalid.mp3')
MOVE_SOUND = pygame.mixer.Sound('audio\move.wav')
POP_SOUND = pygame.mixer.Sound('audio\pop.wav')
SELECT_SOUND = pygame.mixer.Sound('audio\select.wav')
SWEEP_SOUND = pygame.mixer.Sound('audio\sweep.wav')
TRANSITION_IN_SOUND = pygame.mixer.Sound('audio\\transition_in.wav')
TRANSITION_OUT_SOUND = pygame.mixer.Sound('audio\\transition_out.wav')
SWIPE_SOUND = pygame.mixer.Sound('audio\\swipe.wav')
THEME_SELECTED_SOUND = pygame.mixer.Sound('audio\\theme_selected.wav')
#VICTORY_SOUND = pygame.mixer.Sound('audio\\ROUTE_209.wav')

SOUNDS = [POP_SOUND, MOVE_SOUND, 
          SWEEP_SOUND, SELECT_SOUND, 
          CAPTURE_SOUND, INVALID_SOUND,
          TRANSITION_IN_SOUND, 
          TRANSITION_OUT_SOUND]