from functools import total_ordering
from typing import List, Dict

from .rank import RANKS, Rank
from .suit import SUITS, Suit
from .card import CARDS, Card
from .combo import Combo


class HandError(Exception):
    """
    Exception class of pynlh's Hand class.
    """
    pass

    def __init__(self, hand: 'Hand', msg='Not a valid hand!'):
        self.hand = hand
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"'{self.hand.input}' -> {self.msg}"


@total_ordering
class Hand():

    def __init__(self, input: str, input_freq: float = 100) -> None:
        """Pynlh's Hand Class. Holds a dict of all available Combos with a
           frequency.

        Args:
            input (str): [description]
            input_freq (float, optional): [description]. Defaults to 100.
        """
        self.input: str = input
        self._reorder_combo_input()
        self.input_freq: float = input_freq
        self.hand: str = ''  # set by _parse_input()
        self.rank1: Rank = None  # set by _parse_input()
        self.rank2: Rank = None  # set by _parse_input()
        self.hand_type: str = ''  # set by _parse_input()
        self.handstring: str = ''  # set by _parse_input()
        self.combos: Dict[Combo] = {}  # set by _parse_input()
        self.freq: float = 0.00  # set by _parse_input()
        self._parse_input()
        self.class_skl_mal = self.get_sklansky_malmuth_handclass()

    def _reorder_combo_input(self) -> None:
        if not self._input_is_combo:
            return None

        is_RRss_format: bool = ((self.input[0].upper() in RANKS)
                                and (self.input[1].upper() in RANKS)
                                and (self.input[2].lower() in SUITS)
                                and (self.input[3].lower() in SUITS))
        is_RsRs_format: bool = ((self.input[0].upper() in RANKS)
                                and (self.input[1].lower() in SUITS)
                                and (self.input[2].upper() in RANKS)
                                and (self.input[3].lower() in SUITS))
        if is_RRss_format:
            rank1 = self.input[0].upper()
            rank2 = self.input[1].upper()
            suit1 = self.input[2].lower()
            suit2 = self.input[3].lower()
        elif is_RsRs_format:
            r1 = self.input[0].upper()
            r2 = self.input[2].upper()
            s1 = self.input[1].lower()
            s2 = self.input[3].lower()
        else:
            raise HandError(self)
        if list(RANKS.keys()).index(r1) < list(RANKS.keys()).index(r2):
            rank1 = r1
            rank2 = r2
        else:
            rank1 = r2
            rank2 = r1
        if list(SUITS.keys()).index(s1) < list(SUITS.keys()).index(s2):
            suit1 = s1
            suit2 = s2
        else:
            suit1 = s2
            suit2 = s1
        self.input = rank1 + suit1 + rank2 + suit2

    def _parse_input(self) -> None:
        self._parse_hand_from_input()
        self.hand_type = self._parse_hand_type_from_input()
        self._parse_handstring_from_input()
        self._set_combos()
        self.freq = self._avg([combo.freq for _, combo in self.combos.items()])

    @staticmethod
    def _avg(lst) -> float:
        return sum(lst) / len(lst)

    @property
    def _input_is_combo(self) -> bool:
        return len(self.input) == 4

    def _parse_hand_from_input(self) -> None:
        if self._input_is_combo:
            self.hand = self.input[0] + self.input[2]
        else:
            self.hand = self.input[0:2]
        try:
            self.rank1 = Rank(self.hand[0].upper())
            self.rank2 = Rank(self.hand[1].upper())
        except KeyError:
            raise HandError(self)

    def _parse_hand_type_from_input(self) -> str:
        # sourcery skip: remove-redundant-if
        input = self.input
        if self._input_is_combo:
            if input[0] == input[2]:
                return "pair"
            elif input[1] == input[3]:
                return "suited"
            elif input[1] != input[3]:
                return "offsuit"
            else:
                raise HandError
        else:
            if len(input) == 2:
                if input[0] == input[1]:
                    return "pair"
                else:
                    return "nosuit"
            elif len(input) == 3:
                suit = input[2].lower()
                if suit == "s":
                    return "suited"
                elif suit == "o":
                    return "offsuit"
            else:
                raise HandError

    def _parse_handstring_from_input(self) -> None:
        if self.hand_type in ['suited', 'offsuit']:
            hand_type_abr = self.hand_type[0]
        else:
            hand_type_abr = ''
        self.handstring = self.hand + hand_type_abr

    def _set_combos(self) -> None:
        if not self._input_is_combo:
            self.combos = {combo: Combo(combo_str=combo, freq=self.input_freq)
                           for combo in self.all_combos_str}
        else:
            self.combos = {combo: Combo(combo_str=combo, freq=0)
                           for combo in self.all_combos_str}
            self.combos[self.input].freq = self.input_freq

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
        actual_combos = [combo for _,
                         combo in self.combos.items() if combo.freq > 0]
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

    @property
    def all_combos_str(self) -> List[str]:
        cards_list = []
        rv = []
        for suit in SUITS:
            for rank in self.hand:
                cards_list.append(rank+suit)
        for card1 in cards_list:
            for card2 in cards_list:
                if ((card1 != card2) and
                    (card1[0] == self.hand[0]) and
                    (card2[0] == self.hand[1]) and
                    ((card1 + card2) not in rv) and
                        (card2 + card1) not in rv):
                    rv.append(card1 + card2)
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
    def index_x(self) -> int:
        """
        Property X-Index (The Position from left to right.)
        "Nosuit" hands will be treated as "offsuit" hands.
        """
        if self.hand_type == 'suited':
            return self.rank2.order
        if self.hand_type in ['offsuit', 'nosuit', 'pair']:
            return self.rank1.order

    @property
    def index_y(self) -> int:
        """
        Property Y-Index (The Position top left to bottom.)
        "Nosuit" hands will be treated as "offsuit" hands.
        """
        if self.hand_type == 'suited':
            return self.rank1.order
        elif self.hand_type in ['offsuit', 'nosuit', 'pair']:
            return self.rank2.order

    def __delitem__(self, combo):
        del self.combos[combo]

    def __setitem__(self, combo :str, freq):
        self.combos[combo] = freq

    def __getitem__(self, combo) -> Combo:
        return self.combos[combo]

    def pick_combos(self) -> List[Combo]:
        return [combo for _, combo in self.combos.items() if combo.pick()]

    def pick_combos_str(self) -> str:
        combos_list = [str(combo)
                       for _, combo in self.combos.items() if combo.pick()]
        return ','.join(combos_list)
