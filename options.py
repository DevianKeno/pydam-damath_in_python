"""
Game options.
"""

enableDebugMode = True

enableMandatoryCapture = True
enableCheats = True
enableTimer = True
enableTouchMove = True
enableActions = True

allowMovementOfOpponentPieces = False

_MODES = [
    'Naturals', 'Integers', 
    'Rationals', 'Radicals', 
    'Polynomials'
    ]

MODE = _MODES[1]

versusAI = False

enableAnimations = True
chipMoveAnimationSpeed = 0.5
maxBufferSize = 1024