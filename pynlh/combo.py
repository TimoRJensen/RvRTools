from numpy import random
import numpy

from .rank import Rank
from .suit import Suit


class ComboError(Exception):
    pass

    def __init__(self, combo_str: str, msg: str = 'Not a valid combo!'):
        """
        Exception class pf pynlh's Combo class.
        """
        self.combo_str = combo_str
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"'{self.combo_str}' -> {self.msg}"


class Combo():
    def __init__(self,
                 combo_str: str = None,
                 rank1: Rank = None,
                 rank2: Rank = None,
                 suit1: Suit = None,
                 suit2: Suit = None,
                 freq: float = 0.00,
                 ) -> None:
        """
        Pynlh's Combo class object.
        Can be isntanciated either giving it a combo_str like "Ac5d" or
        via Suits and Rank objects.
        """
        self.combo_str = combo_str
        self.rank1 = rank1
        self.rank2 = rank2
        self.suit1 = suit1
        self.suit2 = suit2
        self.freq = freq

    def __repr__(self) -> str:
        return f"Combo(combo_str='{self.combo_str}')"

    def __str__(self) -> str:
        return self.combo_str

    def pick(self) -> bool:
        random_float = numpy.random.uniform(0.01, 100)
        if self.freq == 100:
            return True
        elif self.freq > random_float:
            return True
        else:
            return False
