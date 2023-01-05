import pygame
from pygame import gfxdraw
from display_constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

dt = pygame.time.Clock().tick(FPS)/1000
    
class Slider:

    def __init__(self, surface: pygame.Surface, color: pygame.Color, 
                 pos: tuple, width: int, height: int, *, 
                 border_radius: int = 0, circle_color: pygame.Color = (255, 255, 255),
                 circle_x = 0): 
        """
        Creates a Slider object.

        - Color argument should be in (R, G, B) or pygame.Color(). \n
        - Circle radius is equal to the inputted width / 20. \n 
        - Font size is equal to circle radius.\n
        - circle_x = starting position of the circle.
        """ 
        self.surface = surface
        self.color = color
        self.x, self.y = pos
        self.width = width
        self.height = height
        self.border_radius = border_radius
        self.circle_radius = int(width // 20)
        self.circle_color = circle_color

        self.value = 0
        self.circle_x = int(circle_x*width) + self.x  # initial position of the slider circle
        self.font = pygame.font.Font('font\CookieRun_Regular.ttf', int(self.circle_radius))
        self._init()

    def _init(self):
        self.slider_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.mini_rect_fade = 0
        self.slider_selected = False
        self.collider_rect = pygame.Rect(self.x, self.y-self.height*5, self.width, self.height*10)

    def get_rect(self) -> pygame.Rect:
        """
        Returns the Rect value of the Slider object
        """
        return self.slider_rect

    def get_collider(self) -> pygame.Rect:
        """
        Returns the Rect value of the Slider's collider
        """
        return self.collider_rect

    def get_value(self) -> int:
        """
        Returns the current value of the slider (0 - 100)
        """
        self.value = int(((self.circle_x-self.x)/(self.width+self.x-self.x)*100))
        return self.value

    def get_slider_state(self) -> bool:
        """
        Returns the current status of the slider (selected or not)
        """
        return self.slider_selected

    def draw(self, x):
        """
        Draws the slider rect and the movable circle on the passed surface
        """
        diff = self.x - x
        self.x = x 
        self.slider_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.circle_x -= diff

        # draw slider
        pygame.draw.rect(self.surface, self.color, self.slider_rect, border_radius=self.border_radius)

        #draw the movable circle's shadow
        gfxdraw.aacircle(self.surface, self.circle_x, self.y + int(self.height+self.height/2), self.circle_radius, self.color)
        gfxdraw.filled_circle(self.surface, self.circle_x, self.y + int(self.height+self.height/2), self.circle_radius, self.color)
        
        #draw the movable circle of the slider
        gfxdraw.aacircle(self.surface, self.circle_x, self.y + self.height//2, self.circle_radius, self.circle_color)
        gfxdraw.filled_circle(self.surface, self.circle_x, self.y + self.height//2, self.circle_radius, self.circle_color)

    def update(self, mx: int):
        """
        Only call when the mouse hovers over the slider's collider.

        - Switches the slider's current state when mouse gets pressed.
        - Inflates the collider rect to maintain its function even after the mouse
          moves away from the initial collider rect as long as the mouse is pressed.
        - Updates the circle's current position equal to the mouse's current x position.
        - When pressed, draws a small rectangle with its shadow slightly above the circle 
          containing a text of the current slider value.
        """

        if pygame.mouse.get_pressed()[0]:
            self.slider_selected = True
            self.collider_rect.inflate_ip(SCREEN_WIDTH-self.x, SCREEN_HEIGHT-self.y)

            # set the circle's position equal to the passed argument 
            if self.x < mx <= self.x + self.width:
                self.circle_x = mx
            elif mx < self.x:
                self.circle_x = self.x
            elif mx > self.x + self.width:
                self.circle_x = self.x + self.width

            self.value = int(((self.circle_x-self.x)/(self.width+self.x-self.x)*100))
            
            if self.mini_rect_fade < 255-int(2500*dt):
                self.mini_rect_fade+=int(2500*dt)

        else:
            if self.mini_rect_fade <= int(2500*dt):
                self._init() # resets
            else:
                self.mini_rect_fade -=int(2500*dt)

        mini_rect = pygame.Rect(self.circle_x-self.circle_radius, self.y - self.circle_radius*4, self.circle_radius*2, self.circle_radius*2)
        rect_shadow = pygame.Rect(self.circle_x-(self.circle_radius-4), self.y - self.circle_radius*4+4, self.circle_radius*2, self.circle_radius*2)
        text = self.font.render(str(self.value), True, (self.circle_color))
        text_surface = pygame.Surface((mini_rect.w, mini_rect.h))
        
        gfxdraw.box(self.surface, rect_shadow, (0, 0, 0, int(self.mini_rect_fade//10)))
        gfxdraw.box(self.surface, mini_rect, (255, 112, 69, self.mini_rect_fade))
        
        text_surface.fill((225, 112, 69))
        text_surface.blit(text, (mini_rect.w//2-text.get_width()//2, mini_rect.h//2-text.get_height()//2))
        text_surface.set_alpha(self.mini_rect_fade)
        self.surface.blit(text_surface, (mini_rect.x, mini_rect.y))