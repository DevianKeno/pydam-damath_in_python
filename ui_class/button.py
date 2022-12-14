from ui_class.constants import TXT_COLOR, BTN_COLOR, FONTSIZE, HOVER_SIZE
from display_constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ui_class.fade import *
import pygame

class Button:
    def __init__(self, screen, width, height, pos, radius, image, image_size=None, text=None, fontsize=FONTSIZE):
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

    def display_image(self):
        """
        Displays the image in the window
        """
        # if an image is passed in the initialization
        if self.image_surface != None:
            self.image_rect = self.image_surface.get_rect(center=self.top_rect.center)
            pygame.draw.rect(self.screen , self.top_color, self.top_rect, border_radius=8)
            pygame.draw.circle(self.screen , 'white', self.top_big_circle, self.radius)
            pygame.draw.circle(self.screen , 'white', self.top_small_circle,self.radius//2)
            pygame.draw.circle(self.screen , 'white', self.bottom_big_circle, self.radius)
            pygame.draw.circle(self.screen , 'white', self.bottom_small_circle, self.radius//2)
            self.screen.blit(self.image_surface, self.image_rect)

    def render(self):
        """
        Renders a Surface Object
        (The text/image in the button Object)
        """
        # for text
        font = pygame.font.Font("font/GlacialIndifference-Bold.ttf", self.text_fontsize)
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

    def play_audio(self):
        if self.play == 1:
            pygame.mixer.music.load("audio/pop.wav")
            pygame.mixer.music.play()

    def hover_update(self, func=None, param=None, func2=None, _fade=True, delay=6):
        """
        Updates if mouse hovered or clicked the button
        """
        # updates the button rectangle and text
        self.top_rect.update((self.x-(HOVER_SIZE/2), self.y-(HOVER_SIZE/2)), 
                                (self.width+HOVER_SIZE, self.height+HOVER_SIZE))
        self.radius = self.init_radius+1
        self.top_color = '#51A938'
        self.text_fontsize = self.fontsize+(int(self.fontsize*0.2))
        self.play+=1
        self.play_audio()
        self.delay = delay

        # updates image if it contains one
        if self.image_surface is not None:
            self.image_surface = pygame.transform.smoothscale(self.image_surface, (self.image_width+(self.image_width*0.2), self.image_height+(self.image_height*0.2))).convert_alpha()
            pygame.draw.rect(self.screen, self.top_color, self.top_rect, border_radius=8)

        # checks for clicks
        if pygame.mouse.get_pressed()[0]:
            self.top_big_circle[1] = self.y+self.bigcircle_y_offset + 2
            self.bottom_big_circle[1] = self.y+self.height-self.bigcircle_y_offset + 2
            self.top_small_circle[1] = self.y+self.smallcircle_y_offset + 2
            self.bottom_small_circle[1] = self.y+self.height-self.smallcircle_y_offset + 2
            self.y = self.pos[1] + 5
            self.clicked = True
        else:
            self.top_big_circle[1] = self.y+self.bigcircle_y_offset
            self.bottom_big_circle[1] = self.y+self.height-self.bigcircle_y_offset
            self.top_small_circle[1] = self.y+self.smallcircle_y_offset
            self.bottom_small_circle[1] = self.y+self.height-self.smallcircle_y_offset
            self.y = self.pos[1]
            if self.clicked:
                self.reset()
                if func is not None:
                    self.clicked = False
                    if param:
                        func(param)
                    else:
                        func()
                self.clicked = False # temp
        
    def reset(self):
        """
        Resets all attributes of the button
        """
        self.top_rect.update((self.x, self.y), (self.width, self.height))
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

        if self.image_surface is not None:
            self.image_surface = self.image