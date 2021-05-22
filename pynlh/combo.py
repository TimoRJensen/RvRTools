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
        Pynlh's Combo class.
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
        if self.freq == 100:
            return f"Combo('{str(self)}')"
        else:
            return f"Combo('{str(self)}', freq={self.freq})"

    def __str__(self) -> str:
        if self.freq == 100:
            return str(self.card1) + str(self.card2)
        else:
            return (f"[{self.freq}]{str(self.card1) + str(self.card2)}"
                    + f"[/{self.freq}]")

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

        if self.card1 < self.card2:
            self._switch_cards()
        elif self.card1 == self.card2:
            if self.card1.suit.order > self.card2.suit.order:
                self._switch_cards()

    def _switch_cards(self):
        c1 = self.card2
        c2 = self.card1
        self.card1 = c1
        self.card2 = c2


class SuitedCombo(Combo):
    pass


class OffsuitCombo(Combo):
    pass


class PairCombo(Combo):
    pass
