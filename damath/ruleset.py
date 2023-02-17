from .rules import *


class Ruleset:
    """
    Rules to be used for match instances.
    """

    def __init__(self) -> None:
        """
        A standard ruleset inherits the default rules of Classic Damath.
        """
        
        self.players_count = 2
        self.IsVersusAI = True
        self.IsCustom = False
        self.IsMultiplayer = False
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
                    self.allowActions,
                    self.allowCheats,
                    self.ai
                    )

        return rule_str

    def set_rulestr(self, rulestr: str):
        """
        Sets ruleset based on string.
        """

        rulestr_backup = self.get_rulestr()
        
        try:
            rules = rulestr.split()
            self.mode = rules[0]
            self.symbolAdd = rules[1]
            self.symbolSubtract = rules[2]
            self.symbolMultiply = rules[3]
            self.symbolDivide = rules[4]
            self.symbolRandom = rules[5]
            self.piece_values = rules[6]
            self.allowPromotion = rules[7]
            self.allowCapture = rules[8]
            self.allowChainCapture = rules[9]
            self.allowMandatoryCapture = rules[10]
            self.enableTimer = rules[11]
            self.timer_turn = rules[12]
            self.timer_global = rules[13]
            self.allowActions = rules[14]
            self.allowCheats = rules[15]
            self.ai = rules[16]
        except:
            print("Invalid rulestr set!")
            self.set_rulestr(rulestr_backup)

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
        
        self.ai = "Xena"

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

    def toggle_actions(self):
        self.allowActions = not self.allowActions

    def toggle_cheats(self):
        self.allowCheats = not self.allowCheats

    def set_rule(self, rule: str, value):
        """
        Set a single rule option.
        """
        
        try:
            match rule:
                case "mode":
                    self.mode = value
                case "symbolAdd":
                    self.symbolAdd = value
                case "symbolAdd":
                    self.symbolAdd = value
                case "symbolSubtract":
                    self.symbolSubtract = value
                case "symbolMultiply":
                    self.symbolMultiply = value
                case "symbolDivide":
                    self.symbolDivide = value
                case "symbolRandom":
                    self.symbolRandom = value
                case "piece_values":
                    self.piece_values = value
                case "allowPromotion":
                    self.allowPromotion = value
                case "allowCapture":
                    self.allowCapture = value
                case "allowChainCapture":
                    self.allowChainCapture = value
                case "allowMandatoryCapture":
                    self.allowMandatoryCapture = value
                case "enableTimer":
                    self.enableTimer = value
                case "timer_turn":
                    self.timer_turn = value
                case "timer_global":
                    self.timer_global = value
                case "allowActions":
                    self.allowActions = value
                case "allowCheats":
                    self.allowCheats = value
                case "ai":
                    self.ai = value
        except:
            print("Invalid rule value.")

    def toggle_multiplayer(self):
        self.IsMultiplayer = not self.IsMultiplayer


Rules = Ruleset()