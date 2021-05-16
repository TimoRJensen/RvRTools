from random import randint

from .abstracts import PynlhComponent
from .rank import Rank
from .suit import Suit


class Combo(PynlhComponent):
    def __init__(self,
                 combo_str: str = None,
                 freq: float = 100.00,
                 ) -> None:
        """
        Pynlh's Combo class object.
        Can be instantiated giving it a combo_str like "Ac5d".
        """
        self.combo_str = combo_str
        self.rank1 = Rank(combo_str[0])
        self.rank2 = Rank(combo_str[2])
        self.suit1 = Suit(combo_str[1])
        self.suit2 = Suit(combo_str[3])
        self.freq = freq

    def __repr__(self) -> str:
        return f"Combo('{self.combo_str}')"

    def __str__(self) -> str:
        return self.combo_str

    def apply_rng(self) -> bool:
        if self.freq == 100:
            return True
        random_int = randint(0, 100)
        return self.freq >= random_int

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
