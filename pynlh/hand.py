from functools import total_ordering
from typing import List, Dict

from .rank import RANKS, Rank
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

    def __init__(self, input: str, freq: float = 0) -> None:
        """Pynlh's Hand Class. Holds a dict of all available Combos with a
           frequency.

        Args:
            input (str): [description]
            freq (float, optional): [description]. Defaults to 0.
        """
        self.input: str = input
        self.freq: float = freq
        self.hand: str = ''  # set by _parse_input()
        self.hand_type: str = ''  # set by _parse_input()
        self.handstring: str = ''  # set by _parse_input()
        self.combos: Dict[Combo] = {}  # set by _parse_input()
        self.rank1: Rank = None  # set by _parse_input()
        self.rank2: Rank = None  # set by _parse_input()
        self.class_skl_mal = self.get_sklansky_malmuth_handclass()

    def __eq__(self, o: 'Hand') -> bool:
        if not isinstance(o, Hand):
            return NotImplemented
        return self.handstring == o.handstring

    def __gt__(self, o: 'Hand') -> bool:
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
        actual_combos = [combo for combo in self.combos if combo.freq > 0]
        return len(actual_combos)

    def __repr__(self) -> str:
        return f"Hand('{self.input}')"

    def __str__(self) -> str:
        return(self.handstring)

    def get_sklansky_malmuth_handclass(self) -> int:
        """Return the Sklansky Malmuth Ranking Class of this hand

        Returns:
            int: [The class as integer]
        """
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
