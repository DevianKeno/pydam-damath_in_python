import pygame
from .board import Board
from .constants import RED, LIGHT_BLUE, YELLOW, SQUARE_SIZE
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
        return self.board.winner()

    def reset(self):
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
        for move in moves:
            row, col = move
            #pygame.draw.circle(self.surface, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 8)
            pygame.draw.rect(self.surface, YELLOW, (col * SQUARE_SIZE, row *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = LIGHT_BLUE
        else:
            self.turn = RED
