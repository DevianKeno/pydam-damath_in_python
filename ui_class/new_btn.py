import pygame
from typing import Callable, Iterable
from event_loop import event_loop
from .tooltip import Tooltip
from .colors import *

state = str
args = Iterable

'''
Guide for creating new buttons:

    - first instantiate individual buttons using the NButton Class
    - group them as a list and instantiate a new ButtonGroup Class
        (Note: You will still need to create a ButtonGroup even if
                there's only a single button you have to add, and 
                this can also be helpful if we later decide to add more 
                buttons in the same Screen with that singleton ButtonGroup)
    - call the draw() method of the ButtonGroup inside the loop, 
        you are allowed to pass new positions for the buttons if it is 
        affected by any moving surfaces, or you can call it with no parameters
        if you want all the buttons' positions in the ButtonGroup to be fixed
'''

class NButton(Tooltip):

    Normal = 'Normal'
    Hovered = 'Hovered'
    Selected = 'Selected'
    Disabled = 'Disabled'
    Toggled = 'Toggled'

    def __init__(self, surface: pygame.Surface, 
                    pos: tuple, width: int, height: int, 
                    *, text: str='', border_radius: int=16, 
                    rect_color=(98, 140, 159), hover_color=(124, 172, 194), 
                    selected_color=(124, 172, 194), disabled_color=(130, 130, 130), 
                    toggled_color=(243, 112, 72), text_color=(255, 255, 255), 
                    shadow_rect_color=(38, 73, 89), shadow_hovered_color=(54, 103, 126),
                    shadow_selected_color=(54, 103, 126), shadow_disabled_color=(80, 80, 80),
                    shadow_toggled_color=(149, 49, 30), transition_duration = 10,
                    fontsize: int = 0, fontstyle = 'font\CookieRun_Regular.ttf', 
                    shadow_offset: int=0, tooltip_text=None, target: Callable = None, args: Iterable=[],
                    toggleable: bool=False): 
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
                        - transition_duration = duration of color transition (default = 20)
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

                    self.transition_duration = transition_duration
                    self.color_idx = 0
                    self.moved = False
                    self.pos_reset = False
                    self.will_call_target = False

                    if fontsize <= 0:
                        self.fontsize = int(self.height / 1.7)
                    else:
                        self.fontsize = fontsize

                    if shadow_offset <= 0:
                        self.shadow_offset = self.height * 0.25
                    else:
                        self.shadow_offset = shadow_offset

                    self.toggleable = toggleable
                    self.prev_state = self.Normal

                    # Dict for button states : [button color, bool, shadow color]
                    self.states = {
                        self.Normal: [self.rect_color, False, self.shadow_rect_color],
                        self.Hovered: [self.hover_color, False, self.shadow_hovered_color],
                        self.Selected: [self.selected_color, False, self.shadow_selected_color],
                        self.Disabled: [self.disabled_color, True, self.shadow_disabled_color],
                        self.Toggled: [self.toggled_color, False, self.shadow_toggled_color]
                    }

                    if (self.target != None or self.args):
                        self.states[self.Normal][1] = True

                    # button, shadow, text rect
                    self.btn_rect = pygame.Rect(self.x, self.y, self.width, self.height)
                    self.btn_shadow_rect = pygame.Rect(self.x, self.y + self.shadow_offset, self.width, self.height)
                    
                    self.btn_font = pygame.font.Font(self.fontstyle, self.fontsize)
                    self.text_surface = self.btn_font.render(self.text, True, self.text_color)
                    self.text_rect = pygame.Rect((self.btn_rect.x + self.btn_rect.w//2 - self.text_surface.get_width()//2,
                                                self.btn_rect.y + self.btn_rect.h//2 - self.text_surface.get_height()//2),
                                                self.text_surface.get_size())

                    #TODO: Pass the text object and text.get_width()*1.25 as the tooltip rect's width
                    super().__init__(self.surface, 0, 0, self.width*1.25, self.height, PERSIMMON_ORANGE, (255, 255, 255), tooltip_text, shadow_offset=2)

    @property
    def toggled(self):
        return self.states[self.Toggled][1]

    @property
    def clicked(self):
        return self.states[self.Selected][1]

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

        _STATES = [self.Normal, self.Hovered, self.Selected, self.Disabled, self.Toggled]

        if state not in _STATES:
            raise ValueError(f'Invalid argument. Expected one of the following: {_STATES}')

        if state == self.Normal:
            if self.get_target() == None and not self.get_args():
                return

        if state == self.Hovered:
            if self.states[self.Toggled][1] or self.states[self.Selected][1] or self.states[self.Disabled][1]:
                return

        if state == self.Selected or state == self.Toggled:
            if self.get_state() == self.Disabled:
                return
            elif state == self.Toggled and not self.toggleable:
                raise ValueError("Non-toggleable buttons cannot be set to toggled.")

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

    def set_duration(self, duration):
        """
        Sets the color transition's duration
        """
        self.transition_duration = duration

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
        if not self.toggleable:
            self.set_state(self.Selected)
        self.will_call_target = True

    def _call_target(self):
        if self.will_call_target:
            if self.args:
                return self.target(self.args)
            else:
                return self.target()
        else:
            return None

    def draw(self, pos: tuple=None):
        """
        Draws / Updates the button's behavior / appearance depending
        on its current state 
        Pass a new position if the button is in a moving surface
        """

        # checks for collision (hover)
        self.pos_reset = False
        
        mx, my = pygame.mouse.get_pos()
        if self.btn_rect.collidepoint((mx, my)):
            # self.show_tooltip(1)
            self.set_state(self.Hovered)
        else:
            if not self.toggled and not self.clicked:
                if not self.get_state() == self.Disabled:
                    self.set_state(self.Normal)

        # changes position if a new position is passed
        if pos is None:
            self.dx, self.dy = self.x, self.y

        else:
            self.dx, self.dy = pos
            
        self.btn_rect.update(self.dx, self.dy, self.width, self.height)
        self.btn_shadow_rect.update(self.dx, self.dy+self.shadow_offset, self.width, self.height)
        self.text_rect = pygame.Rect((self.btn_rect.x + self.btn_rect.w//2 - 
                            self.text_surface.get_width()//2, self.btn_rect.y + 
                            self.btn_rect.h//2 - self.text_surface.get_height()//2),
                            self.text_surface.get_size())
            
        # moves the button if toggled or clicked and mouse pressed
        if self.get_state() == self.Toggled or (self.get_state() == self.Selected and pygame.mouse.get_pressed()[0]):
            self.btn_rect.move_ip(0, self.shadow_offset/1.5)
            self.text_rect.move_ip(0, self.shadow_offset/1.5)
            self.moved = True
            if self.will_call_target and self.get_state() == self.Toggled:
                self._call_target()
        # if clicked and the mouse button is no longer pressed
        elif self.get_state() == self.Selected and not pygame.mouse.get_pressed()[0]:
            self.set_state(self.Normal)
            if self.moved:
                self.moved = False
                self.pos_reset = True
            if self.btn_rect.collidepoint(pygame.mouse.get_pos()):
                self._call_target()

        # gets the current and previous shadow and button colors
        current_color = pygame.color.Color(self.states[self.get_state()][0])
        prev_color = pygame.color.Color(self.states[self.get_prev_state()][0])
        current_shadow_color = pygame.color.Color(self.states[self.get_state()][2])
        prev_shadow_color = pygame.color.Color(self.states[self.get_prev_state()][2])

        if self.color_idx < self.transition_duration:
            self.color_idx +=1

        # transitioning the color from previous to current
        fade_color = [pc + ((cc - pc)/self.transition_duration)*self.color_idx 
                        for cc, pc in zip(current_color, prev_color)]
        fade_shadow_color = [psc + ((csc - psc)/self.transition_duration)*self.color_idx 
                        for csc, psc in zip(current_shadow_color, prev_shadow_color)]
        
        # draws the text, shadow rect, and the btn rect on the surface
        pygame.draw.rect(self.surface, fade_shadow_color, 
                            self.btn_shadow_rect, border_radius=self.border_radius)
        pygame.draw.rect(self.surface, fade_color, self.btn_rect, 
                            border_radius=self.border_radius)
        self.surface.blit(self.text_surface, self.text_rect)

class ButtonGroup:

    def __init__(self, btn_list: list, allowed_selection: int=None, auto_unselect: bool=False, \
                    *, caller_btn=None, pass_target: bool=False, pass_args: bool=False):
        """
        Creates a button group, ideal for creating a radio / options / toggle buttons that 
        can only allow limited numbers of toggled / clicked buttons

        Only the buttons inside this ButtonGroup can be selected or toggled, so clickable buttons
        inside the same Screen should be grouped for it to function properly 

        Optional Arguments:


        - allowed_selection
                - number of buttons the user is allowed to select / toggle
                - Default = len(btn_list) - 1
        - auto_unselect
                - if the number of buttons selected exceed the allowed selection,
                the button will unselect automatically or not
                - Default = False
        - caller_btn
                - button where other buttons can pass their targets / args to
                - Default = None
        - pass_target
                - if True, pass the toggled button's target to the caller button
                - Default = False
        - pass_args
                - if True, pass the toggled button's arguments to the caller button
                - Default = False
        """

        self.btn_list = btn_list
        if allowed_selection == None:
            self.allowed_selection = len(btn_list) - 1
        else:
            if allowed_selection < len(btn_list):
                self.allowed_selection = allowed_selection
            else:
                raise ValueError("Allowed selection should be less than the total number of buttons.")
                
        self.auto_unselect = auto_unselect
        self.active_btns = []
        self.caller_btn = caller_btn

        if self.caller_btn != None:
            self.pass_target = pass_target
            self.pass_args = pass_args
        else:
            if pass_args or pass_target:
                raise AttributeError("No caller button passed. Cannot assign values to pass_args or pass_target.")

    def restart(self):
        for btn in self.btn_list:
            btn.set_state(btn.Normal)

    @property
    def btns_selected(self):
        return len(self.active_btns)

    def _set_state(self, btn: NButton, state):

        btn.set_state(state)

        if btn.clicked or btn.toggled: 
            self.active_btns.append(btn)
        elif btn.get_state() == btn.Disabled:
            return
        else:
            if btn in self.active_btns:
                self.active_btns.remove(btn)

    def draw(self, new_pos_list: list=None, caller_new_pos: tuple=None):
        """
        Draws the buttons in the group,

        a new position can be passed as a list corresponding to the ordered lists of buttons passed,
        and a new position for the caller button can be passed separately in caller_new_pos
        """

        if new_pos_list == None:
            new_pos_list = [None] * len(self.btn_list) 

        for btn, pos in zip(self.btn_list, new_pos_list):
            if pos != None:
                btn.draw(pos)
            else:
                btn.draw()

        if self.caller_btn != None:
            if caller_new_pos != None:
                self.caller_btn.draw(caller_new_pos)
            else:
                self.caller_btn.draw()

        for event in event_loop.event_list:
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos

                    if self.caller_btn != None:
                        if self.caller_btn.btn_rect.collidepoint((x, y)):
                            self.caller_btn.set_state(self.caller_btn.Selected)
                            self.caller_btn.call_target()

                    # check if any buttons are hovered when the mouse is clicked
                    # and change it to its selected / toggled state
                    for btn in self.btn_list:
                        if btn.btn_rect.collidepoint((x, y)):

                            if btn.toggleable:
                                if not btn.states[btn.Toggled][1]:
                                    if self.btns_selected < self.allowed_selection:
                                        self._set_state(btn, btn.Toggled)
                                        if self.caller_btn != None:
                                            if self.pass_target:
                                                self.caller_btn.set_target(btn.get_target())
                                            if self.pass_args:
                                                self.caller_btn.set_args(btn.get_args()) 
                                            elif (not self.pass_args and not self.pass_target):
                                                btn.call_target()     
                                                # self._set_state(btn, btn.Toggled)                               
                                    else:
                                        if self.auto_unselect:
                                            self._set_state(btn, btn.Toggled)
                                            if btn.toggled:
                                                for remaining_btn in self.active_btns:
                                                    if self.btns_selected >= self.allowed_selection:
                                                        if remaining_btn != btn:
                                                            self._set_state(remaining_btn, remaining_btn.Normal)
                                                if self.caller_btn != None:
                                                    if self.pass_target:
                                                        self.caller_btn.set_target(btn.get_target())
                                                    if self.pass_args:
                                                        self.caller_btn.set_args(btn.get_args())  
                                                    elif (not self.pass_args and not self.pass_target):
                                                        btn.call_target()      
                                else:
                                    self._set_state(btn, btn.Normal)
                            else:
                                self._set_state(btn, btn.Selected)
                                btn.call_target()

        if self.caller_btn != None:
            if len(self.active_btns) == 0:
                self.caller_btn.set_state(self.caller_btn.Disabled)
                if self.pass_target:
                    self.caller_btn.set_target(None)
                if self.pass_args:
                    self.caller_btn.set_args(None)
            else:
                if self.pass_target:
                    if self.caller_btn.get_target() != None:
                        if self.caller_btn.get_state() != self.caller_btn.Selected:
                            self.caller_btn.set_state(self.caller_btn.Normal)
                    else:
                        self.caller_btn.set_state(self.caller_btn.Disabled)
                if self.pass_args:
                    if self.caller_btn.get_args() != None:
                        if self.caller_btn.get_state() != self.caller_btn.Selected:
                            self.caller_btn.set_state(self.caller_btn.Normal)
                    else:
                        self.caller_btn.set_state(self.caller_btn.Disabled)
                else:
                    if self.caller_btn.get_state() != self.caller_btn.Selected:
                        self.caller_btn.set_state(self.caller_btn.Normal)
