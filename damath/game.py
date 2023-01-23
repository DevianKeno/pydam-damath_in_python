import pygame
from multipledispatch import dispatch
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

    def __init__(self, surface, board, scoreboard, theme, IsMultiplayer=True):
        self.surface = surface
        self.board = board
        self.scoreboard = scoreboard
        self.theme = theme
        self.selected_cell = None   # Cell | Raw cell
        self.selected_tile = None   # Tile | Cell relative to board's coordinates
        self.IsMultiplayer = IsMultiplayer
        self.command = ''
        self.ControlsIsEnabled = True

    def _init(self):
        self.moved_piece = None
        self.selected_piece = None
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
            #TODO: Needs optimization
            if self.board.anim_move_piece:
                self.board.anim_move_piece.update()
            if self.board.anim_capture:
                self.board.anim_capture.update()

        self.board.draw_contents(self.surface)
        self.board.draw_coordinates()

        if self.selected_piece:
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

    def select(self, cell, IsOperator=False):
        """
        Selects a cell or move given raw cell arguments.
        """

        if IsOperator:
            if self.selected_piece:
                self.select_move(cell)
                return
            else:
                self.select_piece(self.board.get_piece(cell), IsOperator)
                return

        if self.IsMultiplayer:
            if not self.ControlsIsEnabled:
                return
        
        # Cell = raw coordinates
        self.selected_cell = cell
        # Tile = cell relative to the board's coordinates, regardless of orientation
        self.selected_tile = self.board.get_col_row(cell)

        piece_to_select = self.board.get_piece(cell)

        # If a piece had already captured
        if self.moved_piece:
            if piece_to_select == self.moved_piece:
                piece_to_select = self.moved_piece

        # If a piece is selected
        if self.selected_piece:
            if piece_to_select.color == self.turn:
                if self.TurnRequiresCapture:
                    if piece_to_select.HasPossibleCapture:
                        self.select_piece(piece_to_select)
                else:
                    self.select_piece(piece_to_select)
            else:
                return self.select_move(cell)
        else:
            if self.TurnRequiresCapture:
                if piece_to_select.HasPossibleCapture:
                    self.select_piece(piece_to_select)
            else:
                self.select_piece(piece_to_select)
        
    def select_move(self, cell):
        """
        Selects a valid move, given a raw cell argument.
        """

        if not self.selected_piece:
            raise RuntimeError("No piece selected, select a piece using select_piece(piece_to_select) first.")
        
        if (cell) in self.valid_moves:
            # Send to console
            if self.IsMultiplayer:
                col, row = self.board.get_col_row(cell)
                self.command = "selmove {} {} {} {}".format(self.selected_piece.col, self.selected_piece.row, col, row)
            self._move_piece(self.selected_piece, cell)

            if not self.selected_piece.HasPossibleCapture:
                self.change_turn()

            return self.command
        else:
            self.selected_piece = None

    def select_piece(self, piece, IsOperator=False):
        """
        Selects a piece, given a piece object.
        """
        
        if IsOperator:
            pass
        else:
            if piece.color != self.turn:
                INVALID_SOUND.play()
                return

        self.selected_piece = piece

        if enableDebugMode:
            print(f"[Debug]: Selected piece ({self.selected_piece.col}, {self.selected_piece.row})")

        # Get moves
        moves_to_get = "all"
        if enableMandatoryCapture:
            if not self.selected_piece.IsMovable:
                return

            if self.TurnRequiresCapture:
                moves_to_get = "capture"

        self.valid_moves = self._get_moves_of(self.selected_piece, moves_to_get)

        if not self.valid_moves:
            if self.selected_piece.HasSkipped:
                INVALID_SOUND.play()
                return

            self.selected_piece.HasSkipped = False
        else:
            SELECT_SOUND.play()

    def _get_moves_of(self, piece, moves_to_get):
        """
        Gets the valid moves of the piece.
        """

        return self.board.get_valid_moves(piece, moves_to_get, self.board.IsFlipped)

    def _move_piece(self, piece, destination):
        """
        Moves a piece to the specified cell.
        """

        piece_on_destination = self.board.get_piece(destination)
        destination_cell = piece_on_destination.col, piece_on_destination.row
        col, row = destination_cell

        if piece_on_destination.color == 0 and (destination) in self.valid_moves:
            self.board.move_piece(piece, destination_cell)
            
            self.moved_piece = self.selected_piece
            skipped_list = list(self.valid_moves)

            # Get the skipped piece of the move:skipped_piece pair
            skipped_piece = self.valid_moves[destination]

            if skipped_piece:
                CAPTURE_SOUND.play()
                self.moved_piece.HasSkipped = True
                operations = []

                if len(skipped_piece) > 1:
                    for i in range(len(skipped_list)-1, (len(skipped_list)-1)-len(skipped_piece), -1):
                        operations.append(self.board.piece_landed(skipped_list[i][0], skipped_list[i][1]))
                else:
                    operations.append(self.board.piece_landed(col, row))
                self.scoreboard.score_update(self.selected_piece, skipped_piece, operations)
                
                self.board.move_to_graveyard(skipped_piece)
            else:
                MOVE_SOUND.play()

            # Check if piece had captured
            if self.selected_piece.HasSkipped:
                if self.check_for_captures(self.moved_piece):
                    self.select_piece(self.moved_piece)
                else:
                    self.moved_piece.HasSkipped = False
                    return
            else:
                self.moved_piece.HasSkipped = False
                return

        
    def draw_valid_moves(self, moves):
        color = YELLOW

        if enableMandatoryCapture:
            if self.TurnRequiresCapture:
                color = LIME

        if moves:
            for move in moves:
                col, row = move
                pygame.draw.circle(self.surface, color, (col * square_size + square_size//2, row * square_size + square_size//2), square_size*0.25)
    
    def draw_selected_piece_indicator(self, surface):
        col, row = self.board.get_col_row((self.selected_piece.col, self.selected_piece.row))

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

    def refresh(self):
        """
        Refreshes the game, removing all selections.
        """
        
        self.selected_piece = None
        self.moved_piece = None
        self.valid_moves = {}
        self.capturing_pieces.clear()

    def change_turn(self):
        if self.selected_piece:
            self.board.check_for_kings(self.selected_piece)

        self.refresh()

        if self.turn == PLAYER_ONE:
            self.turn = PLAYER_TWO
        else:
            self.turn = PLAYER_ONE

        turn_timer.reset()
        
        if enableDebugMode:
            print(f"[Debug]: Turns changed, now {self.turn}")

        if enableMandatoryCapture:
            self.check_for_captures()

    @dispatch(Piece)
    def check_for_captures(self, piece):
        """
        Checks a piece for possible captures.
        """
        
        col, row = self.board.get_col_row((piece.col, piece.row))

        if enableDebugMode:
            print(f"[Debug]: Checking for possible captures for piece ({col}, {row})...")
                 
        self.capturing_pieces.clear()
        self.board.set_all_moveables(False)

        capturing_pieces = 0
        
        if self.board.get_valid_moves(piece, "capture", self.board.IsFlipped):
            if piece.HasPossibleCapture:
                if enableDebugMode:
                    print(f"[Debug]: Possible capture by ({piece.col}, {piece.row})")
                
                piece.IsMovable = True
                self.capturing_pieces.append((col, row))
                capturing_pieces += 1

        if capturing_pieces == 0:
            if enableDebugMode:
                print(f"[Debug]: No possible captures for piece ({col}, {row})")

            self.capturing_pieces.clear()
            self.board.set_all_moveables(True)
            self.TurnRequiresCapture = False
            return self.TurnRequiresCapture
        else:
            self.TurnRequiresCapture = True
            return self.TurnRequiresCapture

    @dispatch()
    def check_for_captures(self):
        """
        Checks all pieces of the current turn for possible captures.
        """
        
        if enableDebugMode:
            print(f"[Debug]: Checking for possible captures for {self.turn}...")
            
        self.capturing_pieces.clear()
        self.board.set_all_moveables(False)

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
            return self.TurnRequiresCapture
        else:
            self.TurnRequiresCapture = True
            return self.TurnRequiresCapture