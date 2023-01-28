"""
Saves options to file.
"""

import os
from configparser import ConfigParser

OPTIONS_FILE = 'options.conf'

# Dictionary
enableDebugMode = 'enableDebugMode'
enableAnimations = 'enableAnimations'
cursorColor = 'cursorColor'
port = 'port'
showConsole = 'showConsole'
chipMoveAnimationSpeed = 'chipMoveAnimationSpeed'
showIndicators = 'showIndicators'
musicVolume = 'musicVolume'
soundVolume = 'soundVolume'

DEFAULT_OPTIONS = {
    enableDebugMode : 'False',
    enableAnimations : 'True',
    cursorColor : '255, 255, 255',
    port : '8180',
    showConsole : 'False',
    chipMoveAnimationSpeed : '0.5',
    showIndicators : 'True',
    musicVolume : '100',
    soundVolume : '100'
}

def is_bool(value):
    """
    Check if the given value is a boolean.
    """
    if type(value) == bool:
        return True
    return False

def to_bool(value: str) -> bool:
    """
    Converts a 'True' or 'False' string into its appropriate bool value.
    Returns the value itself if invalid.
    """
    if value == 'True':
        return True
    if value == 'False':
        return False
    return value

"""
Import this file and use the instantiated 'Options' class to access the different
options and methods.

e.g.
from options import *

# Usage in if statements
if Options.enableDebugMode:
    print("Debug mode is enabled.")

# Getting values
Options.get(soundVolume)

# Saving values (must be string)
Options.set_value(enableDebugMode, 'False')
Options.set_value(cursorColor, '219, 156, 112') # Tuple without parentheses
Options.set_value(musicVolume, '75')
"""

class Config:
    """
    Options.    
    """

    def __init__(self, filepath):
        self.filepath = filepath    
        self.config = ConfigParser()
        self.config.optionxform = str   # Makes config parse case-sensitive
        self.section = 'options'
        self.options = {}

        if not os.path.isfile(filepath):
            self.create_config()

        try:
            with open(filepath) as fp:
                self.config.read_file(fp)
                self.update_from_config()
        except:
            print(f"Error reading file {filepath}.\nCreating new config file...")
            os.remove(filepath)
            self.create_config()

    def update_from_config(self):
        """
        Updates the class' options from the 'options.ini' file.
        """
        for option in self.config[self.section]:
            self.options[option] = self.config[self.section][option]
        self.update()

    def update(self):
        """
        Updates all instance variables so options can be accessed by the class' members.
        This checks for invalid values in the file and sets it to default.
        """
        if not is_bool(to_bool(self.options[enableDebugMode])):
            self.enableDebugMode = self.set_value(enableDebugMode, DEFAULT_OPTIONS[enableDebugMode])
        else:
            self.enableDebugMode = to_bool(self.options[enableDebugMode])

        if not is_bool(to_bool(self.options[enableAnimations])):
            self.enableAnimations = self.set_value(enableAnimations, DEFAULT_OPTIONS[enableAnimations])
        else:
            self.enableAnimations = to_bool(self.options[enableAnimations])

        if not is_bool(to_bool(self.options[showConsole])):
            self.showConsole = self.set_value(showConsole, DEFAULT_OPTIONS[showConsole])
        else:
            self.showConsole = to_bool(self.options[showConsole])

        if not is_bool(to_bool(self.options[showIndicators])):
            self.showIndicators = self.set_value(showIndicators, DEFAULT_OPTIONS[showIndicators])
        else:
            self.showIndicators = to_bool(self.options[showIndicators])

        try:
            self.cursorColor = tuple(map(int, (self.options[cursorColor].split(','))))
        except:
            #TODO: this is gonna return an error when used
            self.cursorColor = self.set_value(cursorColor, DEFAULT_OPTIONS[cursorColor])

        try:
            self.port = int(self.options[port])
        except:
            self.port = int(self.set_value(port, DEFAULT_OPTIONS[port]))
            
        try:
            self.chipMoveAnimationSpeed = float(self.options[chipMoveAnimationSpeed])
        except:
            self.chipMoveAnimationSpeed = float(self.set_value(chipMoveAnimationSpeed, DEFAULT_OPTIONS[chipMoveAnimationSpeed]))

        try:
            self.musicVolume = int(self.options[musicVolume])
        except:
            self.musicVolume = int(self.set_value(musicVolume, DEFAULT_OPTIONS[musicVolume]))

        try:
            self.soundVolume = int(self.options[soundVolume])
        except:
            self.soundVolume = int(self.set_value(soundVolume, DEFAULT_OPTIONS[soundVolume]))

    def read_all(self):
        list_of_value = []
        for key in self.config[self.section]:
            list_of_value.append(self.config[self.section][key])
        return list_of_value

    def change_section(self, section: str):
        self.section = section
    
    def update_config(self, option, value: str):
        """
        Saves option value to the file.
        """
        with open(self.filepath, "w") as f:
            self.config[self.section][option] = value
            self.config.write(f)
    
    def update_config_all(self):
        """
        Saves all instance options to the file.
        """
        with open(self.filepath, "w") as f:
            for option in self.options:
                self.config[self.section][option] = self.options[option]
            self.config.write(f)

    def create_config(self):
        """
        Creates a new 'options.conf' file with default values.
        """
        with open(self.filepath, "x") as f:
            try:
                self.config.add_section('options')
            except:
                self.create_config()
            
            for option in DEFAULT_OPTIONS:
                self.config[self.section][option] = DEFAULT_OPTIONS[option]
            self.config.write(f)
        self.update_from_config()

    def get(self, option):
        return self.options[option]
    
    def set_value(self, option, value: str):
        """
        Set option value.
        Args:
        option: 
        """
        self.options[option] = value
        self.update_config(option, value)
        self.update()
        return value

Options = Config(OPTIONS_FILE)