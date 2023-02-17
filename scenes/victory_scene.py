
from ui_class.scene import *
from ui_class.text import *
from objects import *
from ui_class.tween import *

class S_Win(Scene):

    def __init__(self) -> None:
        super().__init__()
        self.name = "Victory Scene"
        self.description = """A player has won."""
        # Scene objects
        self.Match = None
        ## Text elements
        self.victory_message = None
        self.win_condition = None
        self.anim_window_pop_up = None
        self.IsOnTop = True
        self.btn_group = ButtonGroup([restart_btn, main_menu_btn], 1, True)
        self.blue_chip =  None
        self.orange_chip = None
        self.victory_color = None

    @property
    def scores(self) -> tuple:
        return self.Match.Scores.get_scores()

    @property
    def btn_position(self) -> tuple:

        return [(victory_window.x + victory_window.width / 2.1 - restart_btn.width, victory_window.y + victory_window.height*0.82), 
                (victory_window.x + victory_window.width / 1.9, victory_window.y + victory_window.height*0.82)]
        
    def on_entry(self):

        victory_window.wupdate(x = (SCREEN_WIDTH * 0.5) - (victory_window.width * 0.5), 
                               y = (SCREEN_HEIGHT * 0.5) - (victory_window.h * 0.5))

        victory_inner_pane.wupdate(x = (SCREEN_WIDTH * 0.5) - (victory_inner_pane.width * 0.5), 
                               y = (SCREEN_HEIGHT * 0.5) - (victory_inner_pane.h * 0.45))
    

        self.victory_message = Text(screen, CookieRun_Regular, victory_window.h * 0.1, WHITE)
        self.win_condition = Text(screen, CookieRun_Regular, victory_window.h * 0.05, OAR_BLUE)

        self.p1_score = Text(screen, CookieRun_Regular, victory_window.h * 0.12, WHITE, None)
        self.p2_score = Text(screen, CookieRun_Regular, victory_window.h * 0.12, WHITE, None)

        self.p1_score_lead = Text(screen, CookieRun_Regular, victory_window.h * 0.075, WHITE, None)
        self.p2_score_lead = Text(screen, CookieRun_Regular, victory_window.h * 0.075, WHITE, None)

        self.p1_lead = round(round(self.scores[0], 2) - round(self.scores[1], 2), 2)
        self.p2_lead = round(round(self.scores[1], 2) - round(self.scores[0], 2), 2)
    
        if self.p1_lead > self.p2_lead:
            self.p2_score_lead.change_color((128, 0, 0))
            self.p1_score_lead.change_color((0, 128, 0))
            victory_window.color = DARK_BLUE
            victory_inner_pane.color = OAR_BLUE
            self.win_condition.color = OAR_BLUE
            restart_btn.set_color(rect_color=TEAL, shadow_rect_color=DARKER_TEAL, 
                        hover_color=resume_btn.hover_color, shadow_hover_color=resume_btn.shadow_hovered_color)
            main_menu_btn.set_color(rect_color=TEAL, shadow_rect_color=DARKER_TEAL, 
                        hover_color=resume_btn.hover_color, shadow_hover_color=resume_btn.shadow_hovered_color)
        
        elif self.p2_lead > self.p1_lead:
            self.p1_score_lead.change_color((128, 0, 0))
            self.p2_score_lead.change_color((0, 128, 0))
            victory_window.color = PERSIMMON_ORANGE
            victory_inner_pane.color = "#CE492D"
            self.win_condition.color = DARK_ORANGE
            restart_btn.set_color(rect_color=DARK_ORANGE, shadow_rect_color="#7E2A1A", 
                        hover_color="#B23B24", shadow_hover_color="#9E3621")
            main_menu_btn.set_color(rect_color=DARK_ORANGE, shadow_rect_color="#7E2A1A", 
                        hover_color="#B23B24", shadow_hover_color="#9E3621")
        else:
            self.p1_score_lead.change_color((255, 255, 255))
            self.p2_score_lead.change_color((255, 255, 255))
            victory_window.color = DARK_BLUE
            victory_inner_pane.color = OAR_BLUE
            self.win_condition.color = OAR_BLUE
            restart_btn.set_color(rect_color=TEAL, shadow_rect_color=DARKER_TEAL, 
                        hover_color=resume_btn.hover_color, shadow_hover_color=resume_btn.shadow_hovered_color)
            main_menu_btn.set_color(rect_color=TEAL, shadow_rect_color=DARKER_TEAL, 
                        hover_color=resume_btn.hover_color, shadow_hover_color=resume_btn.shadow_hovered_color)

        self.p1_score.text = str(round(self.scores[0], 2))
        self.p2_score.text = str(round(self.scores[1], 2))

        self.p1_score_lead.text = str(self.p1_lead)
        self.p2_score_lead.text = str(self.p2_lead)
        
        game_result = str(self.Match.check_for_winner())

        if game_result == "None":
            self.victory_message.text = "Ongoing Match"
        elif game_result == "TIE":
            self.victory_message.text = "Draw!"
        else:
            self.victory_message.text = game_result + " Victory!"
        
        # self.victory_message.text = "Victory!"
        self.victory_message.pos = ((victory_window.x + victory_window.w // 2),
                                (victory_window.y + victory_window.h * 0.1))

        self.win_condition.text = "Captured all opponents pieces"
        self.win_condition.pos = ((victory_window.x + victory_window.w // 2),
                                (victory_window.y + victory_window.h * 0.2))

        self.blue_chip = Image(BLUE_PIECE, self.surface,
                           (victory_window.x + victory_window.width / 1.85 - restart_btn.width, 
                           victory_inner_pane.y + victory_inner_pane.height * 0.25),
                           (self.surface.get_width()*0.06, self.surface.get_width()*0.068))

        self.orange_chip = Image(ORANGE_PIECE, self.surface,
                           (victory_window.x + victory_window.width / 1.85 - restart_btn.width, 
                           victory_inner_pane.y + victory_inner_pane.height * 0.75),
                           (self.surface.get_width()*0.06, self.surface.get_width()*0.068))

        self.p1_score.pos = self.blue_chip.x + self.blue_chip.w * 1.35, self.blue_chip.get_rect().y + self.blue_chip.h/2 - self.p1_score.rect.h/2
        self.p2_score.pos = self.orange_chip.x + self.orange_chip.w * 1.35, self.orange_chip.get_rect().y + self.orange_chip.h/2 - self.p2_score.rect.h/2
    
    def _draw_buttons(self):
        self.btn_group.draw(self.btn_position)

    def display(self):
        victory_window.draw()
        victory_inner_pane.draw()

        self._draw_buttons()
        self.blue_chip.display()
        self.orange_chip.display()
        self.p1_score.draw()
        self.p2_score.draw()

        self.p1_score_lead.pos = self.p1_score.pos[0] + self.p1_score.rect.w + 10, self.blue_chip.get_rect().y + self.blue_chip.h/2 - self.p1_score_lead.rect.h/2
        self.p2_score_lead.pos = self.p2_score.pos[0] + self.p2_score.rect.w + 10, self.orange_chip.get_rect().y + self.orange_chip.h/2 - self.p2_score_lead.rect.h/2

        self.p1_score_lead.draw()
        self.p2_score_lead.draw()

        self.victory_message.draw()
        self.win_condition.draw()


VictoryScene = S_Win() 