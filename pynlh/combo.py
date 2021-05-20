from random import randint

from .card import Card
from .rank import Rank
from .suit import Suit


class ComboError(Exception):
    def __init__(self, combo: 'Combo', msg: str = 'Not a valid combo!'):
        """
        Exception class pf pynlh's Combo class.
        """
        self.combo_str = combo.input
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"'{self.combo_str}' -> {self.msg}"


class Combo():
    def __init__(self,
                 input: str,
                 freq: float = 100.00,
                 ) -> None:
        """
        Pynlh's Combo class object.
        Can be instantiated giving it a input like "Ac5d".
        """
        self.input = input
        self.card1: Card = Card(Rank(input[0]), Suit(input[1]))
        self.card2: Card = Card(Rank(input[2]), Suit(input[3]))
        self._reorder_cards()
        self.freq = freq

    @classmethod
    def new(cls,
            input: str,
            freq: float = 100.00,
            ) -> "Combo":
        """ Alternative constructor for Combo class.
        Not used at the moment."""
        return cls(input, freq)

    def __repr__(self) -> str:
        return f"Combo('{self.input}')"

    def __str__(self) -> str:
        return self.input

    def __eq__(self, other: 'Combo') -> bool:
        if self.__class__ is not other.__class__:
            return NotImplemented
        return (self.card1 == other.card1) and (self.card2 == other.card2)

    def __gt__(self, other: 'Combo') -> bool:
        if self.__class__ is not other.__class__:
            return NotImplemented
        if (self.card1 == self.card2) and (other.card1 != other.card2):
            return True
        if self.card1 != other.card1:
            return self.card1 > other.card1
        else:
            return self.card2 > other.card2

    def apply_rng(self) -> bool:
        if self.freq == 100:
            return True
        random_int = randint(0, 100)
        return self.freq >= random_int

    def _reorder_cards(self):
        pass


class SuitedCombo(Combo):
    pass


class OffsuitCombo(Combo):
    pass


class PairCombo(Combo):
    pass
