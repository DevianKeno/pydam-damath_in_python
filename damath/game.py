import pygame
import random
import time
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

    def __init__(self, surface, board, scoreboard, theme):
        self.surface = surface
        self.board = board
        self.scoreboard = scoreboard
        self.theme = theme
        self.selected_cell = None   # Cell | Raw cell
        self.selected_tile = None   # Tile | Cell relative to board's coordinates

    def _init(self):
        self.game_evaluation = 0
        self.moved_piece = None
        self.selected_piece = None
        self.board = Board(self.surface, self.theme) # for game reset
        self.capturing_pieces = []
        self.valid_moves = {}
        self.TurnRequiresCapture = False
        self.turn = PLAYER_ONE
        self.movables = {}
        self.evaluate()

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

    def evaluate(self):
        
        # this function only works in Naturals and Integers for now
        
        p1_eval = self.scoreboard.p1_score
        p2_eval = self.scoreboard.p2_score

        # get the values of all the remaining pieces on the board
        for r in range(ROWS):
            for c in range(COLS):
                piece = self.board.get_piece((self.board.get_col_row((r, c))))
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
        
        if enableDebugMode:
            print(f"[Evaluation] Game Value: {self.game_evaluation}")
        self.get_all_possible_moves()

    def get_all_possible_moves(self):

        self.movables = {}

        for r in range(ROWS):
            for c in range(COLS):
                piece = self.board.get_piece((c, r))
                if piece.color == self.turn:
                    _move = self._get_moves_of(piece, "all")
                    #print(_move)
                    if self.TurnRequiresCapture:
                        moves = list(self._get_moves_of(piece, "capture").keys())
                    else:
                        moves = list(self._get_moves_of(piece, "all").keys())
                    
                    if moves:
                        self.movables[piece] = moves
        
        #BUG: Bug in some king pieces where no valid moves are returned on first click,
        #     causing the function to fail to count those moves, and will only do so 
        #     after the player reselects the affected king piece
        piece_movables = list(self.movables.keys())
        valid_moves = []
        for move in list(self.movables.values()):
            valid_moves.extend(move)

        if enableDebugMode:
            print(f"[Evaluation] Number of valid moves: {len(valid_moves)}")
            print(f"[Evaluation] Number of movables pieces: {len(piece_movables)}")

    def select(self, cell):
        """
        Selects a cell or move given raw cell arguments.
        """
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
            self.select_move(cell)
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
            self._move_piece(self.selected_piece, cell)
        else:
            self.selected_piece = None

    def select_piece(self, piece):
        """
        Selects a piece, given a piece object.
        """
        
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
        
        col, row  = piece.col, piece.row

        self.valid_moves = self._get_moves_of(self.selected_piece, moves_to_get)

        if not self.valid_moves:
            if not self.board.piece_had_skipped(self.selected_piece, col, row):
                INVALID_SOUND.play()
                return

            self.board.piece_skipped(self.selected_piece, col, row, bool=False)
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
                self.board.piece_skipped(self.selected_piece, col, row, bool=True)
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
                    if versusAI:
                        self.versus_ai()
                else:
                    self.change_turn()
            else:
                self.board.piece_skipped(self.selected_piece, col, row, bool=False)
                self.change_turn()
        
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

        self.evaluate()
        if versusAI:
            self.versus_ai()

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

    def versus_ai(self):
        
        # her name is Xena
        
        #TODO: create a more complex algorithm to choose the best possible move for the player
        #           - making a move that will result to a positive score for the AI
        #           - making a move that will result to a negative score for the opponent
        #           - making a move that will lead the chips to promotion
        #           - making a move that will quickly end the game if the AI's score is significantly
        #               bigger than the opponent's

        if self.turn == PLAYER_TWO:
            
            self.get_all_possible_moves()

            random_piece_num = random.randint(0, len(list(self.movables.keys()))-1)
            chosen_piece = list(self.movables.keys())[random_piece_num]

            random_move_num = random.randint(0, len(list(self.movables.get(chosen_piece)))-1)
            chosen_move = list(self.movables.get(chosen_piece))[random_move_num]

            if not self.moved_piece:
                self.selected_piece = chosen_piece
                self.select_piece(self.selected_piece)
                if self.selected_piece:
                    self.select_move(chosen_move)
            else:
                self.select_move(chosen_move)
            mcol, mrow = self.board.get_col_row(chosen_move)
            print(f"[AI Xena] Xena moved {chosen_piece} ({chosen_piece.number}) to {(mcol, mrow)}")