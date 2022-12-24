import pygame
from .board import Board
from .constants import ROWS, COLS, RED, LIGHT_BLUE, YELLOW, LIME, WHITE, SQUARE_SIZE, OFFSET, BOARD_OFFSET, BOARD_WIDTH, BOARD_HEIGHT
from audio_constants import *
from ui_class.tween import *
from objects import SQUARE_SIZE

pygame.mixer.init()

MANDATORY_CAPTURE = True

class Game:

    def __init__(self, surface, scoreboard, theme):
        self.surface = surface
        self.theme = theme
        self.moved_piece = None
        self.selected = None
        self.board = Board(self.surface, self.theme)
        self.moveable_pieces = list(self.board.moveables)
        self.scoreboard = scoreboard
        self.RequiresCapture = False
        self.turn = RED
        self.valid_moves = {}

    def update(self):
        self.board.draw_contents(self.surface)
        self.draw_indicators(self.surface)
        self.board.draw_chips(self.surface)
        self.scoreboard.update(self.turn)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update() 
    
    def draw_indicators(self, surface):
        if self.selected:
            piece = self.selected
            selected_piece_rect = pygame.Rect((piece.col*SQUARE_SIZE, piece.row*SQUARE_SIZE), (SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(surface, YELLOW, selected_piece_rect)
        
        if MANDATORY_CAPTURE:
            if self.RequiresCapture:
                for i in range(len(self.moveable_pieces)):
                    capturing_pieces_rect = []
                    capturing_piece_rect = pygame.Rect((self.moveable_pieces[i][1]*SQUARE_SIZE, self.moveable_pieces[i][0]*SQUARE_SIZE), (SQUARE_SIZE, SQUARE_SIZE))   
                    capturing_pieces_rect.append(capturing_piece_rect)
                    pygame.draw.rect(surface, LIME, capturing_piece_rect)

    def winner(self):   
        if (self.board.red_left <=0 or self.board.white_left <= 0):
            red_score, blue_score = self.scoreboard.score()
            if red_score > blue_score:
                return RED
            elif blue_score > red_score:
                return LIGHT_BLUE
            else:
                return "TIE"
        return None

    def reset(self):
        self.scoreboard.reset()
        # self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                #INVALID_SOUND.play()
                self.selected = None
                self.select(row, col)

        if self.moved_piece == None:
            piece = self.board.get_piece(row, col)
        else:
            piece = self.moved_piece

        if piece.color != 0 and piece.color == self.turn:
            get_moves = "both"
            if MANDATORY_CAPTURE:
                if not (piece.row, piece.col) in self.moveable_pieces:
                    return False
                if self.RequiresCapture:
                    get_moves = "capture"

            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece, get_moves)

            if not self.valid_moves:
                if not self.board.piece_had_skipped(self.selected, row, col):
                    INVALID_SOUND.play()
                    return False
                self.board.piece_skipped(self.selected, row, col, bool=False)
                self.change_turn()
            else:
                SELECT_SOUND.play()
            return True

        elif self.moved_piece == None and not self.selected and (piece.color == 0 or piece.color != self.turn):
            INVALID_SOUND.play()

        return False

    def _move(self, row, col):

        piece = self.board.get_piece(row, col) #(color):number

        if self.selected and piece.color == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col, piece.number)
            self.moveable_pieces.append((row, col))
            self.moved_piece = self.board.get_piece(row, col)
            skipped_list = list(self.valid_moves)
            skipped = self.valid_moves[(row, col)] 

            if skipped:
                CAPTURE_SOUND.play()
                self.board.piece_skipped(self.selected, row, col, bool=True)
                operations = []
                if len(skipped) > 1:
                    for i in range(len(skipped_list)-1, (len(skipped_list)-1)-len(skipped), -1):
                        operations.append(self.board.piece_landed(skipped_list[i][0], skipped_list[i][1]))
                else:
                    operations.append(self.board.piece_landed(row, col))
                self.scoreboard.score_update(self.selected.color, self.selected, skipped, operations)
                self.board.remove(skipped)
            else:
                MOVE_SOUND.play()

            if not self.board.piece_had_skipped(self.selected, row, col):
                self.board.piece_skipped(self.selected, row, col, bool=False)
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
                    row, col = move
                    pygame.draw.circle(self.surface, color, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), SQUARE_SIZE*0.25)

    def change_turn(self):
        print("Changed turns")
        self.moved_piece = None
        self.valid_moves = {}

        if self.turn == RED:
            self.turn = LIGHT_BLUE
        else:
            self.turn = RED

        if MANDATORY_CAPTURE:
            self.moveable_pieces.clear()
            self.moveable_pieces = self.check_for_captures()

    def check_for_captures(self):
        print(self.board.moveables)
        print(f"Checking for possible captures for {self.turn}")
        red_count = self.board.red_left + self.board.red_kings
        blue_count = self.board.white_left + self.board.white_kings
        moveables = []
        capturing_pieces = 0
        
        for row in range(ROWS-1):
            if red_count == 0 or blue_count == 0:
                break

            for col in range(7):
                if str(self.board.board[row][col]).strip(" ") == str(self.turn).strip(" "):
                    piece = self.board.get_piece(row, col)

                    if self.board.get_valid_moves(piece, "capture"):
                        if self.board.has_possible_capture(piece):
                            print(f"Possible capture by {row}, {col}")
                            moveables.append((piece.row, piece.col))
                            capturing_pieces += 1

                    if self.turn == RED:
                        red_count -= 1
                    else:
                        blue_count -= 1

        if capturing_pieces == 0:
            print(f"No possible captures for {self.turn}")
            self.RequiresCapture = False
            return self.board.moveables.copy()
        self.RequiresCapture = True
        return moveables

    def reset_moveables(self):
        self.moveable_pieces = self.board.all_moveables