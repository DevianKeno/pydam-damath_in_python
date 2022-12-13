import pygame
from .board import Board
from .constants import RED, LIGHT_BLUE, YELLOW, WHITE, SQUARE_SIZE, OFFSET
#from .scoreboard import Scoreboard

pygame.mixer.init()

class Game:

    def __init__(self, surface, scoreboard):
        self._init()
        self.surface = surface
        self.scoreboard = scoreboard

    def update(self):
        
        self.board.draw(self.surface)
        self.scoreboard.update(self.turn)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update() 

    def _init(self):
        self.selected = None
        self.board = Board()
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
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece.color != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        
        return False

    def _move(self, row, col):

        piece = self.board.get_piece(row, col) #(color):number
        if self.selected and piece.color == 0 and (row, col) in self.valid_moves:
            pygame.mixer.music.load('audio//move.wav')
            pygame.mixer.music.play()
            self.board.move(self.selected, row, col, piece.number)
            skipped_list = list(self.valid_moves)
            skipped = self.valid_moves[(row, col)]        
            
            if skipped:
                operations = []
                if len(skipped) > 1:
                    for i in range(len(skipped_list)-1, (len(skipped_list)-1)-len(skipped), -1):
                        operations.append(self.board.piece_landed(skipped_list[i][0], skipped_list[i][1]))
                else:
                    operations.append(self.board.piece_landed(row, col))
                self.scoreboard.score_update(self.selected.color, self.selected, skipped, operations)
                self.board.remove(skipped)
                
            self.change_turn()       

        else:
            return False

        return True
    
    def draw_valid_moves(self, moves):
        if self.selected:
            for move in moves:
                row, col = move
                """alpha_circle = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                self.surface.blit(alpha_circle, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                alpha_circle.set_alpha(50)
                alpha_circle.fill(WHITE)
                pygame.draw.circle(alpha_circle, YELLOW, (5, 5), 16)"""
                pygame.draw.circle(self.surface, YELLOW, (col * SQUARE_SIZE + SQUARE_SIZE//2+OFFSET, row * SQUARE_SIZE + SQUARE_SIZE//2+OFFSET), 16)
                #pygame.draw.rect(self.surface, YELLOW, (col * SQUARE_SIZE, row *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        else:
            pass

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = LIGHT_BLUE
        else:
            self.turn = RED
