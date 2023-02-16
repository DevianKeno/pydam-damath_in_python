import pygame
import random
import time
from multipledispatch import dispatch
from .board import Board
from .piece import Piece
from .ruleset import Rules
from .scoreboard import Scoreboard
from .constants import *
from .timer import *
from .statistics import *
from audio_constants import *
from ui_class.tween import *
from objects import square_size
from options import *
from .minimax import minimax

pygame.mixer.init()

class Match:
    """
    An instance of a game match.
    """

    def __init__(self, surface=None, board=None, scoreboard=None, IsMultiplayer=False):
        self._surface = surface
        self.Board = board
        self.Scores = scoreboard
        self.ControlsIsEnabled = True
        self.IsRunning = False
        self._console = None
        

    def init(self):
        """
        Initialize match.
        """

        # --- FOR GAME RESET ---
        self.symbols = self.Board.Symbols
        self.Board = Board(self._surface)
        self.Board.Symbols = self.symbols
        self.Board.init()
        
        self.command = None
        self.selected_cell = None   # Cell | Raw cell
        self.selected_tile = None   # Tile | Relative to board's coordinates
        self.selected_piece = None
        self.moved_piece = None

        self.movables = {}
        self.valid_moves = {}
        self.game_evaluation = 0

        self.turn = PLAYER_ONE
        self.ControlsIsEnabled = True
        self.DrawIndicators = True
        self.TurnRequiresCapture = False

    @property
    def Surface(self):
        return self._surface

    @Surface.setter
    def Surface(self, value: pygame.Surface):
        self._surface = value

    def set_mode(self, mode):
        Rules.set_mode("Classic")

    def draw(self):
        self.Scores.draw_scores()
        self.Scores.draw_turn_indicator(self.turn)

    def reset(self):
        self.Scores.reset()
        self.init()
        turn_timer.stop()
        global_timer.stop()

    def evaluate(self):
        
        # this function only works in Naturals and Integers for now
        
        p1_eval = self.Scores.p1_score
        p2_eval = self.Scores.p2_score

        # get the values of all the remaining pieces on the board
        for r in range(ROWS):
            for c in range(COLS):
                piece = self.Board.get_piece((self.Board.get_col_row((r, c))))
                if piece.color != 0:
                    if piece.color == PLAYER_ONE:
                        if piece.IsKing:
                            p1_eval+=int(piece.number * 2)
                        p1_eval+=int(piece.number)
                    else:
                        if piece.IsKing:
                            p2_eval+=int(piece.number * 2)
                        p2_eval+=int(piece.number)

        # positive game evaluation value means PLAYER_ONE (Blue) is winning
        self.game_evaluation = p1_eval - p2_eval
        
        if Options.enableDebugMode:
            print(f"[Evaluation] Game Value: {self.game_evaluation}")
        self.get_all_possible_moves(self.Board.pieces, self.turn)

    def get_all_possible_moves(self, board: list, turn):
        """
        board argument needs the 2D array representation of the board and not the object 
        """
        self.movables = {}

        for r in range(ROWS):
            for c in range(COLS):
                piece = board[c][r]
                if piece.color == turn:
                    _move = self._get_moves_of(piece, "all")
                    #print(_move)
                    if self.TurnRequiresCapture:
                        moves = self._get_moves_of(piece, "capture")
                    else:
                        moves = self._get_moves_of(piece, "all")

                    # print(self._get_moves_of(piece, "all"))
                    
                    if moves:
                        self.movables[piece] = moves
        
        piece_movables = list(self.movables.keys())
        valid_moves = []
        for move in list(self.movables.values()):
            valid_moves.extend(move)

        if Options.enableDebugMode:
            print(f"[Evaluation] Number of valid moves: {len(valid_moves)}")
            print(f"[Evaluation] Number of movables pieces: {len(piece_movables)}")

        return self.movables

    def select(self, cell, IsOperator=False):
        """
        Selects a cell or move given raw cell arguments.
        """

        if IsOperator:
            if self.selected_piece:
                self.select_move(cell)
                return
            else:
                self.select_piece(self.Board.get_piece(cell), IsOperator)
                return

        if Rules.IsMultiplayer:
            if not self.ControlsIsEnabled:
                return
        
        # Cell = raw coordinates
        self.selected_cell = cell
        # Tile = cell relative to the board's coordinates, regardless of orientation
        self.selected_tile = self.Board.get_col_row(cell)

        piece_to_select = self.Board.get_piece(cell)

        # If a piece had already captured, you can only select that piece
        if self.moved_piece:
            if piece_to_select == self.moved_piece:
                piece_to_select = self.moved_piece

        # Handles selection of pieces
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
        
        if (cell) in self.valid_moves:
            # Send to console
            if Rules.IsMultiplayer:
                if self.Board.IsFlipped:
                    col, row = self.Board.to_raw(cell)
                    piece_col, piece_row = self.Board.get_abs((self.selected_piece.col, self.selected_piece.row))
                else:
                    col, row = self.Board.get_col_row(cell)
                    piece_col, piece_row = self.selected_piece.col, self.selected_piece.row
                self.command = "sm {} {} {} {}".format(piece_col, piece_row, col, row)

            self._move_piece(self.selected_piece, cell)

            if not self.selected_piece.HasPossibleCapture:
                self.change_turn()
            else:
                if Rules.ai:
                    self.versus_ai()

            return self.command
        else:
            self.refresh()

    def select_piece(self, piece, IsOperator=False):
        """
        Selects a piece, given a piece object.
        """
        
        if not IsOperator:
            if piece.color != self.turn:
                self.refresh()
                return

        self.selected_piece = piece

        if Options.enableDebugMode:
            print(f"[Debug]: Selected piece ({self.selected_piece.col}, {self.selected_piece.row})")

        # Get moves
        moves_to_get = "all"
        
        if Rules.allowMandatoryCapture:
            if not self.selected_piece.IsMovable:
                return

            if self.TurnRequiresCapture:
                moves_to_get = "capture"

        self.valid_moves = self._get_moves_of(self.selected_piece, moves_to_get)

        if not self.valid_moves:
            if self.selected_piece.HasSkipped:
                return
            self.selected_piece.HasSkipped = False
        else:
            self.Board.selected_piece = self.selected_piece
            self.Board.valid_moves = self.valid_moves
            SELECT_SOUND.play()

    def _get_moves_of(self, piece, moves_to_get):
        """
        Gets the valid moves of the piece.
        """
        return self.Board.get_valid_moves(piece, moves_to_get, self.Board.IsFlipped)

    def _move_piece(self, piece, destination):
        """
        Moves a piece to the specified cell.
        """

        piece_on_destination = self.Board.get_piece(destination)
        destination_cell = piece_on_destination.col, piece_on_destination.row

        if piece_on_destination.color == 0 and (destination) in self.valid_moves:
            self.Board.move_piece(piece, destination_cell)
            self.moved_piece = self.selected_piece
            skipped_piece = self.valid_moves[destination] # Get the skipped piece of key:piece value pair

            if skipped_piece:
                CAPTURE_SOUND.play()
                self.moved_piece.HasSkipped = True

                if self.Board != None:
                    self.Board.move_to_graveyard(skipped_piece)
                    operation = self.Board.Symbols.get_symbol(destination_cell)

                if self.Scores != None:
                    self.Scores.score_update(self.selected_piece, skipped_piece, operation)
            else:
                MOVE_SOUND.play()

            # Check if piece had captured
            if self.selected_piece.HasSkipped:
                if self.check_for_captures(self.moved_piece):
                    self.select_piece(self.moved_piece)
            self.moved_piece.HasSkipped = False
            return

    def toggle_player_controls(self):
        self.ControlsIsEnabled = not self.ControlsIsEnabled

    def toggle_indicators(self):
        self.DrawIndicators = not self.DrawIndicators

    def refresh(self):
        """
        Refreshes the game, removing all selections.
        """
        self.selected_piece = None
        self.moved_piece = None
        self.valid_moves = {}

        if self.Board != None:
            self.Board.refresh()

    def change_turn(self):
        if Rules.IsMultiplayer:
            self.toggle_player_controls()
        if self.selected_piece:
            self.Board.check_for_kings(self.selected_piece)

        self.refresh()

        if self.turn == PLAYER_ONE:
            self.turn = PLAYER_TWO
        else:
            self.turn = PLAYER_ONE

        turn_timer.reset()
        
        if Options.enableDebugMode:
            print(f"[Debug]: Turns changed, now {self.turn}")

        if Rules.allowMandatoryCapture:
            self.check_for_captures()

        self.evaluate()
        if Rules.ai:
            self.versus_ai()

    @dispatch(Piece)
    def check_for_captures(self, piece):
        """
        Checks a piece for possible captures.
        """
        
        col, row = self.Board.get_col_row((piece.col, piece.row))

        if Options.enableDebugMode:
            print(f"[Debug]: Checking for possible captures for piece ({col}, {row})...")
                 
        self.Board.capturing_pieces.clear()
        self.Board.set_all_moveables(False)

        capturing_pieces = 0
        
        if self.Board.get_valid_moves(piece, "capture", self.Board.IsFlipped):
            if piece.HasPossibleCapture:
                if Options.enableDebugMode:
                    print(f"[Debug]: Possible capture by ({piece.col}, {piece.row})")
                
                piece.IsMovable = True
                self.Board.capturing_pieces.append((col, row))
                capturing_pieces += 1

        if capturing_pieces == 0:
            if Options.enableDebugMode:
                print(f"[Debug]: No possible captures for piece ({col}, {row})")

            self.Board.capturing_pieces.clear()
            self.Board.set_all_moveables(True)
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
        
        if Options.enableDebugMode:
            print(f"[Debug]: Checking for possible captures for {self.turn}...")
            
        self.Board.capturing_pieces.clear()
        self.Board.set_all_moveables(False)

        blue_count = self.Board.blue_pieces_count + self.Board.blue_kings
        orange_count = self.Board.orange_pieces_count + self.Board.orange_kings
        capturing_pieces = 0
        
        for row in range(ROWS):
            if blue_count == 0 or orange_count == 0:
                break

            for col in range(COLS):
                if blue_count == 0 or orange_count == 0:
                    break
                
                piece = self.Board.get_piece((col, row))
                
                if piece.color == self.turn:
                    if self.Board.get_valid_moves(piece, "capture", self.Board.IsFlipped):
                        if piece.HasPossibleCapture:
                            if Options.enableDebugMode:
                                print(f"[Debug]: Possible capture by ({col}, {row})")
                            
                            piece.IsMovable = True
                            self.Board.capturing_pieces.append((col, row))
                            capturing_pieces += 1

                    if self.turn == PLAYER_ONE:
                        blue_count -= 1
                    else:
                        orange_count -= 1

        if capturing_pieces == 0:
            if Options.enableDebugMode:
                print(f"[Debug]: No possible captures for {self.turn}")

            self.Board.capturing_pieces.clear()
            self.Board.set_all_moveables(True)
            self.TurnRequiresCapture = False
            return self.TurnRequiresCapture
        else:
            self.TurnRequiresCapture = True
            return self.TurnRequiresCapture

    def check_for_winner(self):   
        if (self.Board.blue_pieces_count <= 0 or self.Board.orange_pieces_count <= 0 or global_timer.get_remaining_time() == (-1, 59)):
            p1, p2 = self.Scores.get_scores()

            if p2 > p1:
                return PLAYER_TWO 
            if p1 > p2:
                return PLAYER_ONE
            return "TIE"
        return None

    def ai_move(self, piece, move):
        
        self.get_all_possible_moves(self.Board.pieces, self.turn)
        
        if not self.moved_piece:
            self.select(self.Board.get_col_row(piece.cell))

            if self.selected_piece:
                self.select_move(move)
        else:
            self.selected_piece = self.Board.get_piece(self.Board.get_col_row((piece.cell)))
            self.select_move(move)

        mcol, mrow = self.Board.get_col_row(move)
        print(f"[AI Xena] Xena moved {piece} ({piece.number}) to {(mcol, mrow)}") 
        
    def versus_ai(self):

        # her name is Xena
        
        #TODO: create a more complex algorithm to choose the best possible move for the player
        #           - ✓ making a move that will result to a positive score for the AI
        #           - ✓ making a move that will result to a negative score for the opponent
        #           - ✓ making a move that will lead the chips to promotion 
        #           - making a move that will quickly end the game if the AI's score is significantly
        #               bigger than the opponent's

        if self.turn == PLAYER_TWO and self.check_for_winner() == None:
            # this will occassionally throw an error if the bug persists 
            # (no valid moves are returned on first click)
            res = minimax(self, self.Board.pieces, 1, self.Scores.p1_score, self.Scores.p2_score, False, None)
            chosen_piece = res[1][0]
            chosen_move = self.Board.get_col_row(res[1][1])
            self.ai_move(chosen_piece, chosen_move)
