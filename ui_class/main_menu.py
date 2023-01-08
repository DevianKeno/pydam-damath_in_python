import pygame, time
import pytweening
from pygame import gfxdraw
from .constants import BTN_PRESSED_COLOR
from ui_class import tween as tween
from ui_class.ease_funcs import *
from display_constants import SIDE_MENU_COLOR, SIDE_MENU_RECT_ACTIVE, SIDE_MENU_RECT_DEFAULT, FPS
from damath.constants import WHITE, DARK_GRAY_BLUE, OAR_BLUE, PERSIMMON_ORANGE

state, status = str, str

HOVERED = 'Hovered'
NORMAL = 'Normal'
SELECTED = 'Selected'

DEFAULT = 'Default'
ANIMATING = 'Animating'
ACTIVE = 'Active'
class Sidebar: 

    dt = pygame.time.Clock().tick(FPS)/1000
    diff = SIDE_MENU_RECT_ACTIVE.width - SIDE_MENU_RECT_DEFAULT.width

    def __init__(self, surface: pygame.Surface, 
                pos: tuple, width: float, height: float,
                color=DARK_GRAY_BLUE, font_color=OAR_BLUE,
                fontstyle='font\CookieRun_Regular.ttf', 
                fontsize=int(SIDE_MENU_RECT_ACTIVE.height*0.045),
                anim_duration: int=8):
                """
                Creates the sidebar object

                Optional parameters:
                - color: sidebar's color (DARK GRAY BLUE)
                - font_color: sidebar option's font color (OAR BLUE)
                - fontstyle: sidebar option's font style (Cookie Run Regular)
                - fontsize: sidebar option's font size
                """

                self.surface = surface
                self.x, self.y = pos
                self.w, self.h = self.width, self.height = width, height
                self.color = color
                self.font_color = font_color
                self.fontstyle = fontstyle
                self.fontsize = fontsize

                self.anim_duration = anim_duration
                self.anim_idx = 0

                self.current_w = width
                self.init_w = width
                
                self.options = {}
                self.options_counter = 0

                self.font = pygame.font.Font(fontstyle, fontsize)
                self._init()

    def _init(self):

        self._STATUS = {
            DEFAULT: True,
            ANIMATING: False,
            ACTIVE: False
            }

        self._STATES = {
            HOVERED: False,
            NORMAL: True
            }

        self.state = NORMAL
        self.status = DEFAULT
        self.sidebar_rect = pygame.Rect(self.x, self.y, 
                                self.w, self.h)
        
        self.anim_move = (self.diff/self.anim_duration)

    def _draw(self, nwidth=None, nheight=None):
        """
        Animates and draws the sidebar rect and its options
        """
        
        if nwidth is None:
            nwidth = self.w
        if nheight is None:
            nheight = self.h
        
        self.sidebar_rect.update(self.x, self.y, nwidth, nheight)
        pygame.draw.rect(self.surface, self.color, self.sidebar_rect)

        if self.anim_idx >= self.anim_duration//4:
            if self.options is not None:
                for option in self.options.keys():
                    self.options[option].update_state(nx=self.options[option].init_x+(10*self.anim_idx))
            
        r, g, b, a = pygame.Color(self.color)
        gfxdraw.box(self.surface, self.sidebar_rect, (r, g, b, (a-(a*(self.anim_idx/self.anim_duration)))))
    
    def _animate(self):
        """
        Changes animation indexes, current width, and sidebar status
        """
        
        if self.state == NORMAL:
            if self.current_w > self.init_w:
                self.current_w-=self.anim_move
            if self.anim_idx > 0:
                self.anim_idx-=1
                self.set(status=ANIMATING)
            else:
                self.set(status=DEFAULT)

        else:
            if self.current_w < (self.init_w + self.diff):
                self.current_w+=self.anim_move
            if self.anim_idx < self.anim_duration:
                self.anim_idx+=1
                self.set(status=ANIMATING)
            else:
                self.set(status=ACTIVE)

        self._draw(self.current_w)

    def add_option(self, type: int, id: str, *, text: str, description: str, 
                    pos: tuple, width: float=None, height: float=None, default_color=OAR_BLUE, 
                    hovered_color=WHITE, selected_color=PERSIMMON_ORANGE, 
                    icon=None, icon_placement='left', icon_offset=10, img=None, 
                    target: callable=None, args=None, index=None):
                    """
                    Adds options in the sidebar
                    
                    Types:
                    - 1: Image (Unfinished)
                    - 2: Text
                    - 3: Text with Icon (Unfinished)
                    """
                    
                    if type not in [1, 2]:
                        raise ValueError('Type must be 1 or 2')

                    match type:
                        case 1:
                            self.options[id] = Image(self.surface, id, pos, width, height,
                                                    img, target, args, index)
                        case 2:
                            self.options[id] = Text(self.surface, id, pos, text, description,
                                                    self.fontstyle, self.fontsize,
                                                    default_color, hovered_color, 
                                                    selected_color, target, args, index)
                        #TODO: finish TextIcon if ever icon for every options gets created
                        case 3:
                            self.options[id] = TextIcon(id, pos, width, height,
                                                    text, description,
                                                    default_color, hovered_color,
                                                    selected_color, icon,
                                                    icon_placement, icon_offset,
                                                    target, args, index)

    def set(self, *, state=None, status=None):
        """
        Sets a state or a status for the sidebar
        """
        pass

        if state is not None:
            if state not in self._STATES.keys():
                raise ValueError(f'Invalid State.' \
                                f'Expected one of the following: {self._STATES}')

            for key_state in self._STATES.keys():
                if key_state != state:
                    self._STATES[key_state] = False
                else:
                    self._STATES[key_state] = True
            
            self.state = state
            self._animate()

        if status is not None:
            if status not in self._STATUS.keys():
                raise ValueError(f'Invalid Status.' \
                                    f'Expected one of the following: {self._STATUS}')
                
            for key_status in self._STATUS.keys():
                if key_status != status:
                    self._STATUS[key_status] = False
                else:
                    self._STATUS[key_status] = True       

            self.status = status

    def get_option(self, id) -> object:
        """
        Returns the SideBarOption object from the sidebar
        """
        return self.options.get(id)

    def update_options_state(self, id, state):
        for option in self.options.keys():
            if option != id:
                if state == HOVERED:
                    if self.get_option(option).state != SELECTED:
                        self.get_option(option).set_state(NORMAL)
                elif state == SELECTED:
                    if self.get_option(option).state == SELECTED:
                        self.get_option(option).set_state(NORMAL)                   
            if option == id:
                self.get_option(option).set_state(state)

