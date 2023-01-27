class Ruleset:
    """
    Rules to be used for match instances.
    """

    def __init__(self) -> None:
        """
        A standard ruleset inherits the default rules of Classic Damath.
        """
        
        self.players_count = 2
        self.IsCustom = False
        self.set_classic()

    def get_rulestr(self) -> str:
        """
        Returns the ruleset as a string.
        """

        rule_str = "{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}".format(
                    self.mode,
                    self.symbolAdd,
                    self.symbolSubtract,
                    self.symbolMultiply,
                    self.symbolDivide,
                    self.symbolRandom,
                    self.piece_values,
                    self.allowPromotion,
                    self.allowCapture,
                    self.allowChainCapture,
                    self.allowMandatoryCapture,
                    self.enableTimer,
                    self.timer_turn,
                    self.timer_global,
                    self.allowActions ,
                    self.allowCheats ,
                    self.ai
                    )

        return rule_str

    def set_mode(self, mode: str):
        """
        Sets rules based on passed mode.
        - Classic
        - Speed
        - Checkers
        """

        match mode:
            case "Classic" | "classic":
                self.set_classic()
            case "Speed" | "speed":
                self.set_speed()
            case "Checkers" | "checkers":
                self.set_checkers()

    def set_rulestr(self, ruleset: str):
        """
        Sets ruleset based on string.
        """

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

