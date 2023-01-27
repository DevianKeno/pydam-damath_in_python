"""
Default game options.
"""

enableDebugMode = 'enableDebugMode'
enableAnimations = 'enableAnimations'
cursorColor = 'cursorColor'
port = 'port'
chipMoveAnimationSpeed = 'chipMoveAnimationSpeed'
showIndicators = 'showIndicators'

from configparser import ConfigParser

class Config:
    """
    Global game settings.
    """

    def __init__(self) -> None:
        self.config = ConfigParser()

        try:
            open('config.txt')
        except:
            print("no config lmao where did u put it haha")
            # Create
        try:
            self.config.read('config.txt')
        except:
            print("tite")

        self.enableDebugMode = bool(self.config.get('options', 'enableDebugMode'))
        self.enableAnimations = bool(self.config.get('options', 'enableAnimations'))
        self.cursorColor = tuple(map(int, (self.config.get('options', 'cursorColor').split(','))))
        self.port = int(self.config.get('options', 'port'))
        self.chipMoveAnimationSpeed = float(self.config.get('options', 'chipMoveAnimationSpeed'))
        self.showIndicators = bool(self.config.get('options', 'showIndicators'))

    def init(self):
        print('')

    def _save(self):
        self.config.add_section('options')
        pass


    def set(self, option, value):
        match option:
            case 'enableDebugMode':
                self.enableDebugMode = value
            case 'enableAnimations':
                self.enableAnimations = value
            case 'cursorColor':
                self.cursorColor = value
            case 'port':
                self.port = value
            case 'chipMoveAnimationSpeed':
                self.chipMoveAnimationSpeed = value
            case 'showIndicators':
                self.showIndicators = value

if __name__ == '__main__':

    Options = Config()


enableDebugMode = False

allowPromotion = True
allowCapture = True
allowChainCapture = True
allowMandatoryCapture = True

allowMovementOfOpponentPieces = False
allowCheats = True

enableTimer = True
timerDefaultTurn = 60
timerDefaultGlobal = 1200

enableTouchMove = True
enableActions = True
enableAnimations = True

chipMoveAnimationSpeed = 0.5
maxBufferSize = 1024

# Default values

board_symbols = []


_MODES = [
    'Naturals', 'Integers', 
    'Rationals', 'Radicals', 
    'Polynomials'
    ]

MODE = _MODES[1]

versusAI = True

