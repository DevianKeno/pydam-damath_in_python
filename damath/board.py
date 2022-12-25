import pygame
from .piece import Piece
from .constants import *
from assets import BOARD
from audio_constants import *
from display_constants import BG_COLOR
from ui_class.tween import *

pygame.mixer.init()

class Board:
    
    def __init__(self, surface, theme):
        self.surface = surface
        self.board = [] #array representation of the board
        self.moveables = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.red_captures = self.white_captures = []
        self.init_chips(self.surface)
        self.theme = theme
        self.anim = None

    def update_theme(self, theme):
        self.theme = theme

    def init_symbols(self, surface):
        surface.fill(WHITE)
        surface.set_colorkey(WHITE)
        SYMBOLS_ONE = ["x", "-", "x", "-"]
        SYMBOLS_TWO = ["÷", "+", "÷", "+"]
        symbol_counter = 0
        symbol_counter_reversed = 3
        global symbol_map
        symbol_map = {}
        
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

    def init_chips(self, surface):
        
        num_counter = 0
        num = [2, -5, 8, -11,
               -7, 10, -3, 0,
               4, -1, 6, -9]

        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row) % 2):
                    if row < 3:                  
                        self.board[row].append(Piece(surface, row, col, PLAYER_TWO, num[num_counter]))
                        self.moveables.append((row, col))
                        if num_counter < 11:
                            num_counter+=1
                    elif row > 4:
                        self.board[row].append(Piece(surface, row, col, PLAYER_ONE, num[num_counter]))
                        self.moveables.append((row, col))
                        num_counter-=1
                    else:
                        self.board[row].append(Piece(surface, row, col, 0, 0))
                else:
                    self.board[row].append(Piece(surface, row, col, 0, 0))

    def move(self, piece, row, col, number):
        print(f"[Piece moved]: {piece.color}: ({piece.row}, {piece.col}) -> ({row}, {col})")

        _piece = self.board[piece.row][piece.col]
        _piece_dest = self.board[row][col]
        self.anim = Move(_piece, (_piece_dest.x, _piece_dest.y), 0.5, ease_type=easeOutQuint)
        self.anim.play()

        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        _piece.x, _piece_dest.x = _piece_dest.x, _piece.x
        _piece.y, _piece_dest.y = _piece_dest.y, _piece.y

        self.moveables.append((row, col))
        del self.moveables[self.moveables.index((piece.row, piece.col))]
        
        piece.move(row, col)


        if row == ROWS - 1:
            if piece.color == PLAYER_TWO:
                piece.make_king()
                CAPTURE_SOUND.play()
                self.white_kings += 1
        elif row == 0:
            if piece.color == PLAYER_ONE:
                piece.make_king()
                CAPTURE_SOUND.play()
                self.red_kings += 1
    
    def piece_skipped(self, piece, row, col, bool):
        piece.HasSkipped = bool

    def piece_had_skipped(self, piece, row, col):
        return piece.HasSkipped
        
    def has_possible_capture(self, piece):
        return piece.HasPossibleCapture
    
    def piece_landed(self, row, col):
        return symbol_map[(row, col)]

    def get_piece(self, row, col):
        return self.board[row][col]

    def draw_contents(self, surface):
        self.init_symbols(surface)

    def draw_chips(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]

                if piece.color != 0:
                    piece.display()

    def draw_captured_chips(self, surface):
        for chip in self.red_captures:
            break
        for chip in self.white_captures:
            break 
        pass

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = Piece(self.surface, piece.row, piece.col, 0, 0)
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1 
                else:
                    self.white_left -= 1

    def get_valid_moves(self, piece, type="both"):
        moves = {}
        up = -1
        down = 1
        above = piece.row-1
        below = piece.row+1
        
        if piece.HasPossibleCapture:
            piece.can_capture(False)

        if piece.color == PLAYER_ONE:
            # Up    
            moves.update(self._check_left(piece, starting_row=above, direction=up, max_distance=-1, type=type))
            moves.update(self._check_right(piece, starting_row=above, direction=up, max_distance=-1, type=type))
            # Down (Capture only)
            moves.update(self._check_left(piece, starting_row=below, direction=down, max_distance=ROWS, type=type))
            moves.update(self._check_right(piece, starting_row=below, direction=down, max_distance=ROWS, type=type))
        else: # piece.color == LIGHT_BLUE:
            # Up (Capture only)
            moves.update(self._check_left(piece, starting_row=above, direction=up, max_distance=-1, type=type))
            moves.update(self._check_right(piece, starting_row=above, direction=up, max_distance=-1, type=type))
            # Down
            moves.update(self._check_left(piece, starting_row=below, direction=down, max_distance=ROWS, type=type))
            moves.update(self._check_right(piece, starting_row=below, direction=down, max_distance=ROWS, type=type))

        return moves

    def _check_left(self, piece, starting_row, direction, max_distance, type, skipped=[]):
        moves = {}
        moves_capture = {}
        can_capture = []
        next_enemy_piece = 0
        left = piece.col - 1

        for r in range(starting_row, max_distance, direction):
            if left < 0:
                break

            if next_enemy_piece >= 2:
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
                        piece.can_capture()
                        moves[(r, left)] = can_capture

                # Check if the backward movement is for capturing
                if piece.color == PLAYER_ONE:
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
                            if not piece.IsKing:
                                break

                # if skipped and not can_capture:
                #     break
                # el
                if skipped:
                    moves[(r, left)] = can_capture + skipped
                else:
                    if next_enemy_piece >= 2:
                        break
                    if can_capture:
                        piece.can_capture(bool=True)
                        moves_capture[(r, left)] = can_capture
                    else:
                        moves[(r, left)] = can_capture

                    if not piece.IsKing:
                        break
                    
                if can_capture:
                    piece.can_capture(bool=True)
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

        if type == "move":
            return moves
        elif type == "capture":
            return moves_capture
        elif type == "both":
            moves.update(moves_capture)
            return moves

    def _check_right(self, piece, starting_row, direction, max_distance, type, skipped=[]):
        moves = {}
        moves_capture = {}
        can_capture = []
        next_enemy_piece = 0
        right = piece.col + 1

        for r in range(starting_row, max_distance, direction):
            if right >= COLS:
                break

            if next_enemy_piece >= 2:
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
                        piece.can_capture()
                        moves[(r, right)] = can_capture + skipped
                        
                # Checks for backward movement
                if piece.color == PLAYER_ONE:
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
                    if can_capture:
                        piece.can_capture(bool=True)
                        moves_capture[(r, right)] = can_capture
                    else:
                        moves[(r, right)] = can_capture

                    if not piece.IsKing:
                        break

                # After capturing king can move n spaces behind enemy, but not normal pieces
                if can_capture:
                    piece.can_capture(bool=True)
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

        if type == "move":
            return moves
        elif type == "capture":
            return moves_capture
        elif type == "both":
            moves.update(moves_capture)
            return moves