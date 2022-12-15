import pygame
from .board import Board
from .constants import RED, LIGHT_BLUE, YELLOW, WHITE, SQUARE_SIZE, OFFSET, BOARD_OFFSET, BOARD_WIDTH, BOARD_HEIGHT
from audio_constants import *

pygame.mixer.init()

class Game:

    def __init__(self, surface, scoreboard, theme):
        self.theme = theme
        self._init()
        self.surface = surface
        self.scoreboard = scoreboard

    def update(self):
        
        self.board.draw(self.surface)
        self.scoreboard.update(self.turn)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update() 

    def _init(self):
        self.moved_piece = None
        self.selected = None
        self.board = Board(self.theme)
        self.turn = RED
        self.valid_moves = {}

    def winner(self):   
        if self.board.red_left <=0 or self.board.white_left <= 0:
            red_score, blue_score = self.scoreboard.score()
            if red_score > blue_score:
                return "Red Wins"
            elif blue_score > red_score:
                return "Blue Wins"
            else:
                return "Tie"
        
        return None

    def reset(self):
        self.scoreboard.reset()
        self._init()

    def select(self, row, col):

        if self.selected:
            result = self._move(row, col)
            if not result:
                #INVALID_SOUND.play()
                self.selected = None
                self.select(row, col)

        if self.moved_piece == None:
            piece = self.board.get_piece(row, col)
        else:
            piece = self.moved_piece

        if piece.color != 0 and piece.color == self.turn:

            """if self.moved_piece == None:
                SELECT_SOUND.play()"""

            self.selected = piece
            SELECT_SOUND.play()
            self.valid_moves = self.board.get_valid_moves(piece)

            if not self.valid_moves:
                if not self.board.piece_had_skipped(self.selected, row, col):
                    return False
                self.board.piece_skipped(self.selected, row, col, False)
                self.change_turn()
            return True

        elif self.moved_piece == None and not self.selected and (piece.color == 0 or piece.color != self.turn):
            INVALID_SOUND.play()

        return False

    def _move(self, row, col):

        piece = self.board.get_piece(row, col) #(color):number

        if self.selected and piece.color == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col, piece.number)
            self.moved_piece = self.board.get_piece(row, col)
            skipped_list = list(self.valid_moves)
            skipped = self.valid_moves[(row, col)]        
            if skipped:
                CAPTURE_SOUND.play()
                self.board.piece_skipped(self.selected, row, col, True)
                operations = []
                if len(skipped) > 1:
                    for i in range(len(skipped_list)-1, (len(skipped_list)-1)-len(skipped), -1):
                        operations.append(self.board.piece_landed(skipped_list[i][0], skipped_list[i][1]))
                else:
                    operations.append(self.board.piece_landed(row, col))
                self.scoreboard.score_update(self.selected.color, self.selected, skipped, operations)
                self.board.remove(skipped)
            else:
                MOVE_SOUND.play()

            print("check: ", self.board.piece_had_skipped(self.selected, row, col))

            if not self.board.piece_had_skipped(self.selected, row, col):
                print("piece set to false")
                self.board.piece_skipped(self.selected, row, col)
                self.change_turn()
        else:
            return False
        return True
    
    def draw_valid_moves(self, moves):

        if self.selected:
            if self.selected.color == RED:
                circle_color = RED
            else:
                circle_color = LIGHT_BLUE

            for move in moves:
                row, col = move
                """alpha_circle = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                self.surface.blit(alpha_circle, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                alpha_circle.set_alpha(50)
                alpha_circle.fill(WHITE)
                pygame.draw.circle(alpha_circle, YELLOW, (5, 5), 16)"""
                pygame.draw.circle(self.surface, circle_color, (col * SQUARE_SIZE + SQUARE_SIZE//2+OFFSET, row * SQUARE_SIZE + SQUARE_SIZE//2+OFFSET), 16)
                #pygame.draw.rect(self.surface, YELLOW, (col * SQUARE_SIZE, row *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        else:
            pass

    def change_turn(self):
        self.moved_piece = None
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = LIGHT_BLUE
        else:
            self.turn = RED
