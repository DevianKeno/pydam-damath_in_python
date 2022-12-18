import pygame
from .piece import Piece
from .constants import WHITE, BROWN, RED, ROWS, COLS, SQUARE_SIZE, LIGHT_BLUE, BLACK, BOARD_BLACK
from audio_constants import *

pygame.mixer.init()

class Board:
    
    def __init__(self, theme):
        self.board = [] #array representation of the board
        self.IsMovable = {}
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()
        self.theme = theme

    def update_theme(self, theme):
        self.theme = theme

    def draw_squares(self, surface):
        surface.fill(BLACK)
        SYMBOLS_ONE = ["x", "-", "x", "-"]
        SYMBOLS_TWO = ["÷", "+", "÷", "+"]
        symbol_counter = 0
        symbol_counter_reversed = 3
        global symbol_map
        symbol_map = {}

        # for row in range(ROWS):

        #     """for col in range(row % 2, ROWS, 2):
        #         pygame.draw.rect(surface, BROWN, (row*SQUARE_SIZE, col*SQUARE_SIZE, 
        #                          SQUARE_SIZE, SQUARE_SIZE))"""
            
        surface.blit(self.theme, (1, -1))

        for col in range(COLS):
            symbol_counter = 0
            symbol_counter_reversed = 3

            for row in range(0, ROWS, 2):
                if (col % 2 == 2):
                    row+1
                match col:
                    case 0:
                        symbol_map.update({(row, col):SYMBOLS_ONE[symbol_counter]})
                        symbol_counter += 1
                    case 1:
                        symbol_map.update({(row+1, col):SYMBOLS_TWO[symbol_counter]})
                        symbol_counter += 1
                    case 2:
                        symbol_map.update({(row, col):SYMBOLS_TWO[symbol_counter]})
                        symbol_counter += 1
                    case 3:
                        symbol_map.update({(row+1, col):SYMBOLS_ONE[symbol_counter]})
                        symbol_counter += 1
                    case 4:
                        symbol_map.update({(row, col):SYMBOLS_ONE[symbol_counter_reversed]})
                        symbol_counter_reversed -= 1
                    case 5:
                        symbol_map.update({(row+1, col):SYMBOLS_TWO[symbol_counter_reversed]})
                        symbol_counter_reversed -= 1
                    case 6:
                        symbol_map.update({(row, col):SYMBOLS_TWO[symbol_counter_reversed]})
                        symbol_counter_reversed -= 1
                    case 7:
                        symbol_map.update({(row+1, col):SYMBOLS_ONE[symbol_counter_reversed]})
                        symbol_counter_reversed -= 1

    def move(self, piece, row, col, number):
        print(f"Piece {piece.color} moved: {piece.col}, {piece.row} -> {col}, {row}")

        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        self.IsMovable[(row), (col)] = self.IsMovable[(piece.row), (piece.col)]
        del self.IsMovable[(piece.row), (piece.col)]

        piece.move(row, col)

        if row == ROWS - 1:
            if piece.color == LIGHT_BLUE:
                piece.make_king()
                CAPTURE_SOUND.play()
                self.white_kings += 1
        elif row == 0:
            if piece.color == RED:
                piece.make_king()
                CAPTURE_SOUND.play()
                self.red_kings += 1
    
    def piece_skipped(self, piece, row, col, bool=False):
        piece.HasSkipped = bool

    def piece_had_skipped(self, piece, row, col):
        return piece.HasSkipped
        
    def has_possible_capture(self, piece):
        return piece.HasPossibleCapture
    
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
                if col % 2 == ((row) % 2):
                    if row < 3:                  
                        self.board[row].append(Piece(row, col, LIGHT_BLUE, num[num_counter]))
                        self.IsMovable[(row, col)] = True
                        if num_counter < 11:
                            num_counter+=1
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED, num[num_counter]))
                        self.IsMovable[(row, col)] = True
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

    def get_valid_moves(self, piece):
        moves = {}
        up = -1
        down = 1
        above = piece.row-1
        below = piece.row+1

        if piece.color == RED:
            # Up    
            moves.update(self._check_left(piece, starting_row=above, direction=up, max_distance=-1))
            moves.update(self._check_right(piece, starting_row=above, direction=up, max_distance=-1))
            # Down (Capture only)
            moves.update(self._check_left(piece, starting_row=below, direction=down, max_distance=ROWS))
            moves.update(self._check_right(piece, starting_row=below, direction=down, max_distance=ROWS))
        else: # piece.color == LIGHT_BLUE:
            # Up (Capture only)
            moves.update(self._check_left(piece, starting_row=above, direction=up, max_distance=-1))
            moves.update(self._check_right(piece, starting_row=above, direction=up, max_distance=-1))
            # Down
            moves.update(self._check_left(piece, starting_row=below, direction=down, max_distance=ROWS))
            moves.update(self._check_right(piece, starting_row=below, direction=down, max_distance=ROWS))

        return moves

    def _check_left(self, piece, starting_row, direction, max_distance, skipped=[]):
        moves = {}
        moves_capture = {}
        can_capture = []
        next_enemy_piece = 0
        left = piece.col - 1
        piece.can_capture(False)

        for r in range(starting_row, max_distance, direction):
            if left < 0:
                break

            current_spot = self.board[r][left]
            
            # Check if spot is empty
            if current_spot.color == 0:
                # Check if piece had captured previously
                if piece.HasSkipped:
                    # If there's nobody to capture, 
                    if not can_capture:
                        if piece.IsKing:
                            left -= 1
                            continue
                        # Normal piece can't move to an empty spot after capturing
                        else:
                            break
                    else:
                        if next_enemy_piece >= 2:
                            break
                        print("Piece can capture")
                        piece.can_capture()
                        moves[(r, left)] = can_capture

                # Check if the backward movement is for capturing
                if piece.color == RED:
                    if direction == 1: # Down
                        # Piece can capture, allow movement
                        if can_capture:
                            pass
                        # Piece is not capturing, only king pieces can move
                        else:
                            if not piece.IsKing:
                                break
                else: # if BLUE
                    if direction == -1: # Up
                        if can_capture:
                            pass
                        else:
                            if piece.IsKing:
                                break

                if skipped and not can_capture:
                    break
                elif skipped:
                    moves[(r, left)] = can_capture + skipped
                else:
                    if next_enemy_piece >= 2:
                        break
                    moves[(r, left)] = can_capture

                    if not piece.IsKing:
                        break
                    
                if can_capture:
                    print("Piece can capture")
                    piece.can_capture()
                    if piece.IsKing:
                        pass
                    else:
                        break
            
            elif current_spot.color == piece.color:
                break
            # There's enemy piece
            else:
                next_enemy_piece += 1
                can_capture = [current_spot]

            left -= 1

        return moves

    def _check_right(self, piece, starting_row, direction, max_distance, skipped=[]):
        moves = {}
        can_capture = []
        next_enemy_piece = 0
        right = piece.col + 1
        piece.can_capture(False)


        for r in range(starting_row, max_distance, direction):
            if right >= COLS:
                break

            current_spot = self.board[r][right]

            # Check if spot is empty
            if current_spot.color == 0:
                # Check if piece had captured once
                if piece.HasSkipped:
                    if not can_capture:
                        # King can see n tiles behind enemy pieces
                        if piece.IsKing:
                            right += 1
                            continue
                        else:
                            break
                    else:
                        #  Will not be able to chain capture if there's two pieces in succession
                        if next_enemy_piece >= 2:
                            break
                        print("Piece can capture")
                        piece.can_capture()
                        moves[(r, right)] = can_capture + skipped
                        
                # Checks for backward movement
                if piece.color == RED:
                    if direction == 1:
                        if can_capture:
                            pass
                        else:
                            if not piece.IsKing:
                                break
                else: # if LIGHT_BLUE
                    if direction == -1:
                        if can_capture:
                            pass
                        else:
                            if not piece.IsKing:
                                break

                if skipped and not can_capture:
                    break
                elif skipped:
                    moves[(r, right)] = can_capture + skipped
                else:
                    if next_enemy_piece >= 2:
                        break
                    moves[(r, right)] = can_capture

                    if not piece.IsKing:
                        break

                # After capturing king can move n spaces behind enemy, but not normal pieces
                if can_capture:
                    print("Piece can capture")
                    piece.can_capture()
                    if piece.IsKing:
                        pass
                    else:
                        break
            # Piece is ally
            elif current_spot.color == piece.color:
                break
            # Piece is enemy
            else:
                next_enemy_piece += 1
                can_capture = [current_spot]
                
            # Move right by 1 tile
            right += 1
        
        return moves