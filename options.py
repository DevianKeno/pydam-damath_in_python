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

board_symbols = []


_MODES = [
    'Naturals', 'Integers', 
    'Rationals', 'Radicals', 
    'Polynomials'
    ]

MODE = _MODES[1]

versusAI = True

