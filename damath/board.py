import pygame
from .piece import Piece
from .constants import WHITE, BROWN, RED, ROWS, COLS, SQUARE_SIZE, LIGHT_BLUE, BLACK, BOARD
import operator

class Board:
    def __init__(self):
        self.board = [] #array representation of the board
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()

    def draw_squares(self, surface):
        surface.fill(BLACK)
        SYMBOLS = ["x", "÷", "-", "+"]
        symbol_counter = 0
        global symbol_map
        symbol_map = {}
        for row in range(ROWS):

            """for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(surface, BROWN, (row*SQUARE_SIZE, col*SQUARE_SIZE, 
                                 SQUARE_SIZE, SQUARE_SIZE))"""
            
            surface.blit(BOARD, (0, 2))

        for row in range(ROWS):
            for col in range((row+1) % 2, ROWS, 2):
                font = pygame.font.Font(None, 48) 
                text_surface = font.render(SYMBOLS[symbol_counter], True, WHITE) #FFFFFF
                text_rect = text_surface.get_rect(center=(col*SQUARE_SIZE+(SQUARE_SIZE//2), row * SQUARE_SIZE+(SQUARE_SIZE//2)+2))
                surface.blit(text_surface, text_rect)
                symbol_map.update({(row, col):SYMBOLS[symbol_counter]})
                if symbol_counter < 3:
                    symbol_counter+=1
                else:
                    symbol_counter = 0
            if symbol_counter < 3:
                symbol_counter+=1
            else:
                symbol_counter = 0

    def move(self, piece, row, col, number):
        
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == LIGHT_BLUE:
                self.white_kings += 1
            else:
                self.red_kings += 1
    
    def piece_landed(self, row, col):
        return symbol_map[(row, col)]

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        
        num_counter = 0
        num = [2, -5, 8, -11,
               -7, 10, -3, 0,
               4, -1, 6, -9]

        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row+1) % 2):
                    if row < 3:                  
                        self.board[row].append(Piece(row, col, LIGHT_BLUE, num[num_counter]))
                        if num_counter < 11:
                            num_counter+=1
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED, num[num_counter]))
                        num_counter-=1
                    else:
                        self.board[row].append(Piece(row, col, 0, 0))

                else:
                    self.board[row].append(Piece(row, col, 0, 0))

    def draw(self, surface):
        self.draw_squares(surface)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]

                if piece.color != 0:
                    piece.draw(surface, piece.number, piece.color)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = Piece(piece.row, piece.col, 0, 0)
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1 
                else:
                    self.white_left -= 1

    def winner(self):
        if self.red_left <= 0:
            return "BLUE WINS!"
        elif self.white_left <= 0:
            return "RED WINS"

        return None 

    def get_valid_moves(self, piece):
        moves = {}
        left  = piece.col - 1
        right = piece.col + 1
        row  = piece.row
        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row-1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row-1, max(row-3, -1), -1, piece.color, right))
        if piece.color == LIGHT_BLUE or piece.king:
            moves.update(self._traverse_left(row+1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row+1, min(row+3, ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current.color == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
            
                    moves.update(self._traverse_left(r+step, row, step, color, left-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1, skipped=last))
                break

            elif current.color ==  color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current.color == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
            
                    moves.update(self._traverse_left(r+step, row, step, color, right-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1, skipped=last))
                break

            elif current.color ==  color:
                break
            else:
                last = [current]

            right += 1
        
        return moves