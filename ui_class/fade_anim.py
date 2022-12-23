import pygame

class Fade:

    def __init__(self, screen, fade_surf, RGBA_color, pos, *, speed):
        self.screen = screen
        self.fade_surf = fade_surf
        self.pos = pos
        self.speed = speed

        self.r, self.g, self.b, self.a = RGBA_color
        self.a = 0
        
        self._init()

    def _init(self):
        self.next_anim = 0
        self.anim_idx = 0
        self.finished = False

        self.reversed_next_anim = 0
        self.reversed_anim_idx = 255
        self.reversed_finished = False

    def change_pos(self, pos=()):
        self.pos = pos

    def display(self):

        self.screen.blit(self.fade_surf, (self.pos))

    def play(self):

        time_now = pygame.time.get_ticks()

        if not self.finished:
            if time_now > self.next_anim:
                self.next_anim = time_now + 20
                self.fade_surf.fill((self.r, self.g, self.b, self.anim_idx))
                
            if self.anim_idx <= 255 - self.speed:
                self.anim_idx += self.speed
            else:
                self.finished = True

        self.display()

    def reverse_play(self):

        time_now = pygame.time.get_ticks()

        if not self.reversed_finished:
            if time_now > self.reversed_next_anim:
                self.reversed_next_anim = time_now + 1
                self.fade_surf.fill((self.r, self.g, self.b, self.reversed_anim_idx))

            if self.reversed_anim_idx <= self.speed:
                self.reversed_finished = True
            else:
                self.reversed_anim_idx -= self.speed

        self.display()

    def full_fade(self):
        if self.finished:
            self.reverse_play()
        else:
            self.play()

    def get_finished(self):
        return (self.finished and self.reversed_finished)

    def reset(self):
        self._init()