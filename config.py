"""
Config file.
"""

from configparser import ConfigParser
import os

# Dictionary
enableDebugMode = 'enableDebugMode'
enableAnimations = 'enableAnimations'
cursorColor = 'cursorColor'
port = 'port'
showConsole = 'showConsole'
chipMoveAnimationSpeed = 'chipMoveAnimationSpeed'
showIndicators = 'showIndicators'

DEFAULT_OPTIONS = {
    enableDebugMode : 'False',
    enableAnimations : 'True',
    cursorColor : '255, 255, 255',
    port : '8180',
    showConsole : 'False',
    chipMoveAnimationSpeed : '0.5',
    showIndicators : 'True'
}

def is_bool(value: str):
    if type(value) == bool:
        return True
    return False

def to_bool(value: str) -> bool:
    """Converts a 'True' or 'False' string into
    its appropriate bool value.
    Returns the value if invalid.
    """
    if value == 'True':
        return True
    if value == 'False':
        return False
    return value


class Config:

    def __init__(self, filepath):
        self.filepath = filepath    
        self.config = ConfigParser()
        self.config.optionxform = str   # Makes config parse case-sensitive
        self.section = 'options'
        self.options = {}

        if not os.path.isfile(filepath):
            self.create_config()
        self.read(filepath)

        try:
            self.update_from_config()
        except:
            print(f"Error reading file {filepath}.\nCreating new config file...")
            os.remove(filepath)
            self.create_config()

    def update_from_config(self):
        """Updates the class' options from the 'options.ini' file.
        """
        for option in self.config[self.section]:
            self.options[option] = self.config[self.section][option]
        self.update()

    def update(self):
        """Updates the instance variables.
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
            self.cursorColor = self.set_value(cursorColor, DEFAULT_OPTIONS[cursorColor])

        try:
            self.port = int(self.options[port])
        except:
            self.port = self.set_value(port, DEFAULT_OPTIONS[port])
            
        try:
            self.chipMoveAnimationSpeed = float(self.options[chipMoveAnimationSpeed])
        except:
            self.chipMoveAnimationSpeed = self.set_value(chipMoveAnimationSpeed, DEFAULT_OPTIONS[chipMoveAnimationSpeed])

    def read(self, filepath: str):
        self.config.read(filepath)

    def read_all(self):
        list_of_value = []
        for key in self.config[self.section]:
            list_of_value.append(self.config[self.section][key])
        return list_of_value

    def change_section(self, section: str):
        self.section = section
    
    def update_config(self, option, value: str):
        """Saves option value to the file.
        """
        with open(self.filepath, "w") as f:
            self.config[self.section][option] = value
            self.config.write(f)
    
    def update_config_all(self):
        """Saves all instance options to the file.
        """
        with open(self.filepath, "w") as f:
            for option in self.options:
                self.config[self.section][option] = self.options[option]
            self.config.write(f)

    def create_config(self):
        with open(self.filepath, "x") as f:
            self.config.add_section('options')
            for option in DEFAULT_OPTIONS:
                self.config[self.section][option] = DEFAULT_OPTIONS[option]
            self.config.write(f)

    def get_value(self, option):
        return self.config[self.section][option]
    
    def set_value(self, option, value):
        """Set option value.
        """
        self.options[option] = value
        self.update_config(option, value)
        self.update()
        return value

Options = Config("option.conf")