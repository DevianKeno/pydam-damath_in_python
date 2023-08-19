

from options import *

class Statistics:

    def __init__(self) -> None:
        self.total_score = 0
        self.cumulative_score = []

        self.total_turns = 0 
        self.total_moves = 0
        self.moves = []
        
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
        """
        Represents a move.
        """

        def __init__(self) -> None:
            self.piece = None
            self.score_attained = 0