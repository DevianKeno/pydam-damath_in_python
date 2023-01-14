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

    def _init(self):
        self.moved_piece = None
        self.selected = None
        self.board = Board(self.surface, self.theme) # for game reset
        self.moveable_pieces = list(self.board.moveables)
        self.valid_moves = {}
        self.RequiresCapture = False
        self.turn = PLAYER_ONE

    def set_mode(self, mode):
        Piece.mode = mode
        Scoreboard.mode = mode
        self.board.set_mode(mode)

    def update(self):
        if self.board.anim:
            self.board.anim.update()
        if self.board.anim_capture:
            self.board.anim_capture.update()
        self.board.draw_contents(self.surface)
        self.draw_indicators(self.surface)
        self.board.draw_chips(self.surface)
        self.scoreboard.draw_scores()
        self.scoreboard.draw_turn_indicator(self.turn)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update() 
    
    def draw_indicators(self, surface):
        if self.selected:
            piece = self.selected
            selected_piece_rect = pygame.Rect((piece.col*square_size, abs(piece.row-7)*square_size), (square_size, square_size))
            pygame.draw.rect(surface, YELLOW, selected_piece_rect)
        
        if MANDATORY_CAPTURE:
            if self.RequiresCapture:
                for i in range(len(self.moveable_pieces)):
                    capturing_pieces_rect = []
                    capturing_piece_rect = pygame.Rect((self.moveable_pieces[i][0]*square_size, abs(self.moveable_pieces[i][1]-7)*square_size), (square_size, square_size))   
                    capturing_pieces_rect.append(capturing_piece_rect)
                    pygame.draw.rect(surface, LIME, capturing_piece_rect)

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
        
    def select(self, col, row):
        if self.selected:
            result = self._move(col, row)

            if not result:
                self.selected = None
                self.select(col, row)

        if self.moved_piece == None:
            piece = self.board.get_piece(col, row)
        else:
            piece = self.moved_piece

        if piece.color != 0 and piece.color == self.turn:
            get_moves = "all"

            if MANDATORY_CAPTURE:
                if not (piece.col, piece.row) in self.moveable_pieces:
                    return False
                if self.RequiresCapture:
                    get_moves = "capture"

            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece, get_moves)

            if not self.valid_moves:
                if not self.board.piece_had_skipped(self.selected, col, row):
                    INVALID_SOUND.play()
                    return False

                self.board.check_for_kings(self.selected)
                self.board.piece_skipped(self.selected, col, row, bool=False)
                self.change_turn()
            else:
                SELECT_SOUND.play()
            return True

        elif self.moved_piece == None and not self.selected and (piece.color == 0 or piece.color != self.turn):
            INVALID_SOUND.play()

        return False

    def _move(self, col, row):

        piece = self.board.get_piece(col, row) #(color):number

        if self.selected and piece.color == 0 and (col, row) in self.valid_moves:
            self.board.move(self.selected, col, row, piece.number)
            self.moveable_pieces.append((col, row))
            self.moved_piece = self.board.get_piece(col, row)
            skipped_list = list(self.valid_moves)
            skipped = self.valid_moves[(col, row)] 

            if skipped:
                CAPTURE_SOUND.play()
                self.board.piece_skipped(self.selected, col, row, bool=True)
                operations = []
                if len(skipped) > 1:
                    for i in range(len(skipped_list)-1, (len(skipped_list)-1)-len(skipped), -1):
                        operations.append(self.board.piece_landed(skipped_list[i][0], skipped_list[i][1]))
                else:
                    operations.append(self.board.piece_landed(col, row))
                self.scoreboard.score_update(self.selected.color, self.selected, skipped, operations)
                
                self.board.move_to_graveyard(skipped)
            else:
                MOVE_SOUND.play()

            if not self.board.piece_had_skipped(self.selected, col, row):
                self.board.piece_skipped(self.selected, col, row, bool=False)
                self.board.check_for_kings(self.selected)
                self.change_turn()
        else:
            self.selected = None
            return False
        self.selected = None
        return True
        
    def draw_valid_moves(self, moves):
        if self.selected:
            color = YELLOW
            if self.RequiresCapture:
                color = LIME
            if moves:
                for move in moves:
                    col, row = move
                    pygame.draw.circle(self.surface, color, (col * square_size + square_size//2, abs(row-7) * square_size + square_size//2), square_size*0.25)

    def change_turn(self):
        self.moved_piece = None
        self.valid_moves = {}

        if self.turn == PLAYER_ONE:
            self.turn = PLAYER_TWO
        else:
            self.turn = PLAYER_ONE

        turn_timer.reset()
        
        if enableDebugMode:
            print(f"[Debug]: Turns changed, now {self.turn}")

        if MANDATORY_CAPTURE:
            self.moveable_pieces.clear()
            self.moveable_pieces = self.check_for_captures()

    def check_for_captures(self):
        if enableDebugMode:
            print(f"[Debug]: Checking for possible captures for {self.turn}...")

        _blue_count = self.board.blue_pieces_count + self.board.blue_kings
        _orange_count = self.board.orange_pieces_count + self.board.orange_kings
        moveables = []
        capturing_pieces = 0
        
        for row in range(ROWS):
            if _blue_count == 0 or _orange_count == 0:
                break

            for col in range(COLS):
                if self.board.board[col][row].color == self.turn:
                    piece = self.board.get_piece(col, row)

                    if self.board.get_valid_moves(piece, "capture"):
                        if self.board.has_possible_capture(piece):
                            if enableDebugMode:
                                print(f"[Debug]: Possible capture by ({col}, {row})")
                            moveables.append((piece.col, piece.row))
                            capturing_pieces += 1
                    if self.turn == PLAYER_ONE:
                        _blue_count -= 1
                    else:
                        _orange_count -= 1

        if capturing_pieces == 0:
            if enableDebugMode:
                print(f"[Debug]: No possible captures for {self.turn}")
            self.RequiresCapture = False
            return self.board.moveables.copy()
        self.RequiresCapture = True
        return moveables

    def reset_moveables(self):
        self.moveable_pieces = self.board.all_moveables