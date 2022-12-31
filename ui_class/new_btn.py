import pygame
from typing import Callable, Iterable

state = str
args = Iterable

class NButton:

    def __init__(self, surface: pygame.Surface, 
                    pos: tuple, width: int, height: int, 
                    text: str, *, border_radius: int=12, 
                    rect_color=(98, 140, 159), hover_color=(124, 172, 194), 
                    selected_color=(124, 172, 194), disabled_color=(95, 95, 95), 
                    toggled_color=(243, 112, 72), text_color=(255, 255, 255), 
                    shadow_rect_color=(38, 73, 89), shadow_hovered_color=(54, 103, 126),
                    shadow_selected_color=(54, 103, 126), shadow_disabled_color=(10, 10, 10),
                    shadow_toggled_color=(149, 49, 30), transition_speed = 15,
                    fontsize: int = 0, fontstyle = 'font\CookieRun_Regular.ttf', 
                    shadow_offset: int=0, target: Callable = None, args: Iterable=[]): 
                    """
                    Creates an NButton (New Button) object

                    Optional arguments:
                        - border_radius = used for rounded corners (default = 12)
                        - rect_color = button color in normal state (default = (98, 140, 159))
                        - hover_color = button color in hovered state (default = (124, 172, 194))
                        - selected_color = button color in selected state (default = (124, 172, 194))
                        - disabled_color = button color in disabled state (default = (95, 95, 95))
                        - toggled_color = button color in toggled state (default = (243, 112, 72))
                        - text_color = text color in all button states (default = (255, 255, 255))
                        - shadow colors (shadow_rect_color, shadow_hovered_color, shadow_selected_color,
                                        shadow_disabled_color, shadow_toggled_color)
                        - transition_speed = speed of color transition (default = 15)
                        - fontsize = button text size (default = (height / 1.7))
                        - fontstyle = font styled used in the text (default = Cookie Run Regular)
                        - shadow_offset = x-offset of the shadow relative to the button rect (default = height * 0.25)
                        - target = stores a function to be called (or passed) once the button is pressed (default = None)
                        - args = arguments to be passed on the called target (default = None)
                    """
                    self.surface = surface
                    self.x, self.y = pos
                    self.width = width
                    self.height = height
                    self.text = text
                    self.border_radius = border_radius
                    
                    self.rect_color = rect_color
                    self.hover_color = hover_color
                    self.selected_color = selected_color
                    self.disabled_color = disabled_color
                    self.toggled_color = toggled_color
                
                    self.shadow_rect_color = shadow_rect_color
                    self.shadow_hovered_color = shadow_hovered_color
                    self.shadow_selected_color = shadow_selected_color
                    self.shadow_disabled_color = shadow_disabled_color
                    self.shadow_toggled_color = shadow_toggled_color

                    self.text_color = text_color
                    self.fontstyle = fontstyle
                    self.target = target
                    self.args = args

                    self.transition_speed = transition_speed
                    self.color_idx = 0

                    if fontsize >= 0:
                        self.fontsize = int(self.height / 1.7)
                    else:
                        self.fontsize = fontsize

                    if shadow_offset >= 0:
                        self.shadow_offset = self.height * 0.25
                    else:
                        self.shadow_offset = shadow_offset

                    self.toggled = False
                    self.clicked = False
                    self.prev_state = 'Normal'

                    # Dict for button states : [button color, bool, shadow color]
                    self.states = {
                        'Normal': [self.rect_color, True, self.shadow_rect_color],
                        'Hovered': [self.hover_color, False, self.shadow_hovered_color],
                        'Selected': [self.selected_color, False, self.shadow_selected_color],
                        'Disabled': [self.disabled_color, False, self.shadow_disabled_color],
                        'Toggled': [self.toggled_color, False, self.shadow_toggled_color]
                    }

                    # button, shadow, text rect
                    self.btn_rect = pygame.Rect(self.x, self.y, self.width, self.height)
                    self.btn_shadow_rect = pygame.Rect(self.x, self.y + self.shadow_offset, self.width, self.height)
                    
                    self.btn_font = pygame.font.Font(self.fontstyle, self.fontsize)
                    self.text_surface = self.btn_font.render(self.text, True, self.text_color)
                    self.text_rect = pygame.Rect((self.btn_rect.x + self.btn_rect.w//2 - self.text_surface.get_width()//2,
                                                self.btn_rect.y + self.btn_rect.h//2 - self.text_surface.get_height()//2),
                                                self.text_surface.get_size())

    def get_state(self) -> state:
        """
        Returns the current button state (dict key)
        """
        for idx, bool in enumerate(self.states.values()):
            if bool[1]:
                states = [key for key in self.states.keys()]
                return states[idx]

    def get_prev_state(self) -> state:
        """
        Returns the previous button state (dict key)
        """
        return self.prev_state

    def get_rect(self) -> pygame.Rect:
        """
        Returns the rect value of the button
        """
        return self.btn_rect

    def get_shadow_rect(self) -> pygame.Rect:
        """
        Returns the rect value of the button's shadow
        """
        return self.btn_shadow_rect

    def get_target(self) -> Callable:
        """
        Returns the function stored in the button
        """
        return self.target

    def get_args(self) -> args:
        """
        Returns the argument(s) stored in the button
        """
        return self.args

    def set_state(self, state):
        """
        Sets the button's current state
            - Normal
            - Hovered
            - Selected
            - Disabled
            - Toggled
        """

        if state == 'Hovered':
            if self.states['Toggled'][1] or self.states['Selected'][1] or self.states['Disabled'][1]:
                return

        # if the current state is different from the next state (the passed arg)
        if self.get_state() != state:
            self.color_idx = 0
            
        for states in self.states.keys():
            if states == state:
                self.states[states][1] = True
            else:
                if self.states[states][1]:
                    self.prev_state = states
                self.states[states][1] = False

    def set_speed(self, speed):
        """
        Sets the color transition's speed
        """
        self.transition_speed = speed

    def set_text(self, text: str):
        """
        Changes the button's current text
        """

        self.text = text

    def set_target(self, target: Callable):
        """
        Sets or changes the button's target function
        """
        self.target = target

    def set_args(self, args: Iterable=[]):
        """
        Sets or changes the arguments stored in the button
        (This will delete any existing args the button have)
        """
        self.args = args

    def add_args(self, args: Iterable=[]):
        """
        Append arguments on the existing args list in the button
        """
        self.args.extend(args)

    def call_target(self):
        """
        Calls the target function stored in the button
        """
        self.target(self.args)

    def draw(self, pos: tuple=None):
        """
        Draws / Updates the button's behavior / appearance depending
        on its current state 
        Pass a new position if the button is in a moving surface
        """

        # checks for collision (hover)
        mx, my = pygame.mouse.get_pos()
        if self.btn_rect.collidepoint((mx, my)):
            self.set_state('Hovered')
        else:
            if not self.toggled:
                self.set_state('Normal')

        # changes position if a new position is passed
        if pos is not None:
            self.dx, self.dy = pos
            self.btn_rect.update(self.dx, self.dy, self.width, self.height)
            self.btn_shadow_rect.update(self.dx, self.dy+self.shadow_offset, self.width, self.height)
            self.text_rect = pygame.Rect((self.btn_rect.x + self.btn_rect.w//2 - 
                                self.text_surface.get_width()//2, self.btn_rect.y + 
                                self.btn_rect.h//2 - self.text_surface.get_height()//2),
                                self.text_surface.get_size())

        # moves the button if toggled
        if self.toggled:
            self.btn_rect.move_ip(0, self.shadow_offset/1.5)
            self.text_rect.move_ip(0, self.shadow_offset/1.5)

        # gets the current and previous shadow and button colors
        current_color = pygame.color.Color(self.states[self.get_state()][0])
        prev_color = pygame.color.Color(self.states[self.get_prev_state()][0])
        current_shadow_color = pygame.color.Color(self.states[self.get_state()][2])
        prev_shadow_color = pygame.color.Color(self.states[self.get_prev_state()][2])

        if self.color_idx < self.transition_speed:
            self.color_idx +=1

        # transitioning the color from previous to current
        fade_color = [pc + ((cc - pc)/self.transition_speed)*self.color_idx 
                        for cc, pc in zip(current_color, prev_color)]
        fade_shadow_color = [psc + ((csc - psc)/self.transition_speed)*self.color_idx 
                        for csc, psc in zip(current_shadow_color, prev_shadow_color)]
        
        # draws the text, shadow rect, and the btn rect on the surface
        pygame.draw.rect(self.surface, fade_shadow_color, 
                            self.btn_shadow_rect, border_radius=self.border_radius)
        pygame.draw.rect(self.surface, fade_color, self.btn_rect, 
                            border_radius=self.border_radius)
        self.surface.blit(self.text_surface, self.text_rect)