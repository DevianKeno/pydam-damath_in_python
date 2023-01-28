
import sys
import pygame
from ui_class.scene import *
from screens.select_mode import *
from objects import *
from damath.ruleset import *
from damath.piece import *
from console import *
from audio_constants import *

clock = pygame.time.Clock()

def get_cell_from_mouse(pos):
    x, y = pos
    col = (x - selection_guide_rect.w) // square_size
    row = abs(((y - selection_guide_rect.h) // square_size) - 7)

    if Options.enableDebugMode:
        print(f"[Debug/Action]: Clicked on cell ({col}, {row})")
    return col, row

def get_cell_from_mouse_raw(pos):
    """
    Returns a cell (column and row) from the board based from mouse position.
    Returns a negative value if out of bounds of the board.
    """
    x, y = pos
    col = (x - selection_guide_rect.w) // square_size
    row = (y - selection_guide_rect.h) // square_size

    if col < 0 or col > 7:
        return -1, -1
    if row < 0 or row > 7:
        return -1, -1

    if Options.enableDebugMode:
        print(f"[Debug/Action]: Clicked on cell ({col}, {row}), raw")
    return col, row


class S_Game(Scene):

    def __init__(self) -> None:
        super().__init__()
        # Scene objects
        self.Match = None
        self.Actions = None
        self.Cheats = None
        self.TurnTimer = None
        self.GlobalTimer = None

    def display(self):
        self.Match.IsRunning = True
        
        # This too
        if Rules.IsVersusAI:
            text_mode = font_cookie_run_reg.render(str(Rules.mode)+f" vs {Rules.ai}", True, OAR_BLUE)
        else:
            text_mode = font_cookie_run_reg.render(str(Rules.mode), True, OAR_BLUE)

        while self.Match.IsRunning:

            mins, secs = self.GlobalTimer.get_remaining_time()
            if self.GlobalTimer.is_running:
                timer_color = WHITE
            else:
                timer_color = LIGHT_GRAY
            self.GlobalTimer_text = font_cookie_run_reg.render(str(f'{mins:02d}:{secs:02d}'), True, timer_color)

            # change_volume(SOUND_VOLUME)
            #screen.blit(CLEAR_BG, (0, 0)) 
            screen.fill(OAR_BLUE)    
            screen.blit(side_menu_surface, (0, 0))
            side_menu_surface.fill(DARK_GRAY_BLUE)      
            
            if self.Match.check_for_winner() != None:
                print(self.Match.check_for_winner()) 
                GameIsRunning = False
                thread_running = False
                # game_ends()
                
            # Get current mouse position
            m_pos = pygame.mouse.get_pos()

            # if return_btn.top_rect.collidepoint(m_pos):
            #     return_btn.hover_update(pause, _fade=False)
            # else:
            #     return_btn.reset()

            screen.blit(game_side_surface, (0, 0))
            game_side_surface.fill(DARK_GRAY_BLUE)
            
            screen.blit(board_area_surface, (game_side_surface.get_width(), 0))
            board_area_surface.fill(OAR_BLUE)

            # damath_board_shadow.display()
            damath_board.display()

            # Render coordinates surface
            board_area_surface.blit(board_x_coords_surface, board_x_coords_rect)
            board_area_surface.blit(board_y_coords_surface, board_y_coords_rect)
            board_x_coords_surface.fill(DARK_GRAY_BLUE)
            board_y_coords_surface.fill(DARK_GRAY_BLUE)

            # Renders chips
            board_area_surface.blit(chips_surface, (tiles_rect))
            
            # Render captured pieces
            if not self.Match.Board.IsFlipped:
                board_area_surface.blit(right_captured_pieces_surface, (right_captured_pieces_rect))
                board_area_surface.blit(left_captured_pieces_surface, (left_captured_pieces_rect))
            else:
                board_area_surface.blit(right_captured_pieces_surface, (left_captured_pieces_rect))
                board_area_surface.blit(left_captured_pieces_surface, (right_captured_pieces_rect))
            right_captured_pieces_surface.fill(OAR_BLUE)
            left_captured_pieces_surface.fill(OAR_BLUE)
            
            # Display side bar elements
            mini_title.display()

            self.Match.Board.draw()

            screen.blit(text_scores,
                        (game_side_surface.get_width()//2-text_scores.get_width()//2, game_side_surface.get_height()*0.2))

            screen.blit(self.GlobalTimer_text,
                        (game_side_surface.get_width()//2-self.GlobalTimer_text.get_width()//2, game_side_surface.get_height()*0.825)) 

            screen.blit(text_mode,
                        (game_side_surface.get_width()//2-text_mode.get_width()//2, game_side_surface.get_height()*0.9))

            if Rules.allowActions:
                self.Actions.draw_menu()

            if Rules.allowCheats:
                self.Cheats.draw_menu()

                if self.Cheats.ShowEVWindow:
                    if self.Cheats.ev_window.collidepoint(m_pos):
                        self.Cheats.check_for_hover(m_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    GameIsRunning = False
                    thread_running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                        if Rules.allowCheats:
                            if self.Cheats.ShowDropdown:
                                self.Cheats.hide_menus()
                            else:
                                pause(Rules.mode)
                        else:
                            pause(Rules.mode)
                        break
                # Legacy cheat codes
                    if Rules.allowCheats:
                        _keys = pygame.key.get_pressed()
                        
                        if _keys[pygame.K_LCTRL]:

                            if _keys[pygame.K_w]: # king pieces

                                if _keys[pygame.K_1]: # blue pieces
                                    drow, dcol = get_cell_from_mouse(pygame.mouse.get_pos())
                                    piece = self.Match.Board.get_piece((drow, dcol))
                                    if dcol % 2 == 1:
                                        if drow % 2 == 1:
                                            if piece.color == RED:
                                                self.Match.Board.board[drow][dcol] = Piece(drow, dcol, LIGHT_BLUE, 100)
                                                self.Match.Board.board[drow][dcol].king = True
                                                self.Match.Board.red_left -= 1
                                                self.Match.Board.white_left += 1
                                            elif piece.color == 0:
                                                self.Match.Board.board[drow][dcol] = Piece(drow, dcol, LIGHT_BLUE, 100)
                                                self.Match.Board.board[drow][dcol].king = True
                                                self.Match.Board.white_left += 1                                 
                                    else:
                                        if drow % 2 == 0:
                                            if piece.color == RED:
                                                self.Match.Board.board[drow][dcol] = Piece(drow, dcol, LIGHT_BLUE, 100)
                                                self.Match.Board.board[drow][dcol].king = True
                                                self.Match.Board.red_left -= 1
                                                self.Match.Board.white_left += 1
                                            elif piece.color == 0:
                                                self.Match.Board.board[drow][dcol] = Piece(drow, dcol, LIGHT_BLUE, 100)
                                                self.Match.Board.board[drow][dcol].king = True
                                                self.Match.Board.white_left += 1  

                                if _keys[pygame.K_2]: # red pieces
                                    drow, dcol = get_cell_from_mouse(pygame.mouse.get_pos())
                                    piece = self.Match.Board.get_piece((drow, dcol))
                                    if dcol % 2 == 1:
                                        if drow % 2 == 1:
                                            if piece.color == LIGHT_BLUE:
                                                self.Match.Board.board[drow][dcol] = Piece(drow, dcol, RED, 100)
                                                self.Match.Board.board[drow][dcol].king = True
                                                self.Match.Board.red_left += 1
                                                self.Match.Board.white_left -= 1
                                            elif piece.color == 0:
                                                self.Match.Board.board[drow][dcol] = Piece(drow, dcol, RED, 100)
                                                self.Match.Board.board[drow][dcol].king = True
                                                self.Match.Board.red_left += 1                                 
                                    else:
                                        if drow % 2 == 0:
                                            if piece.color == LIGHT_BLUE:
                                                self.Match.Board.board[drow][dcol] = Piece(drow, dcol, RED, 100)
                                                self.Match.Board.board[drow][dcol].king = True
                                                self.Match.Board.red_left += 1
                                                self.Match.Board.white_left -= 1
                                            elif piece.color == 0:
                                                self.Match.Board.board[drow][dcol] = Piece(drow, dcol, RED, 100)
                                                self.Match.Board.board[drow][dcol].king = True
                                                self.Match.Board.red_left += 1  

                            elif _keys[pygame.K_1]: # add normal blue piece
                                drow, dcol = get_cell_from_mouse(pygame.mouse.get_pos())
                                piece = self.Match.Board.get_piece((drow, dcol))
                                if dcol % 2 == 1:
                                    if drow % 2 == 1:
                                        if piece.color == RED:
                                            self.Match.Board.board[drow][dcol] = Piece(drow, dcol, LIGHT_BLUE, 100)
                                            self.Match.Board.red_left -= 1
                                            self.Match.Board.white_left += 1
                                        elif piece.color == 0:
                                            self.Match.Board.board[drow][dcol] = Piece(drow, dcol, LIGHT_BLUE, 100)
                                            self.Match.Board.white_left += 1                                 
                                else:
                                    if drow % 2 == 0:
                                        if piece.color == RED:
                                            self.Match.Board.board[drow][dcol] = Piece(drow, dcol, LIGHT_BLUE, 100)
                                            self.Match.Board.red_left -= 1
                                            self.Match.Board.white_left += 1
                                        elif piece.color == 0:
                                            self.Match.Board.board[drow][dcol] = Piece(drow, dcol, LIGHT_BLUE, 100)
                                            self.Match.Board.white_left += 1  

                            elif _keys[pygame.K_2]: # add normal red piece
                                drow, dcol = get_cell_from_mouse(pygame.mouse.get_pos())
                                piece = self.Match.Board.get_piece((drow, dcol))
                                if dcol % 2 == 1:
                                    if drow % 2 == 1:
                                        if piece.color == LIGHT_BLUE:
                                            self.Match.Board.board[drow][dcol] = Piece(drow, dcol, RED, 100)
                                            self.Match.Board.red_left += 1
                                            self.Match.Board.white_left -= 1
                                        elif piece.color == 0:
                                            self.Match.Board.board[drow][dcol] = Piece(drow, dcol, RED, 100)
                                            self.Match.Board.red_left += 1                                 
                                else:
                                    if drow % 2 == 0:
                                        if piece.color == LIGHT_BLUE:
                                            self.Match.Board.board[drow][dcol] = Piece(drow, dcol, RED, 100)
                                            self.Match.Board.red_left += 1
                                            self.Match.Board.white_left -= 1
                                        elif piece.color == 0:
                                            self.Match.Board.board[drow][dcol] = Piece(drow, dcol, RED, 100)
                                            self.Match.Board.red_left += 1

                        if _keys[pygame.K_LSHIFT]:
                            if _keys[pygame.K_c]: # change turn
                                self.Match.change_turn()
                            if _keys[pygame.K_1]: # self.Match resets
                                self.Match.reset()
                            if _keys[pygame.K_2]: # blue wins
                                self.Match.scoreboard.p1_score = 1
                                self.Match.scoreboard.p2_score = 0
                                self.Match.Board.orange_pieces_count = 0
                            if _keys[pygame.K_3]: # red wins
                                self.Match.scoreboard.p1_score = 0
                                self.Match.scoreboard.p2_score = 1
                                self.Match.Board.blue_pieces_count = 0
                            if _keys[pygame.K_4]: # make all pieces king
                                for i in range(8):
                                    for j in range(8):
                                        self.Match.Board.board[i][j].IsKing = True
                            if _keys[pygame.K_5]: # make all pieces not king
                                for i in range(8):
                                    for j in range(8):
                                        self.Match.Board.board[i][j].IsKing = False   
                            if _keys[pygame.K_6]: # removes all pieces
                                for i in range(8):
                                    for j in range(8):
                                        self.Match.Board.board[i][j] = Piece(chips_surface, i, j, 0, 0)
                            if _keys[pygame.K_7]: # displays a single chip in both ends
                                for i in range(8):
                                    for j in range(8):
                                        self.Match.Board.board[i][j] = Piece(chips_surface, i, j, 0, 0)
                                self.Match.Board.board[0][2] = Piece(chips_surface, 0, 2, PLAYER_TWO, 2)   
                                self.Match.Board.board[7][7] = Piece(chips_surface, 7, 7, PLAYER_ONE, 2)  
                                self.Match.Board.red_left = 1
                                self.Match.Board.white_left = 1
                            if pygame.mouse.get_pressed()[2]: #removes the piece
                                drow, dcol = get_cell_from_mouse(pygame.mouse.get_pos())
                                piece = [self.Match.Board.get_piece((drow, dcol))]
                                self.Match.Board.move_to_graveyard(piece)

                        if _keys[pygame.K_m]:
                            if _keys[pygame.K_0]:
                                self.Match.set_mode('Naturals')
                            elif _keys[pygame.K_1]:
                                self.Match.set_mode('Integers')
                            elif _keys[pygame.K_2]:
                                self.Match.set_mode('Rationals')
                            elif _keys[pygame.K_3]:
                                self.Match.set_mode('Radicals')
                            elif _keys[pygame.K_4]:
                                self.Match.set_mode('Polynomials')
                    
                        if self.Cheats.IsTyping:
                            if event.key == pygame.K_RETURN:
                                print(self.Cheats.input)
                                self.Cheats.input.text = ''
                            elif event.key == pygame.K_BACKSPACE:
                                self.Cheats.input.text = self.Cheats.input.text[:-1]
                            else:
                                self.Cheats.input.text += event.unicode

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Left click
                    if pygame.mouse.get_pressed()[0]:
                        
                        if damath_board.rect.collidepoint(m_pos):
                            cell = get_cell_from_mouse_raw(m_pos)
                            col, row = cell

                            if self.Match.moved_piece != None:
                                if row != self.Match.moved_piece.row or row != self.Match.moved_piece.col:
                                    INVALID_SOUND.play()
                                
                            if Rules.allowCheats:
                                if not self.Cheats.ShowDropdown:
                                    if (-1 < row < ROWS) and (-1 < col < COLS):
                                        if Rules.IsMultiplayer:
                                            Console.listen(self.Match.select(cell))
                                        if Rules.IsVersusAI:
                                            if self.Match.turn == PLAYER_ONE:
                                                self.Match.select(cell)
                                        else:
                                            self.Match.select(cell)
                            else:
                                if (-1 < row < ROWS) and (-1 < col < COLS):
                                    if Rules.IsVersusAI:
                                        if self.Match.turn == PLAYER_ONE:
                                            self.Match.select(cell)
                                    else:
                                        self.Match.select(cell)
                                    
                        if Rules.allowActions:
                            if self.Actions.ShowDropdown:
                                if self.Actions.dropdown.window.collidepoint(m_pos):
                                    self.Actions.invoke()
                                elif self.Actions.ShowFFWindow or self.Actions.ShowODWindow:
                                    if self.Actions.confirmation_window.collidepoint(m_pos):
                                        x, y = event.pos
                                        # btn_selected(x, y, btn_list=[actions.button_ff_yes, actions.button_no, actions.button_od_yes])
                                    else:
                                        self.Actions.hide_menus()
                                else:
                                    self.Actions.hide_menus()

                        if Rules.allowCheats:
                            if self.Cheats.ShowDropdown:
                                if self.Cheats.dropdown.window.collidepoint(m_pos) and not self.Cheats.ShowEVWindow:
                                    self.Cheats.invoke()
                                elif self.Cheats.ShowEVWindow:
                                    if self.Cheats.ev_window.collidepoint(m_pos):
                                        # Clicked on "Done"
                                        if self.Cheats.selected_done == 1:
                                            self.Cheats.invoke()
                                            self.Cheats.hide_menus()
                                        
                                        # Clicked on text box
                                        if self.Cheats.text_box_rect.collidepoint(m_pos):
                                            self.Cheats.IsTyping = True
                                            self.Cheats.input_box.clear()
                                    else:
                                        self.Cheats.hide_menus()
                                else:
                                    self.Cheats.IsTyping = False
                                    self.Cheats.hide_menus()
                                
                    # Right click
                    if pygame.mouse.get_pressed()[2]:
                        if Rules.allowCheats:
                            cell = get_cell_from_mouse_raw(m_pos)
                            col, row = cell

                            if not self.Cheats.ShowEVWindow:
                                self.Cheats.select(cell)

                                if (-1 < row < ROWS) and (-1 < col < COLS):
                                    self.Cheats.create_dropdown(m_pos)
                                    self.Actions.hide_menus()
                                else:
                                    if not game_side_surface.get_rect().collidepoint(m_pos):
                                        self.Cheats.create_dropdown(m_pos, OnBoard=False)
                                        self.Actions.hide_menus()
                                    else:
                                        self.Actions.create_dropdown(m_pos)
                                        self.Cheats.hide_menus()

            screen.blit(CURSOR, pygame.mouse.get_pos())
            self.Match.update()
            pygame.display.update()
            clock.tick(FPS)

            
GameScene = S_Game()