from functools import total_ordering
from typing import List

from .rank import RANKS
from .suit import SUITS
from .combo import Combo

"""
Version: 0.02

Author: GTOHOLE 11-20
"""


class HandError(Exception):
    """
    Exception class of pynlh's Hand class.
    """
    pass

    def __init__(self, handstring, msg='Not a valid hand!'):
        self.handstring = handstring
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"'{self.handstring}' -> {self.msg}"


@total_ordering
class Hand():

    # TODO a Hand ordering à la 22 > AKs > AK > AKo > AQs
    def __init__(self,
                 handstring: str = None,
                 hand: str = None,
                 hand_type: str = None,
                 freq: float = 100.00,
                 ) -> None:
        """
        Pynlh's Hand class.
        Can be instantiated either by giving it a "handstring" like "AKs"
        or a "hand" like "AK" and a "hand_type" like "offsuit", "suited,
        "nosuit" or "pair".
        """
        self.hand = hand
        self.hand_type = hand_type
        self.handstring = handstring
        self.freq = freq
        self._set_default_values()
        try:
            self.rank1 = RANKS[self.hand[0]]
            self.rank2 = RANKS[self.hand[1]]
        except KeyError or TypeError:
            raise HandError(self.handstring)
        self.class_skl_mal = self.get_sklansky_malmuth_handclass()

    @property
    def all_combos_str(self):
        cards_list = []
        rv = []
        for suit in SUITS:
            for rank in self.hand:
                cards_list.append(rank+suit)
        for card1 in cards_list:
            for card2 in cards_list:
                if ((card1 != card2) and (card1[0] == self.hand[0]) and
                        (card2[0] == self.hand[1]) and
                        ((card1+card2) not in rv) and (card2+card1) not in rv):
                    rv.append(card1+card2)
        if self.hand_type == 'pair':
            rv = [c for c in rv if c[0] == c[2]]
        elif self.hand_type == 'suited':
            rv = [c for c in rv if c[1] == c[3]]
        elif self.hand_type == 'offsuit':
            rv = [c for c in rv if (c[0] != c[2]) and (c[1] != c[3])]
        elif self.hand_type == 'nosuit':
            rv = [c for c in rv if (c[0] != c[2])]
        return rv

    @property
    def combos(self) -> List[Combo]:
        return [Combo(combo_str=combo, freq=self.freq)
                for combo in self.all_combos_str]

    @property
    def index_x(self):
        """
        Property X-Index (The Position from left to right.)
        "Nosuit" hands will be treated as "offsuit" hands.
        """
        if self.hand_type == 'suited':
            return self.rank2.order
        if self.hand_type in ['offsuit', 'nosuit', 'pair']:
            return self.rank1.order

    @property
    def index_y(self):
        """
        Property Y-Index (The Position top left to bottom.)
        "Nosuit" hands will be treated as "offsuit" hands.
        """
        if self.hand_type == 'suited':
            return self.rank1.order
        elif self.hand_type in ['offsuit', 'nosuit', 'pair']:
            return self.rank2.order

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Hand):
            return NotImplemented
        return self.handstring == o.handstring

    def __gt__(self, o: object) -> bool:
        if not isinstance(o, Hand):
            return NotImplemented

        if self.hand_type == 'pair' and o.hand_type != 'pair':
            return True
        elif self.rank1 < o.rank1:
            return False
        elif self.rank1 > o.rank1:
            return True
        elif self.rank1 == o.rank1 and self.rank2 < o.rank2:
            return False
        elif self.rank1 == o.rank1 and self.rank2 > o.rank2:
            return True
        elif ((self.hand_type == 'suited') and
              (o.hand_type in ['offsuit', 'nosuit'])):
            return True
        elif self.hand_type == 'nosuit' and o.hand_type == 'offsuit':
            return True
        else:
            return False

    def __len__(self) -> int:
        return len(self.handstring)

    def __repr__(self) -> str:
        return f"Hand('{self.handstring}')"

    def __str__(self) -> str:
        return(self.handstring)

    def _set_default_values(self):
        if self.handstring is not None:
            new_handstring = ''
            for i, chr in enumerate(self.handstring):
                new_handstring += chr.upper() if i < 2 else chr.lower()
            self.handstring = new_handstring
            self.hand_type = self.evaluate_hand_type_from_handstring()
            self.hand = self.eval_hand_from_handstring()
        else:
            if (self.hand is None) or (self.hand_type is None):
                raise HandError('You cannot enter a hand without a hand_type.')
            self.hand = self.hand.upper()
            self.hand_type = self.hand_type.lower()
            self.handstring = self.eval_handstring()

    def eval_hand_from_handstring(self):
        return self.handstring[0:2]

    def eval_handstring(self):
        if self.hand_type in ['pair', 'nosuit']:
            return self.hand.upper()
        elif self.hand_type in ['suited', 'offsuit']:
            return self.hand.upper() + self.hand_type[0]

    def evaluate_hand_type_from_handstring(self):
        """
        Evaluates the hand type (suited, offsuit, pair or nosuit) from a given
        handstring (self.handstring).
        """
        hand_str = self.handstring
        if (len(hand_str) == 2) and (hand_str[0] == hand_str[1]):
            return "pair"
        elif len(hand_str) == 2:
            return "nosuit"
        else:
            suit = hand_str[2].lower()
            if suit == "s":
                return "suited"
            elif suit == "o":
                return "offsuit"

    def get_sklansky_malmuth_handclass(self):
        if self.handstring in ["AA", "AKs", "KK", "QQ", "JJ"]:
            return 1
        elif self.handstring in ["AKo", "AQs", "AJs", "KQs", "TT"]:
            return 2
        elif self.handstring in ["AQo", "ATs", "KJs", "QJs", "JTs", "99"]:
            return 3
        elif self.handstring in ["AJo", "KQo", "KTs", "QTs", "J9s", "T9s",
                                 "98s", "88"]:
            return 4
        elif self.handstring in ["A9s", "A8s", "A7s", "A6s", "A5s", "A4s",
                                 "A3s", "A2s", "KJo", "QJo", "JTo", "Q9s",
                                 "T8s", "97s", "87s", "77", "76s", "66", ]:
            return 5
        elif self.handstring in ["ATo", "KTo", "QTo", "J8s", "86s", "75s",
                                 "65s", "55", "54s"]:
            return 6
        elif self.handstring in ["K9s", "K8s", "K7s", "K6s", "K5s", "K4s",
                                 "K3s", "K2s", "J9o", "T9o", "98o", "64s",
                                 "53s", "44", "43s", "33", "22"]:
            return 7
        elif self.handstring in ["A9o", "K9o", "Q9o", "J8o", "J7s", "T8o",
                                 "96s", "87o", "85s", "76o", "74s", "65o",
                                 "54o", "42s", "32s", "K9o", "Q9o", "J8o",
                                 "J7s", "T8o", "96s", "87o", "85s", "76o",
                                 "74s", "65o", "54o", "42s", "32s", "K9o",
                                 "Q9o", "J8o", "J7s", "T8o", "96s", "87o",
                                 "85s", "76o", "74s", "65o", "54o", "42s",
                                 "32s"]:
            return 8
        else:
            return 9

    def pick_combos(self, as_str=False) -> List[Combo]:
        if not as_str:
            return [combo for combo in self.combos if combo.pick()]

        combos_list = [str(combo) for combo in self.combos if combo.pick()]
        return ','.join(combos_list)
