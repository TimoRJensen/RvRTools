import re
from functools import total_ordering
from .rank import Rank, RANKS
from .suit import Suit, SUITS


class CardError(Exception):
    pass

    def __init__(self, card: 'Card', msg: str = 'Not a valid Card!'):
        """
        Exception class of pynlh's Card class.
        """
        self.card = card
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"'{self.card.rank, self.card.suit}' -> {self.msg}"


@total_ordering
class Card():
    def __init__(self,
                 rank: Rank,
                 suit: Suit,
                 ) -> None:
        self.rank = rank
        self.suit = suit
        if ((not isinstance(self.rank, Rank))
                or (not isinstance(self.suit, Suit))):
            raise CardError

    @classmethod
    def from_str(cls, input: str) -> 'Card':
        rank_suit = re.compile(f'^[{RANKS}][{SUITS}]$', flags=re.IGNORECASE)
        suit_rank = re.compile(f'^[{SUITS}][{RANKS}]$', flags=re.IGNORECASE)
        if rank_suit.match(input):
            return cls(Rank(input[0]), Suit(input[1]))
        if suit_rank.match(input):
            return cls(Rank(input[1]), Suit(input[0]))

    def __eq__(self, other: 'Card') -> bool:
        if self.__class__ is not other.__class__:
            return NotImplemented
        return (self.rank == other.rank) and (self.suit == other.suit)

    def __gt__(self, other: 'Card') -> bool:
        if self.__class__ is not other.__class__:
            return NotImplemented
        if self.rank != other.rank:
            return self.rank < other.rank
        else:
            return self.suit < other.suit


CARDS = []
for rank in RANKS:
    for suit in SUITS:
        CARDS.append(Card.from_str(rank + suit))
