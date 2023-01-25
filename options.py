"""
Default game options.
"""

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

boardSymbols = []


_MODES = [
    'Naturals', 'Integers', 
    'Rationals', 'Radicals', 
    'Polynomials'
    ]

MODE = _MODES[1]

versusAI = True


class Rules:
    """
    Rules to be used for match instances.
    """

    def __init__(self) -> None:
        """
        An instantiated match inherits the default rules of Classic Damath.
        """
        
        self.set_classic()

    def set_classic(self):
        """
        Set rules for Classic Damath.
        """

        self.mode = "Classic"

        self.boardSymbols = ['+', '-', 'x', '÷']
        self.symbolAdd = True
        self.symbolSubtract = True
        self.symbolMultiply = True
        self.symbolDivide = True
        self.symbolRandom = False

        self.pieceValues = "Integers"
        self.allowPromotion = True
        self.allowCapture = True
        self.allowChainCapture = True
        self.allowMandatoryCapture = True

        self.timerTurn = 60
        self.timerGlobal = 1200

        self.allowCheats = False
        
        self.ai = None

    def set_speed(self):
        """
        Set rules for Speed Damath.
        """

        self.mode = "Speed"

        self.boardSymbols = ['+', '-', 'x', '÷']
        self.symbolAdd = True
        self.symbolSubtract = True
        self.symbolMultiply = True
        self.symbolDivide = True
        self.symbolRandom = False

        self.pieceValues = "Integers"
        self.allowPromotion = True
        self.allowCapture = True
        self.allowChainCapture = True
        self.allowMandatoryCapture = True

        self.timerTurn = 15
        self.timerGlobal = 300

        self.allowCheats = False
        
        self.ai = None

    def set_checkers(self):
        """
        Set rules for Checkers.
        """
        
        self.mode = "Checkers"

        self.boardSymbols = []
        self.symbolAdd = False
        self.symbolSubtract = False
        self.symbolMultiply = False
        self.symbolDivide = False
        self.symbolRandom = False

        self.pieceValues = None
        self.allowPromotion = True
        self.allowCapture = True
        self.allowChainCapture = True
        self.allowMandatoryCapture = True

        self.timerTurn = 0
        self.timerGlobal = 0

        self.allowCheats = False
        
        self.ai = None

