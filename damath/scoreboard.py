"""
Scoreboard class.
"""

import pygame
import operator
from math import sqrt, ceil
from .constants import *
from ui_class.colors import DARK_GRAY_BLUE
from ui_class.fade import fade
from objects import scoreboard_p1_score_area, scoreboard_p2_score_area, scoreboard_p1_chip, scoreboard_p2_chip
from .timer import *
from options import *

class Scoreboard:

    mode = MODE

    def __init__(self, surface):
        self.surface = surface
        # self.width = SCOREBOARD_WIDTH   
        # self.height = SCOREBOARD_HEIGHT
        self.p1_score = 0 # Blue
        self.p2_score = 0 # Orange
        self.font = pygame.font.Font('font\CookieRun_Bold.ttf', int(scoreboard_p1_score_area.w*0.24))
        self.font_mini = pygame.font.Font('font\CookieRun_Bold.ttf', int(scoreboard_p1_score_area.w*0.17))

    def draw_scores(self):
        """
        Displays the scores.
        """
        scoreboard_p1_score_area.display()
        p1_score, p2_score = str(round(self.p1_score, 1)), str(round(self.p2_score, 1))

        if len(p1_score) > 5:
            self.text_p1_score = self.font_mini.render(str(round(self.p1_score, 1)), True, DARK_GRAY_BLUE)
        else:
            self.text_p1_score = self.font.render(str(round(self.p1_score, 1)), True, DARK_GRAY_BLUE)
        
        self.p1_score_pos = (scoreboard_p1_score_area.x + scoreboard_p1_score_area.w//2,
                             scoreboard_p1_score_area.y + scoreboard_p1_score_area.h//2)
        self.p1_score_rect = self.text_p1_score.get_rect(center=self.p1_score_pos)
        self.surface.blit(self.text_p1_score, self.p1_score_rect)

        scoreboard_p2_score_area.display()
        if len(p2_score) > 5:
            self.text_p2_score = self.font_mini.render(str(round(self.p2_score, 1)), True, DARK_GRAY_BLUE)
        else:
            self.text_p2_score = self.font.render(str(round(self.p2_score, 1)), True, DARK_GRAY_BLUE)
        
        self.p2_score_pos = (scoreboard_p2_score_area.x + scoreboard_p2_score_area.w//2,
                             scoreboard_p2_score_area.y + scoreboard_p2_score_area.h//2)
        self.p2_score_rect = self.text_p2_score.get_rect(center=self.p2_score_pos)
        self.surface.blit(self.text_p2_score, self.p2_score_rect)

    def draw_turn_indicator(self, turn):
        """
        Displays the turn indicator chips.
        """
        remtime = ceil(turn_timer.get_remaining_time())
        timerfont = pygame.font.Font('font\CookieRun_Bold.ttf', int(scoreboard_p1_chip.w//2.5))
        
        if turn == PLAYER_ONE:
            scoreboard_p1_chip.display()
            scoreboard_p2_chip.display(100)
            if TIMER:
                if remtime > 10: timer_text = timerfont.render(str(remtime), True, (DARK_GRAY_BLUE))
                else: timer_text = timerfont.render(str(remtime), True, (RED))
                self.surface.blit(timer_text,(scoreboard_p1_chip.x+(scoreboard_p1_chip.w//2-timer_text.get_width()//2), scoreboard_p1_chip.y+(scoreboard_p1_chip.h//2.35-timer_text.get_height()//2)))
        else:
            scoreboard_p2_chip.display()
            scoreboard_p1_chip.display(100)
            if TIMER:
                if remtime > 10: timer_text = timerfont.render(str(remtime), True, (PERSIMMON_ORANGE))
                else: timer_text = timerfont.render(str(remtime), True, (RED))
                self.surface.blit(timer_text,(scoreboard_p2_chip.x+(scoreboard_p2_chip.w//2-timer_text.get_width()//2), scoreboard_p2_chip.y+(scoreboard_p2_chip.h//2.35-timer_text.get_height()//2)))

    def score_update(self, color, piece, numbers, operations):
        result = 0
        OPERATOR_MAP = {'+' : operator.add,
                        '-' : operator.sub,
                        'x' : operator.mul,
                        '÷' : operator.truediv}

        piece_num = piece.number
        nums = list(num.number for num in numbers)

        if self.mode == 'Rationals':
            
            rationals_dict = {
                '10/10': 10/10, '7/10': 7/10, '2/10': 2/10,
                '5/10': 5/10, '1/10': 1/10, '4/10': 4/10,
                '11/10': 11/10, '8/10': 8/10, '12/10': 12/10,
                '9/10': 9/10, '6/10': 6/10, '3/10': 3/10
            } 

            nums = list(rationals_dict.get(i) for i in nums)
            piece_num = rationals_dict.get(piece.number)

        elif self.mode == 'Radicals':

            radicals_dict = {
                    '9√2': 9*sqrt(2), '-√8':sqrt(8), '4√18':4*sqrt(18), 
                    '16√32':16*sqrt(32), '-49√8':-49*sqrt(8), '-25√18':-25*sqrt(18), 
                    '36√32':36*sqrt(32), '64√2':64*sqrt(2), '-121√18':-121*sqrt(18), 
                    '-81√32':-81*sqrt(32), '100√2':100*sqrt(2), '144√8':144*sqrt(8)
            }

            nums = list(radicals_dict.get(i) for i in nums)
            piece_num = radicals_dict.get(piece.number)

        elif self.mode == 'Polynomials':
            #TODO: needs fixing of the assignment of values for row and col
            pass

        for num, operation in zip(nums, operations):

            op = OPERATOR_MAP.get(operation)
            if operation == '÷' and float(num) == 0:
                continue
            else:
                result += op(float(piece_num), float(num))
                if piece.IsKing:
                    if piece.IsOnPromotion:
                        piece.done_promote()
                    else:
                        result *= 2.
                
            print("+", result)

        if color == PLAYER_ONE:
            self.p1_score += result
            round(self.p1_score, 1)
        else:
            self.p2_score += result
            round(self.p2_score, 1)

        print(f'[Score]: {PLAYER_ONE}: {self.p1_score}\n' \
              f'[Score]: {PLAYER_TWO}: {self.p2_score}')       

    def score(self):
        return self.p1_score, self.p2_score

    def reset(self):
        self.p1_score = 0 # Blue
        self.p2_score = 0 # Orange