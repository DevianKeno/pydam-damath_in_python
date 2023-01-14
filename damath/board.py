import pygame
from .piece import Piece
from .constants import *
from assets import BOARD
from audio_constants import *
from display_constants import BG_COLOR
from ui_class.tween import *
from objects import p1_captured_pieces_surface, p1_captured_pieces_rect, p2_captured_pieces_rect, p2_captured_pieces_surface
from options import *

pygame.mixer.init()

class Board:
    
    mode = MODE

    def __init__(self, surface, theme=None):
        self.surface = surface

        self.board = []
        self.theme = theme    
        self.symbol_map = {}

        self.blue_pieces_count = 12
        self.orange_pieces_count = 12
        self.blue_kings = 0
        self.orange_kings = 0
        self.blue_captured = []
        self.orange_captured = []
        self.moveables = []

        self.anim = None
        self.anim_capture = None
        
        self.init_chips(self.surface)

    def update_theme(self, theme):
        self.theme = theme

    def init_symbols(self, surface):
        surface.fill('#B9BABB')
        surface.set_colorkey('#B9BABB')
        SYMBOLS_ONE = ["-", "x", "-", "x"]
        SYMBOLS_TWO = ["+", "÷", "+", "÷"]
        symbol_counter = 0
        symbol_counter_reversed = 3
        
        for col in range(COLS):
            symbol_counter = 0
            symbol_counter_reversed = 3

            for row in range(0, ROWS, 2):
                if (col % 2 == 0):
                    row += 1
                    
                match col:
                    case 0:
                        self.symbol_map.update({(col, row):SYMBOLS_ONE[symbol_counter]})
                        symbol_counter += 1
                    case 1:
                        self.symbol_map.update({(col, row):SYMBOLS_TWO[symbol_counter]})
                        symbol_counter += 1
                    case 2:
                        self.symbol_map.update({(col, row):SYMBOLS_TWO[symbol_counter]})
                        symbol_counter += 1
                    case 3:
                        self.symbol_map.update({(col, row):SYMBOLS_ONE[symbol_counter]})
                        symbol_counter += 1
                    case 4:
                        self.symbol_map.update({(col, row):SYMBOLS_ONE[symbol_counter_reversed]})
                        symbol_counter_reversed -= 1
                    case 5:
                        self.symbol_map.update({(col, row):SYMBOLS_TWO[symbol_counter_reversed]})
                        symbol_counter_reversed -= 1
                    case 6:
                        self.symbol_map.update({(col, row):SYMBOLS_TWO[symbol_counter_reversed]})
                        symbol_counter_reversed -= 1
                    case 7:
                        self.symbol_map.update({(col, row):SYMBOLS_ONE[symbol_counter_reversed]})
                        symbol_counter_reversed -= 1

    def init_chips(self, surface):
        val_counter = 0
        
        match self.mode:
            case 'Naturals':
                num = [
                    10, 7, 2, 5,
                    1, 4, 11, 8, 
                    12, 9, 6, 3
                ]

            case 'Integers':
                num = [2, -5, 8, -11,
                       -7, 10, -3, 0,
                       4, -1, 6, -9]

            case 'Rationals':
                num = [
                    '10/10', '7/10', '2/10', '5/10',
                    '1/10', '4/10', '11/10', '8/10',
                    '12/10', '9/10', '6/10', '3/10'
                ]

            case 'Radicals':
                num = [
                    '9√2', '-√8', '4√18', '16√32',
                    '-49√8', '-25√18', '36√32', '64√2',
                    '-121√18', '-81√32', '100√2', '144√8'
                ]
                
            case 'Polynomials':
                num = [
                    '3x²y', '-xy²', '6x', '10y',
                    '21xy²', '-15x', '28y', '36x²y',
                    '-55x', '-45y', '66x²y', '78xy' 
                ]

        self.board = [[0]*COLS for i in range(ROWS)]

        """
        Generate player one chips
        """
        val_counter = 11

        for row in range(2, -1, -1):
            for col in range(COLS):
                if col % 2 != ((row) % 2):
                    self.board[col][row] = Piece(surface, (col, row), PLAYER_ONE, num[val_counter])
                    self.moveables.append((col, row))

                    if enableDebugMode:
                        print(f"[Debug]: Created {PLAYER_ONE} piece \"{num[val_counter]}\" at cell ({col}, {row})")

                    val_counter-=1
                else:
                    self.board[col][row] = Piece(surface, (col, row), 0, 0)

        """
        Generate player two chips
        """
        val_counter = 0

        for row in range(7, 4, -1):
            for col in range(COLS):
                if col % 2 != ((row) % 2):
                    self.board[col][row] = Piece(surface, (col, row), PLAYER_TWO, num[val_counter])
                    self.moveables.append((col, row))

                    if enableDebugMode:
                        print(f"[Debug]: Created {PLAYER_TWO} piece \"{num[val_counter]}\" at cell ({col}, {row})")

                    val_counter+=1
                else:
                    self.board[col][row] = Piece(surface, (col, row), 0, 0)

        """
        Generate imaginary pieces at the middle of the board
        """
        for row in range(3, 5, 1):
            for col in range(COLS):
                self.board[col][row] = Piece(surface, (col, row), 0, 0)
        
        # print(f"Buffer") # Debug

    def set_mode(self, mode):
        self.mode = mode
        self.board = []
        self.init_chips(self.surface)
        self.draw_chips(self.surface)

    def move_piece(self, piece, dest_cell=()):
        """
        Moves piece to destination cell.
        """
        if enableDebugMode:
            print(f"[Debug]: Moved piece {piece.color}: ({piece.col}, {piece.row}) -> ({dest_cell[0]}, {dest_cell[1]})")

        _piece = self.board[piece.col][piece.row]
        _piece_dest = self.board[dest_cell[0]][dest_cell[1]]

        # Play animation
        if enableAnimations:
            self.anim = Move(_piece, (_piece_dest.x, _piece_dest.y), 0.5, ease_type=easeOutQuint)
            self.anim.play()

        # Swap current piece with destination
        self.board[piece.col][piece.row], self.board[dest_cell[0]][dest_cell[1]] = self.board[dest_cell[0]][dest_cell[1]], self.board[piece.col][piece.row]
        # Re-swap x and y variables
        _piece.x, _piece_dest.x = _piece_dest.x, _piece.x
        _piece.y, _piece_dest.y = _piece_dest.y, _piece.y

        # Set dest cell as movable
        self.moveables.append((dest_cell[0], dest_cell[1]))
        del self.moveables[self.moveables.index((piece.col, piece.row))]
        
        piece.move(dest_cell[0], dest_cell[1])

    def check_for_kings(self, piece):
        """
        Checks for possible kings. Executed once after every move.
        """
        if piece.IsKing and piece.HasPossibleCapture:
            return

        if piece.color == PLAYER_ONE:
            if piece.row == 7:
                piece.make_king()
                CAPTURE_SOUND.play()
                self.blue_kings += 1
        else:
            if piece.row == 0:
                piece.make_king()
                CAPTURE_SOUND.play()
                self.orange_kings += 1
    
    def piece_skipped(self, piece, col, row, bool):
        piece.HasSkipped = bool

    def piece_had_skipped(self, piece, col, row):
        return piece.HasSkipped
        
    def has_possible_capture(self, piece):
        return piece.HasPossibleCapture
    
    def piece_landed(self, col, row):
        return self.symbol_map[(col, row)]

    def get_piece(self, col, row):
        return self.board[col][row]

    def draw_contents(self, surface):
        self.init_symbols(surface)

    def draw_chips(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]

                if piece.color != 0:
                    piece.display()
        
        for piece in self.blue_captured:
            piece.display()

        for piece in self.orange_captured:
            piece.display()

    def move_to_graveyard(self, pieces):
        for piece in pieces:
            if piece.color == PLAYER_ONE: # Blue
                captured_piece = Piece(p2_captured_pieces_surface, (0, 0), piece.color, piece.number)

                if piece.IsKing:
                    captured_piece.IsKing = True
                captured_piece.IsCaptured = True
                self.blue_captured.append(captured_piece)

                if len(self.blue_captured) <= 9:
                    captured_piece.x = (p2_captured_pieces_surface.get_width() // 2) - 2
                    captured_piece.y = (p2_captured_pieces_rect.top - (piece.h + piece.h*0.75)) + (len(self.blue_captured) * piece.h)
                else:
                    captured_piece.x = (p2_captured_pieces_surface.get_width() // 2) - piece.w
                    captured_piece.y = (p2_captured_pieces_rect.top - (piece.h + piece.h*0.75)) + ((len(self.blue_captured) - 9) * piece.h)
                self.blue_pieces_count -= 1
            else:
                captured_piece = Piece(p1_captured_pieces_surface, (0, 0), piece.color, piece.number)

                if piece.IsKing:
                    captured_piece.IsKing = True
                captured_piece.IsCaptured = True
                self.orange_captured.append(captured_piece)

                if len(self.orange_captured) <= 9:
                    captured_piece.x = (p1_captured_pieces_surface.get_width() // 2) - (piece.w)
                    captured_piece.y = ((p1_captured_pieces_rect.bottom - (piece.h - piece.h*0.25)) - (len(self.orange_captured) * piece.h)) - 5
                else:
                    captured_piece.x = (p1_captured_pieces_surface.get_width() // 2)
                    captured_piece.y = ((p1_captured_pieces_rect.bottom - (piece.h - piece.h*0.25)) - ((len(self.orange_captured) - 9) * piece.h)) - 5
                
                self.orange_pieces_count -= 1
            self.board[piece.col][piece.row] = Piece(self.surface, (piece.col, piece.row), 0, 0)

    def add_piece(self, piece):
        self.board[piece.col][piece.row] = piece
        self.moveables.append((piece.col, piece.row))

    def remove(self, piece):
        self.board[piece.col][piece.row] = Piece(self.surface, (piece.col, piece.row), 0, 0)

    def get_valid_moves(self, piece, type="all"):
        moves = {}
        up = 1
        down = -1
        above = piece.row+1
        below = piece.row-1
        
        if piece.HasPossibleCapture:
            piece.can_capture(False)

        if piece.color == PLAYER_ONE:
            # Up    
            moves.update(self._check_left(piece, starting_row=above, direction=up, max_distance=ROWS, type=type))
            moves.update(self._check_right(piece, starting_row=above, direction=up, max_distance=ROWS, type=type))
            # Down (Capture only)
            moves.update(self._check_left(piece, starting_row=below, direction=down, max_distance=-1, type=type))
            moves.update(self._check_right(piece, starting_row=below, direction=down, max_distance=-1, type=type))
        else: # piece.color == ORANGE:
            # Up (Capture only)
            moves.update(self._check_left(piece, starting_row=above, direction=up, max_distance=ROWS, type=type))
            moves.update(self._check_right(piece, starting_row=above, direction=up, max_distance=ROWS, type=type))
            # Down
            moves.update(self._check_left(piece, starting_row=below, direction=down, max_distance=-1, type=type))
            moves.update(self._check_right(piece, starting_row=below, direction=down, max_distance=-1, type=type))

        return moves

    def _check_left(self, piece, starting_row, direction, max_distance, type, skipped=[]):
        moves = {}
        moves_capture = {}
        can_capture = []
        next_enemy_piece = 0
        left = piece.col - 1

        for r in range(starting_row, max_distance, direction):
            # If left spot is out of bounds of the board
            if left < 0:
                break

            if next_enemy_piece >= 2:
                break

            current_spot = self.board[left][r]
            
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
                        moves[(left, r)] = can_capture

                # Check if the backward movement is for capturing
                if piece.color == PLAYER_ONE:
                    if direction == -1: # Down
                        # Piece can capture, allow movement
                        if can_capture:
                            pass
                        # Piece is not capturing, only king pieces can move
                        else:
                            if not piece.IsKing:
                                break
                else: # if BLUE
                    if direction == 1: # Up
                        if can_capture:
                            pass
                        else:
                            if not piece.IsKing:
                                break

                # if skipped and not can_capture:
                #     break
                # el
                if skipped:
                    moves[(left, r)] = can_capture + skipped
                else:
                    if next_enemy_piece >= 2:
                        break
                    if can_capture:
                        piece.can_capture(bool=True)
                        moves_capture[(left, r)] = can_capture
                    else:
                        moves[(left, r)] = can_capture

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
        elif type == "all":
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

            current_spot = self.board[right][r]

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
                        moves[(right, r)] = can_capture + skipped
                        
                # Checks for backward movement
                if piece.color == PLAYER_ONE:
                    if direction == -1:
                        if can_capture:
                            pass
                        else:
                            if not piece.IsKing:
                                break
                else: # if LIGHT_BLUE
                    if direction == 1:
                        if can_capture:
                            pass
                        else:
                            if not piece.IsKing:
                                break

                if skipped and not can_capture:
                    break
                elif skipped:
                    moves[(right, r)] = can_capture + skipped
                else:
                    if next_enemy_piece >= 2:
                        break
                    if can_capture:
                        piece.can_capture(bool=True)
                        moves_capture[(right, r)] = can_capture
                    else:
                        moves[(right, r)] = can_capture

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
        elif type == "all":
            moves.update(moves_capture)
            return moves