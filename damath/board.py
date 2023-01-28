import pygame
from .piece import Piece
from .ruleset import Rules
from .constants import *
from audio_constants import *
from display_constants import BG_COLOR
from ui_class.font import *
from ui_class.textlist import TextList
from ui_class.tween import *
from objects import board_x_coords_surface, board_y_coords_surface, board_x_coords_rect, board_y_coords_rect, chips_surface, right_captured_pieces_surface, right_captured_pieces_rect, left_captured_pieces_rect, left_captured_pieces_surface, square_size
from options import *

pygame.mixer.init()

piece_height = square_size
piece_width = square_size * .874

class Board:

    def __init__(self, surface=None, theme=None):
        self._surface = surface
        self.pieces = []
        self.theme = theme    
        self.symbol_map = {}
        self.x_coordinates = None
        self.y_coordinates = None

        self.blue_pieces_count = 12
        self.orange_pieces_count = 12
        self.blue_kings = 0
        self.orange_kings = 0
        self.blue_captured = []
        self.orange_captured = []
        self.moveables = []

        self.selected_piece = None
        self.moved_piece = None
        self.valid_moves = None
        self.capturing_pieces = []

        self.ShowIndicators = True

        self.anim_move_piece = None
        self.anim_capture = None
        
        self.font_size = int(board_y_coords_rect.w * 0.9)
        self.font = pygame.font.Font(CookieRun_Regular, self.font_size)

        self.IsFlipped = False

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, value: pygame.Surface):
        self._surface = value

    def init(self):
        self._init_rotation()
        self._init_chips(self._surface)

    def update_theme(self, theme):
        self.theme = theme

    def _init_rotation(self):        
        """
        Initializes the first rotation of the board, as well as the coordinates.
        """       
        
        _x_coordinates = ["0", "1", "2", "3", "4", "5", "6", "7"]
        _y_coordinates = ["7", "6", "5", "4", "3", "2", "1", "0"]

        self.x_coordinates = TextList(self.font, OAR_BLUE, _x_coordinates,
                                    spacing = board_x_coords_rect.w * 0.105, 
                                    padding = [0, board_x_coords_rect.w * 0.05, 0, board_x_coords_rect.h * 0.2],
                                    vertical = False)
        self.y_coordinates = TextList(self.font, OAR_BLUE, _y_coordinates,
                                    spacing = board_y_coords_rect.h * 0.0775,
                                    padding = [board_y_coords_rect.h * 0.04, board_y_coords_rect.w * 0.2, 0, 0])

    def flip(self):
        """
        Rotates the board by 180 degrees.
        """
        self._rotate_180()
        self.recalculate_graveyard_positions()

    def _rotate_180(self):
        if self.IsFlipped:
            self.IsFlipped = False        
            _x_coordinates = ["0", "1", "2", "3", "4", "5", "6", "7"]
            _y_coordinates = ["7", "6", "5", "4", "3", "2", "1", "0"]

            self.x_coordinates = TextList(self.font, OAR_BLUE, _x_coordinates,
                                        spacing = board_x_coords_rect.w * 0.105, 
                                        padding = [0, board_x_coords_rect.w * 0.05, 0, board_x_coords_rect.h * 0.2],
                                        vertical = False)
            self.y_coordinates = TextList(self.font, OAR_BLUE, _y_coordinates,
                                        spacing = board_y_coords_rect.h * 0.0775,
                                      padding = [board_y_coords_rect.h * 0.04, board_y_coords_rect.w * 0.2, 0, 0])
        else:
            self.IsFlipped = True
            _x_coordinates = ["7", "6", "5", "4", "3", "2", "1", "0"]
            _y_coordinates = ["0", "1", "2", "3", "4", "5", "6", "7"]
            
            self.x_coordinates = TextList(self.font, OAR_BLUE, _x_coordinates, spacing=0)

            self.x_coordinates = TextList(self.font, OAR_BLUE, _x_coordinates,
                                        spacing = board_x_coords_rect.w * 0.105, 
                                        padding = [0, board_x_coords_rect.w * 0.05, 0, board_x_coords_rect.h * 0.2],
                                        vertical = False)
            self.y_coordinates = TextList(self.font, OAR_BLUE, _y_coordinates,
                                      spacing = board_y_coords_rect.h * 0.0775,
                                      padding = [board_y_coords_rect.h * 0.04, board_y_coords_rect.w * 0.2, 0, 0])
        
        # Reverse all board elements
        for i, row in enumerate(self.pieces):
            self.pieces[i].reverse()           
        self.pieces.reverse()
        self.reset_pieces()

    def reset_pieces(self):
        """
        Resets all piece's cells, and recalculates their x and y positions.
        """
        
        for col in range(COLS):
            for row in range(ROWS):
                self.pieces[col][row].col = col
                self.pieces[col][row].row = row
                self.pieces[col][row].calc_pos()

    def refresh(self):
        """
        Sets some variables to None.
        """
        self.selected_piece = None
        self.valid_moves = None

    def init_symbols(self, surface):
        surface.fill('#B9BABB')
        surface.set_colorkey('#B9BABB')
        SYMBOLS_SET_ONE = ["-", "x", "-", "x"]
        SYMBOLS_SET_TWO = ["+", "÷", "+", "÷"]
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
                        self.symbol_map.update({(col, row):SYMBOLS_SET_ONE[symbol_counter]})
                        symbol_counter += 1
                    case 1:
                        self.symbol_map.update({(col, row):SYMBOLS_SET_TWO[symbol_counter]})
                        symbol_counter += 1
                    case 2:
                        self.symbol_map.update({(col, row):SYMBOLS_SET_TWO[symbol_counter]})
                        symbol_counter += 1
                    case 3:
                        self.symbol_map.update({(col, row):SYMBOLS_SET_ONE[symbol_counter]})
                        symbol_counter += 1
                    case 4:
                        self.symbol_map.update({(col, row):SYMBOLS_SET_ONE[symbol_counter_reversed]})
                        symbol_counter_reversed -= 1
                    case 5:
                        self.symbol_map.update({(col, row):SYMBOLS_SET_TWO[symbol_counter_reversed]})
                        symbol_counter_reversed -= 1
                    case 6:
                        self.symbol_map.update({(col, row):SYMBOLS_SET_TWO[symbol_counter_reversed]})
                        symbol_counter_reversed -= 1
                    case 7:
                        self.symbol_map.update({(col, row):SYMBOLS_SET_ONE[symbol_counter_reversed]})
                        symbol_counter_reversed -= 1

    def get_col_row(self, cell):
        """
        Returns a cell relative to the board's coordinate given a raw cell.
        This considers the board's orientation. 
        """

        if cell[0] == -1 or cell[1] == -1:
            return

        col = cell[0]
        row = abs(cell[1] - 7)

        return col, row

    def to_raw(self, cell):
        """
        Converts a board-relative coordinate to raw coordinates.
        This considers the board's orientation. 
        """

        if cell[0] == -1 or cell[1] == -1:
            return

        col = abs(cell[0] - 7)
        row = cell[1]

        return col, row

    def get_abs(self, cell):
        """
        Returns the flipped values of the given cell.
        """

        if cell[0] == -1 or cell[1] == -1:
            return

        col = abs(cell[0] - 7)
        row = abs(cell[1] - 7)

        return col, row

    def get_piece(self, cell):
        """
        Returns the piece in the specified cell.
        This considers the board's orientation. 
        """

        if cell[0] == -1 or cell[1] == -1:
            return

        col = cell[0]
        row = abs(cell[1] - 7)

        return self.pieces[col][row]

    def _init_chips(self, surface):
        val_counter = 0
        
        match Rules.piece_values:
            case 'Naturals':
                num = [
                    3, 6, 9, 12,
                    8, 11, 4, 1, 
                    5, 2, 7, 10
                ]

            case 'Integers':
                num = [2, -5, 8, -11,
                       -7, 10, -3, 0,
                       4, -1, 6, -9]

            case 'Rationals':
                num = [
                    '3/10', '6/10', '9/10', '12/10',
                    '8/10', '11/10', '4/10', '1/10',
                    '5/10', '2/10', '7/10', '10/10'
                ]

            case 'Radicals':
                num = [
                    '144√8', '100√2', '-81√32', '-121√8',
                    '64√2', '36√32', '-25√18', '-49√8',
                    '16√32', '4√18', '-√8', '-9√2'
                ]
                
            case 'Polynomials':
                num = [
                    '78xy²', '66x²y', '-45y', '-55x',
                    '36x²y', '28y', '-15x', '-21xy²',
                    '10y', '6x', '-xy²', '-3x²y' 
                ]

        # Generate 8 empty lists of 8 size
        self.pieces = [[0]*COLS for i in range(ROWS)]

        # Generate player one chips
        val_counter = 11

        for row in range(2, -1, -1):
            for col in range(COLS):
                if col % 2 != ((row) % 2):
                    self.pieces[col][row] = Piece(surface, (col, row), PLAYER_ONE, num[val_counter])
                    self.moveables.append((col, row))

                    if enableDebugMode:
                        print(f"[Debug]: Created {PLAYER_ONE} piece \"{num[val_counter]}\" at cell ({col}, {row})")

                    val_counter-=1
                else:
                    self.pieces[col][row] = Piece(surface, (col, row), 0, 0)

        # Generate player two chips
        val_counter = 0

        for row in range(7, 4, -1):
            for col in range(COLS):
                if col % 2 != ((row) % 2):
                    self.pieces[col][row] = Piece(surface, (col, row), PLAYER_TWO, num[val_counter])
                    self.moveables.append((col, row))

                    if enableDebugMode:
                        print(f"[Debug]: Created {PLAYER_TWO} piece \"{num[val_counter]}\" at cell ({col}, {row})")

                    val_counter+=1
                else:
                    self.pieces[col][row] = Piece(surface, (col, row), 0, 0)


        # Generate imaginary pieces at the middle of the board
        for row in range(3, 5, 1):
            for col in range(COLS):
                self.pieces[col][row] = Piece(surface, (col, row), 0, 0)
        
        # print(f"Buffer") # Debug

    def set_mode(self, mode):
        """
        Sets the mode of the match.
        """
        
        self.mode = mode
        self.pieces = []

        self._init_chips(self._surface)
        self.draw_chips()

    def draw(self):
        """
        Draws the board and its elements.
        """

        if enableAnimations:
            #TODO: Needs optimization
            if self.anim_move_piece:
                self.anim_move_piece.update()
            if self.anim_capture:
                self.anim_capture.update()

        self.draw_symbols(self._surface)
        self.draw_coordinates()
        if Options.showIndicators:
            self.draw_selected_piece_indicator()
            self.draw_capturing_piece_indicator()
            self.draw_valid_moves(self.valid_moves)
        self.draw_chips()
        
    def draw_symbols(self, surface):
        self.init_symbols(surface)

    def draw_chips(self):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.pieces[row][col]

                if piece.color != 0:
                    piece.display()
        
        for piece in self.blue_captured:
            piece.display()
        for piece in self.orange_captured:
            piece.display()

    def draw_coordinates(self):
        """
        Draws the coordinates on the side of the board.
        """
        
        self.x_coordinates.draw(board_x_coords_surface, (0, 0))
        self.y_coordinates.draw(board_y_coords_surface, (0, 0))

    def draw_selected_piece_indicator(self):
        """
        Draws indicator for the selected piece.
        """
        
        if self.selected_piece == None:
            return

        col, row = self.get_col_row((self.selected_piece.col, self.selected_piece.row))

        selected_piece_rect = pygame.Rect((col * square_size, row * square_size),
                                            (square_size, square_size))
        pygame.draw.rect(self._surface, YELLOW, selected_piece_rect)
    
    def draw_capturing_piece_indicator(self):
        """
        Draws indicator for pieces that has captures.
        """
        
        if not self.capturing_pieces:
            return

        if Rules.allowMandatoryCapture:
            for i, piece in enumerate(self.capturing_pieces):
                col, row = (piece[0], piece[1])
                capturing_piece_rect = pygame.Rect((col*square_size, row*square_size), (square_size, square_size))   
                pygame.draw.rect(self._surface, LIME, capturing_piece_rect)

    def draw_valid_moves(self, moves):
        """
        Draw indicator for valid moves.
        """

        if not moves:
            return
        else:
            color = YELLOW
            if self.capturing_pieces:
                color = LIME
                
            for move in moves:
                col, row = move
                pygame.draw.circle(self._surface, color, (col * square_size + square_size//2, row * square_size + square_size//2), square_size*0.25)    
    
    def move_piece(self, piece, destination):
        """
        Moves given piece to destination cell.
        """

        destination_col = destination[0]
        destination_row = destination[1]
        destination_piece = self.pieces[destination_col][destination_row]

        if enableDebugMode:
            print(f"[Debug]: Moved piece {piece.color}: ({piece.col}, {piece.row}) -> ({destination_col}, {destination_row})")

        # Play animation
        if enableAnimations:
            self.anim_move_piece = Move(piece, (destination_piece.x, destination_piece.y), Options.chipMoveAnimationSpeed, ease_type=easeOutQuint)
            self.anim_move_piece.play()

        self.pieces[destination_col][destination_row] = piece
        self.pieces[piece.col][piece.row] = Piece(chips_surface, (piece.col, piece.row), 0, 0)

        piece.move(destination_col, destination_row)        

    def check_for_kings(self, piece):
        """
        Checks for possible kings. Executed once after every move.
        """
        if piece.IsKing and piece.HasPossibleCapture:
            return

        if self.IsFlipped:
            orange_home_row = 0
            blue_home_row = 7
        else:
            orange_home_row = 7
            blue_home_row = 0

        if piece.color == PLAYER_ONE:
            if piece.row == orange_home_row:
                piece.make_king()
                self.blue_kings += 1
                CAPTURE_SOUND.play()
        else: # piece.color == PLAYER_TWO
            if piece.row == blue_home_row:
                piece.make_king()
                self.orange_kings += 1
                CAPTURE_SOUND.play()
    
    def piece_landed(self, col, row):
        return self.symbol_map[(col, row)]

    def set_all_moveables(self, IsMovable=True):
        """
        Sets all pieces state to be movable or not.
        """
        
        for row in range(ROWS):
            for col in range(COLS):
                self.pieces[col][row].IsMovable = IsMovable

    def move_to_graveyard(self, pieces):
        """
        Moves a piece/or pieces to the graveyard (capture).
        """
        for piece in pieces:
            if piece.color == PLAYER_ONE: # Blue
                captured_piece = Piece(left_captured_pieces_surface, (0, 0), piece.color, piece.number)# if not self.IsFlipped else Piece(right_captured_pieces_surface, (0, 0), piece.color, piece.number)

                if piece.IsKing:
                    captured_piece.IsKing = True
                captured_piece.IsCaptured = True
                self.blue_captured.append(captured_piece)
                self.blue_pieces_count -= 1
            else:
                captured_piece = Piece(right_captured_pieces_surface, (0, 0), piece.color, piece.number)# if not self.IsFlipped else Piece(left_captured_pieces_surface, (0, 0), piece.color, piece.number)

                if piece.IsKing:
                    captured_piece.IsKing = True
                captured_piece.IsCaptured = True
                self.orange_captured.append(captured_piece)
                self.orange_pieces_count -= 1

            self.pieces[piece.col][piece.row] = Piece(self._surface, (piece.col, piece.row), 0, 0)

        self.recalculate_graveyard_positions()

    def recalculate_graveyard_positions(self):
        for i, captured_piece in enumerate(self.blue_captured):
            if i < 9:
                captured_piece.x = (left_captured_pieces_surface.get_width() // 2) - 2 if not self.IsFlipped else (left_captured_pieces_surface.get_width() // 2) - (piece_width)
                captured_piece.y = (left_captured_pieces_rect.top - (piece_height + piece_height*0.75)) + ((i + 1) * piece_height) if not self.IsFlipped else ((left_captured_pieces_rect.bottom - (piece_height - piece_height*0.25)) - ((i + 1) * piece_height)) - 5
            else:
                captured_piece.x = (left_captured_pieces_surface.get_width() // 2) - piece_width if not self.IsFlipped else (left_captured_pieces_surface.get_width() // 2)
                captured_piece.y = (left_captured_pieces_rect.top - (piece_height + piece_height*0.75)) + (((i + 1) - 9) * piece_height) if not self.IsFlipped else ((left_captured_pieces_rect.bottom - (piece_height - piece_height*0.25)) - (((i + 1) - 9) * piece_height)) - 5
        for i, captured_piece in enumerate(self.orange_captured):
            if i < 9:
                captured_piece.x = (right_captured_pieces_surface.get_width() // 2) - (piece_width) if not self.IsFlipped else (right_captured_pieces_surface.get_width() // 2) - 2
                captured_piece.y = ((right_captured_pieces_rect.bottom - (piece_height - piece_height*0.25)) - ((i + 1) * piece_height)) - 5 if not self.IsFlipped else (right_captured_pieces_rect.top - (piece_height + piece_height*0.75)) + ((i + 1) * piece_height)
            else:
                captured_piece.x = (right_captured_pieces_surface.get_width() // 2) if not self.IsFlipped else (right_captured_pieces_surface.get_width() // 2) - piece_width
                captured_piece.y = ((right_captured_pieces_rect.bottom - (piece_height - piece_height*0.25)) - (((i + 1) - 9) * piece_height)) - 5 if not self.IsFlipped else (right_captured_pieces_rect.top - (piece_height + piece_height*0.75)) + (((i + 1) - 9) * piece_height)

    def add_piece(self, piece):
        """
        Adds a piece to the board, given a piece object.
        """
        self.pieces[piece.col][piece.row] = piece
        self.moveables.append((piece.col, piece.row))

        if piece.color == PLAYER_ONE:
            self.blue_pieces_count += 1
        else:
            self.orange_pieces_count += 1

    def remove(self, cell):
        """
        Removes a piece from the board, given raw cell arguments.
        This does not decrement current pieces count.
        """
        col, row = self.get_col_row(cell)
        self.pieces[col][row] = Piece(self._surface, (col, row), 0, 0)

    def capture(self, cell):
        """
        Captures a piece from the board moving it to the graveyard.
        This receives raw cell arguments.
        """
        piece = self.get_piece(cell)
        self.move_to_graveyard(piece)

    def get_valid_moves(self, piece, type="all", BoardIsFlipped=False):
        """
        Returns all the possible moves of the given piece.
        """
        
        moves = {}
        up = -1
        down = 1
        # Raw coordinates
        above = abs(piece.row - 7) - 1
        below = abs(piece.row - 7) + 1
        
        if piece.HasPossibleCapture:
            piece.set_capture_status(False)

        if piece.color == PLAYER_ONE:
            # Up    
            moves.update(self._check_left(piece, starting_row=above, direction=up, max_distance=-1, type=type, BoardIsFlipped=BoardIsFlipped))
            moves.update(self._check_right(piece, starting_row=above, direction=up, max_distance=-1, type=type, BoardIsFlipped=BoardIsFlipped))
            # Down
            moves.update(self._check_left(piece, starting_row=below, direction=down, max_distance=ROWS, type=type, BoardIsFlipped=BoardIsFlipped))
            moves.update(self._check_right(piece, starting_row=below, direction=down, max_distance=ROWS, type=type, BoardIsFlipped=BoardIsFlipped))
        else: # piece.color == ORANGE:
            # Up
            moves.update(self._check_left(piece, starting_row=above, direction=up, max_distance=-1, type=type, BoardIsFlipped=BoardIsFlipped))
            moves.update(self._check_right(piece, starting_row=above, direction=up, max_distance=-1, type=type, BoardIsFlipped=BoardIsFlipped))
            # Down
            moves.update(self._check_left(piece, starting_row=below, direction=down, max_distance=ROWS, type=type, BoardIsFlipped=BoardIsFlipped))
            moves.update(self._check_right(piece, starting_row=below, direction=down, max_distance=ROWS, type=type, BoardIsFlipped=BoardIsFlipped))
        
        return moves

    def _check_left(self, piece, starting_row, direction, max_distance, type, BoardIsFlipped, skipped=[]):
        moves = {}
        moves_capture = {}
        can_capture = []
        next_enemy_piece = 0
        left = piece.col - 1

        for row in range(starting_row, max_distance, direction):
            # Break if spot is out of bounds of the board
            if left < 0:
                break

            # Break if there are two or more enemy pieces in succession
            if next_enemy_piece >= 2:
                break

            cell_to_check = self.get_piece((left, row))

            # Check if cell is empty
            if cell_to_check.color == 0:
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
                        piece.set_capture_status()
                        moves[(left, row)] = can_capture

                # Check for backward movement
                if piece.color == PLAYER_ONE:
                    if direction == 1: # Down
                        # If board is flipped, downward movement is forward, thus allowed
                        if BoardIsFlipped:
                            pass
                        # If board is not flipped, backward movement is for captures only
                        else:
                            if can_capture:
                                pass
                            # Piece is not capturing, only king pieces can move backward
                            else:
                                if not piece.IsKing:
                                    break
                    else: # Up
                        # If board is flipped, backward movement is for captures only
                        if BoardIsFlipped:
                            if can_capture:
                                pass
                            # Piece is not capturing, only king pieces can move backward
                            else:
                                if not piece.IsKing:
                                    break
                        # Forward movement
                        else:
                            pass
                else: # if piece.color == PLAYER_TWO
                    if direction == -1: # Up
                        # Same logic
                        if BoardIsFlipped:
                            pass
                        else:
                            if can_capture:
                                pass
                            else:
                                if not piece.IsKing:
                                    break
                    else:
                        if BoardIsFlipped:
                            if can_capture:
                                pass
                            # Piece is not capturing, only king pieces can move backward
                            else:
                                if not piece.IsKing:
                                    break
                        # If board is not flipped, backward movement is for captures only
                        else:
                            pass

                # Piece can capture
                if can_capture:
                    piece.set_capture_status(True)
                    moves_capture[(left, row)] = can_capture
                else:
                    moves[(left, row)] = can_capture

                if not piece.IsKing:
                    break
                    
                if can_capture:
                    piece.set_capture_status(True)
                    if piece.IsKing:
                        pass
                    else:
                        break
            # There's ally piece in cell
            elif cell_to_check.color == piece.color:
                break
            # There's enemy piece in cell
            else:
                next_enemy_piece += 1
                can_capture = [cell_to_check]

            left -= 1

        match type:
            case "move":
                return moves
            case "capture":
                return moves_capture
            case"all":
                moves.update(moves_capture)
                return moves
 
    def _check_right(self, piece, starting_row, direction, max_distance, type, BoardIsFlipped, skipped=[]):
        moves = {}
        moves_capture = {}
        can_capture = []
        next_enemy_piece = 0
        right = piece.col + 1

        for row in range(starting_row, max_distance, direction):
            if right >= COLS:
                break

            if next_enemy_piece >= 2:
                break

            cell_to_check = self.get_piece((right, row))
            
            # if BoardIsFlipped:
            #     right = abs(right - 7)
            #     row = abs(row - 7)

            # Check if spot is empty
            if cell_to_check.color == 0:
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
                        piece.set_capture_status()
                        moves[(right, row)] = can_capture + skipped
                        
                # Checks for backward movement
                if piece.color == PLAYER_ONE:
                    if direction == 1:
                        if BoardIsFlipped:
                            pass
                        else:
                            if can_capture:
                                pass
                            else:
                                if not piece.IsKing:
                                    break
                    else:
                        if BoardIsFlipped:
                            if can_capture:
                                pass
                            # Piece is not capturing, only king pieces can move backward
                            else:
                                if not piece.IsKing:
                                    break
                        # If board is not flipped, backward movement is for captures only
                        else:
                            pass
                else: # if LIGHT_BLUE
                    if direction == -1:
                        if BoardIsFlipped:
                            pass
                        else:
                            if can_capture:
                                pass
                            else:
                                if not piece.IsKing:
                                    break
                    else:
                        if BoardIsFlipped:
                            if can_capture:
                                pass
                            # Piece is not capturing, only king pieces can move backward
                            else:
                                if not piece.IsKing:
                                    break
                        # If board is not flipped, backward movement is for captures only
                        else:
                            pass

                if can_capture:
                    piece.set_capture_status(True)
                    moves_capture[(right, row)] = can_capture
                else:
                    moves[(right, row)] = can_capture

                if not piece.IsKing:
                    break

                # After capturing king can move n spaces behind enemy, but not normal pieces
                if can_capture:
                    piece.set_capture_status(True)
                    if piece.IsKing:
                        pass
                    else:
                        break
            # Piece is ally
            elif cell_to_check.color == piece.color:
                break
            # Piece is enemy
            else:
                next_enemy_piece += 1
                can_capture = [cell_to_check]
                
            # Move right by 1 tile
            right += 1

        match type:
            case "move":
                return moves
            case "capture":
                return moves_capture
            case"all":
                moves.update(moves_capture)
                return moves