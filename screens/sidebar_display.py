import pygame
import sys
from assets import play_icon, online_icon, option_icon, help_icon, exit_icon
from objects import *
from ui_class.colors import OAR_BLUE
from display_constants import SIDE_MENU_RECT_ACTIVE, SCREEN_WIDTH, SCREEN_HEIGHT, screen
from ui_class.main_menu import SELECTED, NORMAL, HOVERED

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

buffering_icon = pygame.transform.smoothscale(ICON_BUFFERING, (int(multi_join_btn.height*2), int(multi_join_btn.height*2)))   
rot_idx = 360

def multi_window():

    global rot_idx
    multi_join_btn.draw(((sidebar.sidebar_rect.width + 
            (SCREEN_WIDTH-sidebar.sidebar_rect.width) - 
            (SCREEN_WIDTH-sidebar.sidebar_rect.width)/10 - 
            btn_size[0]), 
            SCREEN_HEIGHT*0.85))
    
    window_text = pygame.font.Font('font/CookieRun_Regular.ttf', int(multi_join_btn.height*0.6))
    window_text_surface = window_text.render("Searching for available matches...", True, OAR_BLUE)
    screen.blit(window_text_surface, (mode_window.rect_window.x + mode_window.rect_window.w*0.5 - window_text_surface.get_width()*0.5,
                mode_window.rect_window.y+(mode_window.rect_window.h*0.55)))

    #NOTE: a make-do rotate function for now as I can't seem to move the previously instantiated tween object and it only stays in the middle of the screen
    rotated_image = pygame.transform.rotate(buffering_icon, rot_idx)
    centered = rotated_image.get_rect(center=(mode_window.rect_window.x + mode_window.rect_window.w*0.5, mode_window.rect_window.y+(mode_window.rect_window.h*0.45)))
    screen.blit(rotated_image, centered)
    
    if rot_idx < 0:
        rot_idx = 360
    else:
        rot_idx-=4

def title_up_display(fade_screen):
    """
    For moving the title img up + fade animation 
    """

    title_surface.fill(OAR_BLUE)
    title_surface.set_colorkey(OAR_BLUE)
    anim_title_up.update()
    if anim_title_up.IsFinished:
        fade_screen.full_fade()  
    title.display()
    screen.blit(title_surface, (((SCREEN_WIDTH-sidebar.sidebar_rect.w)//2)+
            sidebar.sidebar_rect.w-title_surface.get_width()//2, 0))

def title_upper(func=None):

    if anim_title_down.IsFinished:
        anim_title_upper.play()
        if anim_title_upper.IsFinished:
            anim_title_down.reset()

    mode_window.rect_window.wupdate(x=sidebar.sidebar_rect.w+
                (0.05*SCREEN_WIDTH),y=title.y+TITLE.get_height()*2,
                width=SCREEN_WIDTH-(0.05*SCREEN_WIDTH)-
                (sidebar.sidebar_rect.w+(0.05*SCREEN_WIDTH)),
                height=SCREEN_HEIGHT*0.8-(title.y+TITLE.get_height()*2))
    mode_window.rect_window.draw()

    if anim_title_upper.IsFinished:
        if func is not None:
            func()

# target_functions = {
#     "sb_play": sidebar.get_option("sb_play").target,
#     "sb_online": sidebar.get_option("sb_online").target,
#     "sb_help": sidebar.get_option("sb_help").target,
#     "sb_options": sidebar.get_option("sb_options").target,
#     "sb_exit": sidebar.get_option("sb_exit").target
# }

# def sidebar_display(func_called):

#     for id in target_functions.keys():
#         if target_functions[id] == func_called:
#             target_functions[id] = None
#             sidebar.get_option(id).target = None
#         else:
#             sidebar.get_option(id).target = target_functions[id]

#     if func_called == title:
#         for opt in sidebar.options.keys():
#             if sidebar.get_option(opt).state == SELECTED:
#                 sidebar.update_options_state(opt, NORMAL)

#     mx, my = pygame.mouse.get_pos() # gets the curent mouse position
#     if sidebar.sidebar_rect.collidepoint((mx, my)):
#         sidebar.set(state=HOVERED)
#         for opt in sidebar.options.keys():
#             if sidebar.get_option(opt).get_rect().collidepoint((mx, my)):
#                 if pygame.mouse.get_pressed()[0]:
#                     sidebar.update_options_state(opt, SELECTED)
#                     sidebar.get_option(opt).call_target()
#                 else:
#                     sidebar.update_options_state(opt, HOVERED)
#             else:
#                 if sidebar.get_option(opt).state != SELECTED:
#                     sidebar.update_options_state(opt, NORMAL)
#     else:
#         sidebar.set(state=NORMAL)
#     