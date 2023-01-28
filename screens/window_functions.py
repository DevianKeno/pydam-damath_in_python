import pygame
from objects import *
from ui_class.colors import OAR_BLUE
from display_constants import SIDE_MENU_RECT_ACTIVE, SCREEN_WIDTH, SCREEN_HEIGHT, screen

def custom_window():

    heading = pygame.font.Font('font\CookieRun_Bold.ttf', int(SIDE_MENU_RECT_ACTIVE.height*0.06))
    subheading = pygame.font.Font('font\CookieRun_Regular.ttf', int(SIDE_MENU_RECT_ACTIVE.height*0.035))

    board_text = heading.render('Board', True, WHITE)
    pieces_text = heading.render('Pieces', True, WHITE)
    symbols_text = subheading.render('Symbols', True, WHITE)
    values_text = subheading.render('Values', True, WHITE)
    promotion_text = subheading.render('Promotion', True, WHITE)

    screen.blit(board_text, (mode_window.rect_window.x+
                mode_window.rect_window.w*0.025,
                mode_window.rect_window.y+
                mode_window.rect_window.h*0.05))
    screen.blit(symbols_text, (mode_window.rect_window.x+
                mode_window.rect_window.w*0.025,
                mode_window.rect_window.y+
                mode_window.rect_window.h*0.05 + 
                board_text.get_height()*1.5))
    screen.blit(pieces_text, (mode_window.rect_window.x+
                mode_window.rect_window.w*0.025,
                mode_window.rect_window.y+
                mode_window.rect_window.h*0.05 + 
                board_text.get_height()*2.5))
    screen.blit(values_text, (mode_window.rect_window.x+
                mode_window.rect_window.w*0.025,
                mode_window.rect_window.y+
                mode_window.rect_window.h*0.05 + 
                board_text.get_height()*3.75))
    screen.blit(promotion_text, (mode_window.rect_window.x+
                mode_window.rect_window.w*0.025,
                mode_window.rect_window.y+
                mode_window.rect_window.h*0.05 + 
                board_text.get_height()*5))

    add_btn.draw((mode_window.rect_window.x+
                    mode_window.rect_window.w*0.6,
                    mode_window.rect_window.y+
                    mode_window.rect_window.h*0.05 + 
                    board_text.get_height()*1.25))
    sub_btn.draw((mode_window.rect_window.x+
                    mode_window.rect_window.w*0.675,
                    mode_window.rect_window.y+
                    mode_window.rect_window.h*0.05 + 
                    board_text.get_height()*1.25))
    mul_btn.draw((mode_window.rect_window.x+
                    mode_window.rect_window.w*0.75,
                    mode_window.rect_window.y+
                    mode_window.rect_window.h*0.05 + 
                    board_text.get_height()*1.25))
    div_btn.draw((mode_window.rect_window.x+
                    mode_window.rect_window.w*0.825,
                    mode_window.rect_window.y+
                    mode_window.rect_window.h*0.05 + 
                    board_text.get_height()*1.25))
    random_btn.draw((mode_window.rect_window.x+
                    mode_window.rect_window.w*0.9,
                    mode_window.rect_window.y+
                    mode_window.rect_window.h*0.05 + 
                    board_text.get_height()*1.25))
    
    none_btn.draw((mode_window.rect_window.x+
                    mode_window.rect_window.w*0.525,
                    mode_window.rect_window.y+
                    mode_window.rect_window.h*0.05 + 
                    board_text.get_height()*3.5))
    naturals_btn.draw((mode_window.rect_window.x+
                    mode_window.rect_window.w*0.6,
                    mode_window.rect_window.y+
                    mode_window.rect_window.h*0.05 + 
                    board_text.get_height()*3.5))
    integers_btn.draw((mode_window.rect_window.x+
                    mode_window.rect_window.w*0.675,
                    mode_window.rect_window.y+
                    mode_window.rect_window.h*0.05 + 
                    board_text.get_height()*3.5))
    rationals_btn.draw((mode_window.rect_window.x+
                    mode_window.rect_window.w*0.75,
                    mode_window.rect_window.y+
                    mode_window.rect_window.h*0.05 + 
                    board_text.get_height()*3.5))
    radicals_btn.draw((mode_window.rect_window.x+
                    mode_window.rect_window.w*0.825,
                    mode_window.rect_window.y+
                    mode_window.rect_window.h*0.05 + 
                    board_text.get_height()*3.5))
    polynomial_btn.draw((mode_window.rect_window.x+
                    mode_window.rect_window.w*0.9,
                    mode_window.rect_window.y+
                    mode_window.rect_window.h*0.05 + 
                    board_text.get_height()*3.5))