




class Player:

    def __init__(self, name="") -> None:
        self.name = name
        self.stats = Statistics()

class Statistics:

    def __init__(self) -> None:
        self.total_score = 0
        self.cumulative_score = []

        self.total_moves = 0
        self.total_moves_including_chains = 0
        
        self.capture_scores = []
        self.highest_single_capture_score = 0
        
        self.chain_capture_scores = [[]]
        self.highest_chain_capture_score = 0

        self.captures = []
        self.captured_pieces_count = 0
        self.captured_kings_count = 0

        self.pieces_left = []

        # In seconds
        self.average_time_per_turn = 0 
        self.total_time_used = 0

class Move:

    def __init__(self) -> None:
        self.player = 0