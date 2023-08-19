#
#
#

from damath.statistics import *
from options import *

class Player:

    def __init__(self, name=None) -> None:
        if name == None:
            self.name = Options.username
        self.Stats = Statistics()

    @classmethod
    def get_name(self):
        return self.name

    @classmethod
    def set_name(self, value: str):
        self.name = value