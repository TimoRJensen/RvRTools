"""
Version: 0.02

Author: GTOHOLE 11-20
"""
SUITS = ["s", "c", "d", "h"]


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


class Hand():
    RANKS = {'A': 1,
             'K': 2,
             'Q': 3,
             'J': 4,
             'T': 5,
             '9': 6,
             '8': 7,
             '7': 8,
             '6': 9,
             '5': 10,
             '4': 11,
             '3': 12,
             '2': 13,
             }

    def __init__(self,
                 hand: str = None,
                 hand_type: str = None,
                 handstring: str = None):
        self.hand = hand
        self.hand_type = hand_type
        self.handstring = handstring
        self._set_default_values()
        self.all_combos = self.get_all_combos()
        self.class_skl_mal = self.get_sklansky_malmuth_handclass()

    def __repr__(self) -> str:
        return f"Hand({self.hand_uid}, {self.hand}, {self.hand_type}"

    def __str__(self) -> str:
        return(self.handstring)

    def __len__(self) -> int:
        return len(self.handstring)

    @property
    def index_x(self):
        """
        Property X-Index (The Position from left to right.)
        "Nosuit" hands will be treated as "offsuit" hands.
        """
        if self.hand_type == 'suited':
            return self.RANKS[self.hand[1]]
        if self.hand_type in ['offsuit', 'nosuit', 'pair']:
            return self.RANKS[self.hand[0]]

    @property
    def index_y(self):
        """
        Property X-Index (The Position from left to right.)
        "Nosuit" hands will be treated as "offsuit" hands.
        """
        if self.hand_type == 'suited':
            return self.RANKS[self.hand[0]]
        elif self.hand_type in ['offsuit', 'nosuit', 'pair']:
            return self.RANKS[self.hand[1]]

    def _set_default_values(self):
        if self.handstring is not None:
            self.hand_type = self.evaluate_hand_type_from_handstring()
            self.hand = self.eval_hand_from_handstring()
        elif not self.handstring:
            if (self.hand is None) or (self.hand_type is None):
                raise HandError('You cannot enter a hand without a hand_type.')
            self.handstring = self.eval_handstring()

    def eval_handstring(self):
        if (self.hand_type == 'pair') or (self.hand_type == 'nosuit'):
            return self.hand
        elif (self.hand_type == 'suited') or (self.hand_type == 'offsuit'):
            return self.hand + self.hand_type[0]

    def eval_hand_from_handstring(self):
        return self.handstring[0:2]

    def evaluate_hand_type_from_handstring(self):
        """
        Evaluates the hand type (suited, offsuit, pair or nosuit) from a given
        handstring (self.handstring).
        """
        hand_str = self.handstring
        if (len(hand_str) == 2) and (hand_str[0] == hand_str[1]):
            return "pair"
        elif (len(hand_str) == 2) and (hand_str[0] != hand_str[1]):
            return "nosuit"
        else:
            suit = hand_str[2].lower()
            if suit == "s":
                return "suited"
            elif suit == "o":
                return "offsuit"

    def get_all_combos(self):
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
