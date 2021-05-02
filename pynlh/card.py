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


class Card():
    def __init__(self,
                 rank: Rank,
                 suit: Suit,
                 ) -> None:
        self.rank = rank
        self.suit = suit
        if (rank not in RANKS) or (suit not in SUITS):
            raise CardError(self)


CARDS = []
for rank in RANKS:
    for suit in SUITS:
        CARDS.append(Card(rank, suit))
