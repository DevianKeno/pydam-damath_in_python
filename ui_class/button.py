from ui_class.constants import TXT_COLOR, BTN_COLOR, FONTSIZE, HOVER_SIZE, BTN_HOVER_COLOR, BTN_PRESSED_COLOR
from display_constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ui_class.fade import *
from ui_class.tween import *
from audio_constants import *
from damath.constants import LIGHT_BLUE, RED
import pygame

class Button:
    def __init__(self, screen, width, height, pos, radius, image, image_size=None, text=None, fontsize=FONTSIZE+8, target=None, toggle=False):
        """
        Creates Rectangle Object
        (The main rectangle of the button Object)
        """
        # passed arguments ------
        self.fontsize = fontsize
        self.screen = screen
        self.width = width
        self.height = height
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.image = image
        self.image_surface = image
        self.text = text
        self.init_radius = radius
        self.target = target
        self.toggle = toggle

        self.pos_x = self.x
        self.pos_y = self.y

        if image_size != None:
            self.image_width, self.image_height = image_size

        # initialized attributes ------
        self.top_rect = pygame.Rect(pos, (width, height)) # (x, y), (w, h)
        self.bigcircle_x_offset = 12
        self.bigcircle_y_offset = 11
        self.smallcircle_x_offset = 10
        self.smallcircle_y_offset = 22
        self.top_big_circle = [self.x+self.bigcircle_x_offset, self.y+self.bigcircle_y_offset ]
        self.top_small_circle = [self.x+self.smallcircle_x_offset, self.y+self.smallcircle_y_offset]
        self.bottom_big_circle = [self.x+self.width-self.bigcircle_x_offset, self.y+self.height-self.bigcircle_y_offset]
        self.bottom_small_circle = [self.x+self.width-self.smallcircle_x_offset, self.y+self.height-self.smallcircle_y_offset]
        self.radius = self.init_radius 
        self.top_color = BTN_COLOR
        self.text_color = TXT_COLOR
        self.text_fontsize = self.fontsize
        self.play = 0
        self.clicked = False

    def get_target(self):

        if self.target is not None:
            return self.target
        return False

    def display_image(self):
        """
        Displays the image in the window
        """
        # if an image is passed in the initialization
        if self.image_surface != None:
            self.image_rect = self.image_surface.get_rect(center=self.top_rect.center)
            pygame.draw.rect(self.screen , self.top_color, self.top_rect, border_radius=12)
            # pygame.draw.circle(self.screen , 'white', self.top_big_circle, self.radius)
            # pygame.draw.circle(self.screen , 'white', self.top_small_circle,self.radius//2)
            # pygame.draw.circle(self.screen , 'white', self.bottom_big_circle, self.radius)
            # pygame.draw.circle(self.screen , 'white', self.bottom_small_circle, self.radius//2)
            self.screen.blit(self.image_surface, self.image_rect)

    def render(self):
        """
        Renders a Surface Object
        (The text/image in the button Object)
        """
        # for text
        font = pygame.font.Font('font\CookieRun_Regular.ttf', self.text_fontsize)
        self.text_surface = font.render(self.text, True, self.text_color) #FFFFFF
        self.text_rect = self.text_surface.get_rect(center=self.top_rect.center)      

    def draw(self):
        """
        Calls the render() function to render the text,
        and draws the rectangle Object in the window
        (Shows the rectangle and text in the screen)
        """
        self.render()
        pygame.draw.rect(self.screen, self.top_color, self.top_rect, border_radius=8)
        pygame.draw.circle(self.screen, 'white', self.top_big_circle, self.radius)
        pygame.draw.circle(self.screen, 'white', self.top_small_circle,self.radius//2)
        pygame.draw.circle(self.screen, 'white', self.bottom_big_circle, self.radius)
        pygame.draw.circle(self.screen, 'white', self.bottom_small_circle, self.radius//2)
        self.screen.blit(self.text_surface, self.text_rect)

    def mdraw(self): #clicked btn position
        """
        Calls the render() function to render the text,
        and draws the rectangle Object in the window
        (Shows the rectangle and text in the screen)
        """
        self.top_rect.update((self.pos_x, self.pos_y+5, self.top_rect.w, self.top_rect.h))
        self.render()
        pygame.draw.rect(self.screen, BTN_PRESSED_COLOR, self.top_rect, border_radius=12)
        # pygame.draw.circle(self.screen, 'white', self.top_big_circle, self.radius)
        # pygame.draw.circle(self.screen, 'white', self.top_small_circle,self.radius//2)
        # pygame.draw.circle(self.screen, 'white', self.bottom_big_circle, self.radius)
        # pygame.draw.circle(self.screen, 'white', self.bottom_small_circle, self.radius//2)
        self.screen.blit(self.text_surface, self.text_rect)

    def ddraw(self, pos_x, pos_y): # for btn pos changes

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.top_rect.update((pos_x, pos_y, self.top_rect.w, self.top_rect.h))

        font = pygame.font.Font('font\CookieRun_Regular.ttf', self.text_fontsize)
        self.text_surface = font.render(self.text, True, self.text_color) #FFFFFF
        self.text_rect = self.text_surface.get_rect(center=self.top_rect.center)

        pygame.draw.rect(self.screen, self.top_color, self.top_rect, border_radius=12)
        self.screen.blit(self.text_surface, self.text_rect)

    def rdraw(self): #redraw the ddraw btn

        self.top_rect.update((self.pos_x, self.pos_y, self.top_rect.w, self.top_rect.h))

        font = pygame.font.Font('font\CookieRun_Regular.ttf', self.text_fontsize)
        self.text_surface = font.render(self.text, True, self.text_color) #FFFFFF
        self.text_rect = self.text_surface.get_rect(center=self.top_rect.center)

        pygame.draw.rect(self.screen, self.top_color, self.top_rect, border_radius=12)
        self.screen.blit(self.text_surface, self.text_rect)

    def play_audio(self):
        if self.play == 1:
            POP_SOUND.play()

    def hover_update(self, target=None, args=None, _fade=False, delay=6):
        """
        Updates if mouse hovered or clicked the button
        """

        # updates the button rectangle and text
        self.top_rect.update((self.x-(HOVER_SIZE/2), self.y-(HOVER_SIZE/2)), 
                                (self.width+HOVER_SIZE, self.height+HOVER_SIZE))
        self.radius = self.init_radius+1
        if self.clicked:
            self.top_color = BTN_PRESSED_COLOR
        else:
            self.top_color = BTN_HOVER_COLOR 
        self.text_fontsize = self.fontsize+(int(self.fontsize*0.2))
        self.play+=1
        self.play_audio()
        self.delay = delay


        # updates image if it contains one
        if self.image_surface is not None:
            self.image_surface = pygame.transform.smoothscale(self.image_surface, (self.image_width+(self.image_width*0.2), self.image_height+(self.image_height*0.2))).convert_alpha()
            pygame.draw.rect(self.screen, self.top_color, self.top_rect, border_radius=12)

        # checks for clicks
        if pygame.mouse.get_pressed()[0]:
            self.clicked = True
        # else:
        #     if self.clicked:
        #         SWEEP_SOUND.play()
        #         #self.reset()
        #         # if target is not None:
        #         #     self.clicked = False
        #         #     if args:
        #         #         target(args)
        #         #     else:
        #         #         target()
        #         self.clicked = False # temp

    def reset(self):
        """
        Resets all attributes of the button
        """
        self.top_rect.update((self.pos_x, self.pos_y, self.width, self.height))
        self.radius = self.init_radius 
        self.top_color = BTN_COLOR
        self.text_color = TXT_COLOR
        self.text_fontsize = self.fontsize
        self.play = 0
        self.top_big_circle[1] = self.y+self.bigcircle_y_offset
        self.bottom_big_circle[1] = self.y+self.height-self.bigcircle_y_offset
        self.top_small_circle[1] = self.y+self.smallcircle_y_offset
        self.bottom_small_circle[1] = self.y+self.height-self.smallcircle_y_offset
        self.y = self.pos[1]
        self.clicked = False

        if self.image_surface is not None:
            self.image_surface = self.image

    def __repr__(self):
        return str(f'Button Clicked: {self.text}')

class ButtonList(Button):

    def __init__(self, btn_list):
        self.btn_list = btn_list
        self.hvrd_status = [False]*3
        self.clicked_btn = None
        self.clicked_status = False

    def get_hvrd_status(self):
        return any(self.hvrd_status) 

    def hover_check(self, mx, my):
        for idx, btn in enumerate(self.btn_list):
            if btn.top_rect.collidepoint((mx, my)):
                self.hvrd_status[idx] = True
                btn.hover_update()
                for remaining_btn in self.btn_list:
                    if remaining_btn != btn and not remaining_btn.clicked and not remaining_btn.toggle:
                        remaining_btn.reset()

                if pygame.mouse.get_pressed()[0]:
                    if not self.clicked_status:
                        self.clicked_status = True

                        if self.clicked_btn == btn:
                            self.clicked_btn = None
                            btn.reset()

                        else:
                            btn.clicked = True
                            self.clicked_btn = btn

                            for remaining_btn in self.btn_list:
                                if remaining_btn != btn:
                                    remaining_btn.rdraw()
                                    remaining_btn.reset()

                    if self.clicked_status:
                        pass

            else:
                if btn.clicked and btn.toggle:
                    pass
                else:
                    btn.reset()
                self.hvrd_status[idx] = False

        self.clicked_status = False



    