class SidebarOptions:
    def __init__(self, surface, id, pos, width, 
                height, target, args, index):
                """
                Creates SidebarOptions object

                Only the Sidebar object should instantiate an object
                from this class

                Stores general functionality of a sidebar option 
                (setting a state, calling a function, and setting a target function)
                """
                self.surface = surface
                self.id = id
                self.init_x = pos[0]
                self.x, self.y = pos
                self.w, self.h = self.width, self.height = width, height
                self.target = target
                self.args = args
                self.index = index
                self.state = NORMAL

                self._STATES = {
                    NORMAL: True,
                    HOVERED: False,
                    SELECTED: False
                }

    def call_target(self):
        """
        Calls the stored function
        in the options object
        """
        if self.target is None:
            return

        if self.args is None:
            return self.target()

        self.target(args for args in self.args)

    def set_state(self, state):
        """
        Sets the state of the sidebar option
        """
        if state == HOVERED:
            if self.state == SELECTED:
                return
            
        for key_state in self._STATES.keys():
            if key_state == state:
                self._STATES[key_state] = True
            else:
                self._STATES[key_state] = False

        self.state = state

    def set_target(self, target):
        self.target = target

class Image(SidebarOptions):
    def __init__(self, surface, id, pos, width, height, 
                    img, target, args, index):
        super().__init__(surface,id, pos, width, 
                    height,target, args, index)
        self.img = img

class Text(SidebarOptions):
    def __init__(self, surface, id, pos, text,
                description, fontstyle, fontsize,
                default_color, hovered_color, 
                selected_color, target, args, index):
                """
                A text SideBarOptions object

                This class requires several text 
                attributes as its parameter
                (colors depending on the state, text, description)
                """

                self.text = text
                self.description = description
                self.fontstyle = fontstyle
                self.fontsize = fontsize
                self.font = pygame.font.Font(fontstyle, fontsize)
                self.font_scale = pygame.font.Font(fontstyle, int(fontsize*1.2))
                self.font_mini = pygame.font.Font(fontstyle, int(0.42*fontsize))
                self.hover_idx = 0

                self._COLORS = {
                    NORMAL: default_color,
                    HOVERED: hovered_color,
                    SELECTED: selected_color
                }

                self.text_surface = self.font.render(text, True, default_color)
                self.desc_surface = self.font_mini.render(description, True, hovered_color)
                super().__init__(surface, id, pos, self.text_surface.get_width(), 
                                self.text_surface.get_height(), target, args, index)

    def _draw(self, nx=None):
        """
        Draws / Updates the text rects & surfaces
        """
        if nx is not None:
            self.x = nx 

        if self.state == HOVERED:
            self.text_update_surface = self.font_scale.render(self.text, True, self._COLORS[HOVERED])
            self.text_rect = self.text_update_surface.get_rect(center=self.get_rect().center)
            self.surface.blits(blit_sequence=((self.desc_surface, (self.text_rect.x-5+
                                self.hover_idx, self.y+self.h)), (self.text_update_surface, (self.text_rect))))
            if self.hover_idx < 10:
                self.hover_idx+=1
        else:
            self.text_surface = self.font.render(self.text, True, self._COLORS[self.state])
            self.surface.blit(self.text_surface, (self.x, self.y))

            self.text_update_surface = self.font_scale.render(self.text, True, self._COLORS[HOVERED])
            self.text_rect = self.text_update_surface.get_rect(center=self.get_rect().center)
            if self.hover_idx > 3:
                self.surface.blit(self.desc_surface, (self.text_rect.x-5+self.hover_idx, self.y+self.h))
                self.hover_idx-=1

    def update_state(self, state=None, nx=None):
        """
        Updates the option's state
        An optional ragument (nx) can be passed
        if the object needs to be moved
        """
        if state is not None:
            self.set_state(state)
        if nx is not None:
            self._draw(nx)
        else:
            self._draw()

    def get_rect(self) -> pygame.Rect:
        """
        Returns the text rect value
        """
        return pygame.Rect(self.x, self.y, self.text_surface.get_width(), self.text_surface.get_height())

class TextIcon(Text):
    def __init__(self, id, pos, width, height,
                    text, description, default_color, 
                    hovered_color, selected_color, icon, 
                    icon_placement, icon_offset, 
                    target, args, index):

                    super().__init__(id, pos, width, height,
                                    text, description,
                                    default_color, hovered_color,
                                    selected_color, target,
                                    args, index)

                    self.icon = icon
                    self.icon_placement = icon_placement
                    self.icon_offset = icon_offset