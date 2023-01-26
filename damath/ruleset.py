class Ruleset:
    """
    Rules to be used for match instances.
    """

    def __init__(self) -> None:
        """
        A standard ruleset inherits the default rules of Classic Damath.
        """
        
        self.players_count = 2
        self.set_classic()

    def set(self, mode: str):
        """
        Sets rules based on passed mode.
        - Classic
        - Speed
        - Checkers
        """

        match mode:
            case "Classic":
                self.set_classic()
            case "Speed":
                self.set_speed()
            case "Checkers":
                self.set_checkers()

    def set_classic(self):
        """
        Set rules for Classic Damath.
        """

        self.mode = "Classic"

        self.board_symbols = ['+', '-', 'x', '÷']
        self.symbolAdd = True
        self.symbolSubtract = True
        self.symbolMultiply = True
        self.symbolDivide = True
        self.symbolRandom = False

        self.piece_values = "Integers"
        self.allowPromotion = True
        self.allowCapture = True
        self.allowChainCapture = True
        self.allowMandatoryCapture = True

        self.enableTimer = True
        self.timer_turn = 60
        self.timer_global = 1200

        self.allowActions = True
        self.allowCheats = False
        
        self.ai = None

    def set_speed(self):
        """
        Set rules for Speed Damath.
        """

        self.mode = "Speed"

        self.board_symbols = ['+', '-', 'x', '÷']
        self.symbolAdd = True
        self.symbolSubtract = True
        self.symbolMultiply = True
        self.symbolDivide = True
        self.symbolRandom = False

        self.piece_values = "Integers"
        self.allowPromotion = True
        self.allowCapture = True
        self.allowChainCapture = True
        self.allowMandatoryCapture = True

        self.enableTimer = True
        self.timer_turn = 15
        self.timer_global = 300

        self.allowActions = True
        self.allowCheats = False
        
        self.ai = None

    def set_checkers(self):
        """
        Set rules for Checkers.
        """
        
        self.mode = "Checkers"

        self.board_symbols = []
        self.symbolAdd = False
        self.symbolSubtract = False
        self.symbolMultiply = False
        self.symbolDivide = False
        self.symbolRandom = False

        self.piece_values = None
        self.allowPromotion = True
        self.allowCapture = True
        self.allowChainCapture = True
        self.allowMandatoryCapture = True

        self.enableTimer = False
        self.timer_turn = 0
        self.timer_global = 0

        self.allowActions = True
        self.allowCheats = False
        
        self.ai = None

