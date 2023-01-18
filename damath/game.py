import pygame
from .board import Board
from .piece import Piece
from .scoreboard import Scoreboard
from .constants import *
from .timer import *
from audio_constants import *
from ui_class.tween import *
from objects import square_size
from options import *

pygame.mixer.init()

class Game:

    def __init__(self, surface, board, scoreboard, theme):
        self.surface = surface
        self.board = board
        self.scoreboard = scoreboard
        self.theme = theme
        self.selected_cell = None       # Raw cell
        self.selected_cell_board = None # Cell relative to board's coordinates

    def _init(self):
        self.moved_piece = None
        self.selected = None
        self.board = Board(self.surface, self.theme) # for game reset
        self.capturing_pieces = []
        self.valid_moves = {}
        self.TurnRequiresCapture = False
        self.turn = PLAYER_ONE

    def set_mode(self, mode):
        Piece.mode = mode
        Scoreboard.mode = mode
        self.board.set_mode(mode)

    def update(self):
        if enableAnimations:
            if self.board.anim:
                self.board.anim.update()
            if self.board.anim_capture:
                self.board.anim_capture.update()

        self.board.draw_contents(self.surface)
        self.board.draw_coordinates()

        if self.selected:
            self.draw_selected_piece_indicator(self.surface)
            self.draw_valid_moves(self.valid_moves)
        self.draw_capturing_piece_indicator(self.surface)

        self.board.draw_chips(self.surface)

        self.scoreboard.draw_scores()
        self.scoreboard.draw_turn_indicator(self.turn)

        pygame.display.update() 

    def winner(self):   
        if (self.board.blue_pieces_count <=0 or self.board.orange_pieces_count <= 0 or global_timer.get_remaining_time() == (-1, 59)):
            red_score, blue_score = self.scoreboard.score()

            if red_score > blue_score:
                return PLAYER_ONE 
            elif blue_score > red_score:
                return PLAYER_ONE
            else:
                return "TIE"
        return None

    def reset(self):
        self.scoreboard.reset()
        self._init()
        turn_timer.stop()
        global_timer.stop()

    def select(self, cell):
        """
        Selects a cell or move given raw cell arguments.
        """
        # Raw cell
        self.selected_cell = cell
        # Cell relative to the board's coordinates
        self.selected_cell_board = self.board.get_col_row(self.selected_cell)

        # If a piece is selected
        if self.selected:
            self.select_move()
        else:
            self.select_piece(cell)
        
    def select_move(self):
        """
        Selects a valid move.
        """
        
        if (self.selected_cell) in self.valid_moves:
            self._move_piece(self.selected, self.selected_cell)
        else:
            self.selected = None
        return

    def select_piece(self, cell):
        """
        Selects a piece.
        """
        
        col, row  = self.board.get_col_row(self.selected_cell)

        if self.moved_piece == None:
            piece = self.board.get_piece(self.selected_cell)
        else:
            piece = self.moved_piece

        if piece.color != 0 and piece.color == self.turn:
            self.selected = piece
            moves_to_get = "all"
            
            if enableDebugMode:
                print(f"[Debug]: Selected piece ({col}, {row})")

            if enableMandatoryCapture:
                if not piece.IsMovable:
                    return

                if self.TurnRequiresCapture:
                    moves_to_get = "capture"

            self.valid_moves = self._get_moves_of(self.selected, moves_to_get)

            if not self.valid_moves:
                if not self.board.piece_had_skipped(self.selected, col, row):
                    INVALID_SOUND.play()
                    return

                self.board.piece_skipped(self.selected, col, row, bool=False)
                self.change_turn()
            else:
                SELECT_SOUND.play()
                
            return

        elif self.moved_piece == None and not self.selected and (piece.color == 0 or piece.color != self.turn):
            INVALID_SOUND.play()

        return

    def _get_moves_of(self, piece, moves_to_get):
        """
        Gets the valid moves of the piece.
        """

        return self.board.get_valid_moves(piece, moves_to_get, self.board.IsFlipped)

    def get_destination_relative(self, destination):
        if self.board.IsFlipped:
            col = destination[0]
            row = abs(destination[0] - 7)
        else:
            
            col = destination[0]
            row = abs(destination[0] - 7)

        return col, row

    def _move_piece(self, piece, destination):
        """
        Moves a piece to the specified cell.
        """

        # col, row = self.board.get_col_row(self.selected)
        destination_piece = self.board.get_piece(self.selected_cell)
        col, row = destination_piece.col, destination_piece.row

        if destination_piece.color == 0 and (destination) in self.valid_moves:
            self.board.swap_pieces(self.selected, destination_piece)
            self.moved_piece = destination_piece
            skipped_list = list(self.valid_moves)

            # Get the skipped piece of the move:skipped_piece pair
            skipped_piece = self.valid_moves[destination]

            if skipped_piece:
                CAPTURE_SOUND.play()
                self.board.piece_skipped(self.selected, col, row, bool=True)
                operations = []

                if len(skipped_piece) > 1:
                    for i in range(len(skipped_list)-1, (len(skipped_list)-1)-len(skipped_piece), -1):
                        operations.append(self.board.piece_landed(skipped_list[i][0], skipped_list[i][1]))
                else:
                    operations.append(self.board.piece_landed(col, row))
                self.scoreboard.score_update(self.selected, skipped_piece, operations)
                
                self.board.move_to_graveyard(skipped_piece)
            else:
                MOVE_SOUND.play()

            if not self.board.piece_had_skipped(self.selected, col, row):
                self.board.piece_skipped(self.selected, col, row, bool=False)
                self.change_turn()
        else:
            self.selected = None
            return False
        self.selected = None
        return True
        
    def draw_valid_moves(self, moves):
        color = YELLOW

        if self.TurnRequiresCapture:
            color = LIME

        if moves:
            for move in moves:
                col, row = move
                pygame.draw.circle(self.surface, color, (col * square_size + square_size//2, row * square_size + square_size//2), square_size*0.25)
    
    def draw_selected_piece_indicator(self, surface):
        col, row = self.selected_cell

        selected_piece_rect = pygame.Rect((col * square_size, row * square_size),
                                            (square_size, square_size))
        pygame.draw.rect(surface, YELLOW, selected_piece_rect)
    
    def draw_capturing_piece_indicator(self, surface):
        if enableMandatoryCapture:
            if self.TurnRequiresCapture:
                for i in range(len(self.capturing_pieces)):
                    col, row = (self.capturing_pieces[i][0], self.capturing_pieces[i][1])
                    capturing_piece_rect = pygame.Rect((col*square_size, row*square_size), (square_size, square_size))   
                    pygame.draw.rect(surface, LIME, capturing_piece_rect)

    def change_turn(self):
        if self.selected:
            self.board.check_for_kings(self.selected)

        self.selected = None
        self.moved_piece = None
        self.valid_moves = {}

        if self.turn == PLAYER_ONE:
            self.turn = PLAYER_TWO
        else:
            self.turn = PLAYER_ONE

        turn_timer.reset()
        
        if enableDebugMode:
            print(f"[Debug]: Turns changed, now {self.turn}")

        if enableMandatoryCapture:
            self.capturing_pieces.clear()
            self.board.set_all_moveables(False)
            self.check_for_captures()

    def check_for_captures(self):
        """
        Checks all pieces of the current turn for possible captures.
        """
        
        if enableDebugMode:
            print(f"[Debug]: Checking for possible captures for {self.turn}...")

        blue_count = self.board.blue_pieces_count + self.board.blue_kings
        orange_count = self.board.orange_pieces_count + self.board.orange_kings
        capturing_pieces = 0
        
        for row in range(ROWS):
            if blue_count == 0 or orange_count == 0:
                break

            for col in range(COLS):
                if blue_count == 0 or orange_count == 0:
                    break
                
                piece = self.board.get_piece((col, row))
                
                if piece.color == self.turn:
                    if self.board.get_valid_moves(piece, "capture", self.board.IsFlipped):
                        if piece.HasPossibleCapture:
                            if enableDebugMode:
                                print(f"[Debug]: Possible capture by ({col}, {row})")
                            
                            piece.IsMovable = True
                            self.capturing_pieces.append((col, row))
                            capturing_pieces += 1

                    if self.turn == PLAYER_ONE:
                        blue_count -= 1
                    else:
                        orange_count -= 1

        if capturing_pieces == 0:
            if enableDebugMode:
                print(f"[Debug]: No possible captures for {self.turn}")

            self.capturing_pieces.clear()
            self.board.set_all_moveables(True)
            self.TurnRequiresCapture = False
        else:
            self.TurnRequiresCapture = True