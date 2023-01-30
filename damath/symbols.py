import pygame
from damath.constants import COLS, ROWS
from damath.ruleset import Rules
from ui_class.font import *
from ui_class.colors import *
from display_constants import screen
from objects import selection_guide_rect, square_size, chips_surface

def get_xy_from_cell(tile: tuple):
    """
    Returns x and y coordinates from board relative coordinates.
    """
    col, row = tile
    
    x = (col * square_size)
    y = (abs(row - 7) * square_size)

    return x, y

class Symbol:

    def __init__(self) -> None:
        self._surface = chips_surface
        self.symbol_map = {}
        self.symbol_pos_map = {}
        self.add = '' 
        self.subtract = ''
        self.multiply = ''
        self.divide = ''

        self.font = pygame.font.Font(Hitmo_Black, int(square_size*1.25))

        self.init()
        self.generate()
        self.calculate_positions()
        self.align_center()

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, value: pygame.Surface):
        self._surface = value

    def init(self):
        if Rules.symbolAdd:
            self.add = '+'
        if Rules.symbolSubtract:
            self.subtract = '-'
        if Rules.symbolMultiply:
            self.multiply = '×'
        if Rules.symbolDivide:
            self.divide = '÷'

        if not Rules.symbolRandom:
            self.symbol_set_one = [self.subtract, self.multiply, self.subtract, self.multiply]
            self.symbol_set_two = [self.add, self.divide, self.add, self.divide]
        else:
            self.symbol_set_one = [self.subtract, self.multiply, self.subtract, self.multiply]
            self.symbol_set_two = [self.add, self.divide, self.add, self.divide]

    def calculate_positions(self):
        for key in self.symbol_map:
            col, row = key
            self.symbol_pos_map.update({(col, row):get_xy_from_cell((col, row))})
            

    def align_center(self):
        for key in self.symbol_pos_map:
            text_symbol = self.font.render(self.symbol_map[key], True, BLACK)
            text_symbol_rect = text_symbol.get_rect(centerx = (self.symbol_pos_map[key][0] + (square_size//2)),
                                                    centery = (self.symbol_pos_map[key][1] + (square_size//2) + text_symbol.get_height()*0.075 ))
            self.symbol_pos_map.update({key: (text_symbol_rect.x, text_symbol_rect.y)})

    def generate(self):
        """
        Generates the symbol_map dictionary.
        
        Keys are tiles relative to the board.
        """
        for col in range(COLS):
            symbol_counter = 0

            if col == 4:
                self.symbol_set_one.reverse()
                self.symbol_set_two.reverse()

            for row in range(0, ROWS):
                if (col % 2 == 0):
                    row += 1
                    if (row % 2 == 0):
                        self.symbol_map.update('')
                        continue
                else:
                    if not (row % 2 == 0):
                        self.symbol_map.update('')
                        continue

                match col:
                    case 0 | 3:
                        self.symbol_map.update({(col, row):self.symbol_set_one[symbol_counter]})
                        symbol_counter += 1
                    case 1 | 2:
                        self.symbol_map.update({(col, row):self.symbol_set_two[symbol_counter]})
                        symbol_counter += 1
                    case 4 | 7:
                        self.symbol_map.update({(col, row):self.symbol_set_one[symbol_counter]})
                        symbol_counter += 1
                    case 5 | 6:
                        self.symbol_map.update({(col, row):self.symbol_set_two[symbol_counter]})
                        symbol_counter += 1

    def draw(self):
        for key in self.symbol_map:
            text_symbol = self.font.render(self.symbol_map[key], True, DARK_GRAY_BLUE)
            self._surface.blit(text_symbol, self.symbol_pos_map[key])