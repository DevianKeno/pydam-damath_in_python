"""
Scoreboard class.
"""

import pygame, operator
from .constants import *
from ui_class.colors import DARK_GRAY_BLUE
from ui_class.fade import fade
from objects import scoreboard_p1_score_area, scoreboard_p2_score_area, scoreboard_p1_chip, scoreboard_p2_chip


class Scoreboard:

    def __init__(self, surface):
        self.surface = surface
        # self.width = SCOREBOARD_WIDTH   
        # self.height = SCOREBOARD_HEIGHT

        self.p1_score = 0 # Blue
        self.p2_score = 0 # Orange

        self.font = pygame.font.Font('font\CookieRun_Bold.ttf', int(scoreboard_p1_score_area.w*0.24))

    def draw_scores(self):
        """
        Displays the scores.
        """
        scoreboard_p1_score_area.display()
        self.text_p1_score = self.font.render(str(round(self.p1_score, 1)), True, DARK_GRAY_BLUE)
        self.p1_score_pos = (scoreboard_p1_score_area.x + scoreboard_p1_score_area.w//2,
                             scoreboard_p1_score_area.y + scoreboard_p1_score_area.h//2)
        self.p1_score_rect = self.text_p1_score.get_rect(center=self.p1_score_pos)

        self.surface.blit(self.text_p1_score, self.p1_score_rect)

        scoreboard_p2_score_area.display()
        self.text_p2_score = self.font.render(str(round(self.p2_score, 1)), True, DARK_GRAY_BLUE)
        self.p2_score_pos = (scoreboard_p2_score_area.x + scoreboard_p2_score_area.w//2,
                             scoreboard_p2_score_area.y + scoreboard_p2_score_area.h//2)
        self.p2_score_rect = self.text_p2_score.get_rect(center=self.p2_score_pos)
        self.surface.blit(self.text_p2_score, self.p2_score_rect)

    def draw_turn_indicator(self, turn):
        """
        Displays the turn indicator chips.
        """
        if turn == PLAYER_ONE:
            scoreboard_p1_chip.display()
        else:
            scoreboard_p2_chip.display()

    def score_update(self, color, piece, numbers, operations):
        result = 0
        OPERATOR_MAP = {'+' : operator.add,
                        '-' : operator.sub,
                        'x' : operator.mul,
                        '÷' : operator.truediv}
        print(numbers)
        for num, operation in zip(numbers, operations):
            op = OPERATOR_MAP.get(operation)
            if operation == '÷' and num.number == 0:
                continue
            else:
                result += op(piece.number, num.number)
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