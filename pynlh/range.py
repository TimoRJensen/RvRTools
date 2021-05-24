from copy import deepcopy
from typing import List, Union

from .combo import Combo
from .hand import Hand
from .rank import RANKS


class RangeError(Exception):
    """
    Exception class of pynlh's Range class.
    """
    pass

    ERR001_LEN_NOT_EQUAL = """Length of starting hand is not equal to the
                           ending hand of this Range Part. ERR001"""
    ERR002_PAIR_LEN_NOT_2 = """The length of a pair Range Part must be exactly
                            2. - ERR002"""
    ERR003_NOT_VALID_CHAR = ' is not a valid character for a range - ERR003'
    ERR004_TOO_DASHES = 'There are too many dashes in this Range. ERR004'

    def __init__(self, range_str: str, msg: str = 'Not a valid range!'):
        self.range_str = range_str
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"'{self.range_str}' -> {self.msg}"


class Range():
    def __init__(self,
                 input: Union[str, dict] = None,
                 ) -> None:
        self.input = input
        self.combos: dict = {}
        self._parts_strs: list = []
        self._parts: List[RangePart] = []
        self.hands_dict: dict = self.build_0freq_hands_dict()
        self._process_input()

    def __repr__(self) -> str:
        return f"Range(combos={str(self.combos)})"

    def __str__(self) -> str:
        return self.to_str()

    def __len__(self) -> int:
        return len(self.combos)

    def __sub__(self, o: 'Range') -> 'Range':
        new = deepcopy(self.combos)
        for k, combo in self.combos.items():
            if k in o.combos:
                if o.combos[k].freq >= combo.freq:
                    del new[k]
                else:
                    new[k].freq = combo.freq - o.combos[k].freq
        return Range(new)

    def __add__(self, o: 'Range') -> 'Range':
        new = deepcopy(self.combos)
        for k, combo in o.combos.items():
            if k in self.combos:
                new[k].freq = min(self.combos[k].freq + combo.freq, 100)
            else:
                new[k] = combo
        return Range(new)

    def __getitem__(self, input) -> Combo:
        from .str2pynlh import Str2pynlh
        obj = Str2pynlh(input).get_object()
        if str(obj) not in self:
            raise KeyError
        if isinstance(obj, Combo):
            return deepcopy(self.combos[str(obj)])
        if isinstance(obj, Range):
            NotImplementedError
        if isinstance(obj, Hand):
            for part in self._parts:
                for hand in part.hands:
                    if (hand == obj) and (hand.handstring == obj.handstring):
                        return deepcopy(hand)
        if isinstance(obj, RangePart):
            NotImplementedError

    def __setitem__(self) -> 'Range':
        # TODO Construct new Range here.
        deepcopy(self)

    def __delitem__(self, input) -> 'Range':
        # TODO Construct new Range here.
        return deepcopy(self)

    def __iter__(self):
        return iter(self.combos.items())

    def __contains__(self, input) -> bool:
        from .str2pynlh import Str2pynlh
        obj = Str2pynlh(input).get_object()
        if isinstance(obj, Combo):
            return str(obj) in self.combos
        check = [combo in self.combos for combo in obj.combos]
        return all(check)

    def _process_input(self):
        if isinstance(self.input, str):
            self.input = self.input.replace(";", ",").replace('\n', '')
            self.input = self.input.replace(' ', '')
            self._validate_input()
            self._parts_strs = self._split_range_str_in_parts(self.input)
            for part_str in self._parts_strs:
                self._parts.append(RangePart(part=part_str,
                                             my_range_obj=self))
            self._build_combos_dict()
        elif isinstance(self.input, dict):
            self.combos = self.input

    def _build_combos_dict(self):
        combos_list: List[List[Combo]] = []
        for part in self._parts:
            combos_list.append(part.get_combos())
        flat_combos_list: List[Combo] = self._flatten_l_of_ls(combos_list)
        flat = self._flatten_l_of_ls(flat_combos_list)
        for combo in flat:
            self.combos[RangePart.remove_freq_tag(str(combo))] = combo

    def _validate_input(self):
        """
        Validates the range string. Checks for valid characters.
        """
        for ch in self.input.upper():
            if ch not in 'AKQJT9876543210,-OS []./+SDCH':
                err_msg = ch + RangeError.ERR003_NOT_VALID_CHAR
                raise RangeError(self.input, msg=err_msg)

    def apply_rng(self) -> List[Combo]:
        return self.from_combos_list([combo for part in self._parts
                                      for combo in part.apply_rng()])

    def to_str(self) -> str:
        rv = ''
        for k, _ in self:
            if rv:
                rv += ',' + k
            else:
                rv = k
        return rv

    @staticmethod
    def full_range() -> 'Range':
        return Range('''22+,23o,42o+,52o+,62o+,72o+,82o+,92o+,T2o+,J2o+,Q2o+,
                        K2o+,A2o+,23s,42s+,52s+,62s+,72s+,82s+,92s+,T2s+,J2s+,
                        Q2s+,K2s+,A2s+''')

    @staticmethod
    def _split_range_str_in_parts(range_str: str) -> List[str]:
        """
        Parses the given rangestring and returns a list with it's partial
        strings in a list and wraps these partial strings in it's frequency.
        """
        r_str = ''
        r_str = range_str
        read_freq = False
        read_part = True
        freq_str = ''
        part_str = ''
        freq_end = True
        rv = []
        freq = 100
        for i, chr in enumerate(r_str):
            if read_freq:
                freq_str += chr
            elif read_part:
                part_str += chr
            if ((chr == ',') or (i == len(r_str) - 1)):
                part_str = part_str.replace('[', '').replace(']', '')
                part_str = part_str.replace(',', '')
                rv.append(f"[{freq}]{part_str}[/{freq}]")
                part_str = ''
                if freq_end:
                    freq = 100
                    freq_str = ''
            if chr == '[':
                read_freq = True
                freq_end = False
            elif chr == ']':
                if '/' in freq_str:
                    freq_end = True
                else:
                    freq = float(freq_str.replace('[', '').replace(']', ''))
                read_freq = False
            else:
                read_part = True
        return rv

    @staticmethod
    def _flatten_l_of_ls(x) -> list:
        """
        Helperfunction that's flattens lists of lists.
        """
        rv = []
        for sub in x:
            for itm in sub:
                rv.append(itm)
        return rv

    @staticmethod
    def build_0freq_hands_dict() -> dict:
        """
        Creates a dictionary with all No-Limit Holdem hands.
        (like {'AA': [0, 1, 1], 'AKo': [0, 1, 2] ...} ) Hands are the keys and
        the values represent [Frequency, Index_x, Index_y]. Whereas the
        Frequency will always be 0.
        """
        hands_dict = {}
        i = 0
        for n, rank in enumerate(RANKS):
            for n2, rank2 in enumerate(RANKS):
                i += 1
                if rank == rank2:
                    # hand_type = "pair"
                    hand = rank + rank2
                elif n > n2:
                    # hand_type = "suited"
                    hand = rank2 + rank + 's'
                else:
                    # hand_type = "offsuit"
                    hand = rank + rank2 + 'o'
                hands_dict[hand] = [0, n + 1, n2 + 1]
        return hands_dict

    @staticmethod
    def from_combos_list(combos_list) -> 'Range':
        combos_dict = {str(combo): combo for combo in combos_list}
        return Range(combos_dict)


class RangePart():

    def __init__(self,
                 part: str,
                 my_range_obj: Range = None,
                 freq: float = None,
                 range_identifier: str = '-',
                 plus: str = '+'):
        """This class represents parts (like 'AA' or 'QQ-TT') of a
        range (like 'AA,QQ-TT,AKs,QJo-Q9o,[56.0]KQs-KTs[/56.0]')
        separeted by commas. These can then be evaluated to find all the hands
        represented by this range string part.

        Attributes:
        ----------

        - part (String): The actual range string part like 'AA' or 'QQ-TT'
            or '[56.0]KQs-KTs[/56.0]'
        - game_uid (String): The uid referring to the game this range belongs
         to.
        - my_range_obj (Range): The instance of the range this part
            belongs to.
        - freq=None (Float): The frequency this range part will use. (e.g.
        instead of having '[56.0]KQs-KTs[/56.0]' as a part we could also have
        'KQs-KTs' and set the freq=56.)


        created by TJE 10-20
        """
        self.part = part
        self.freq = freq
        self.my_range_obj = my_range_obj
        if self.my_range_obj is None:
            self.my_range_obj = Range(self.part)
        self.range_identifier = range_identifier
        self.plus = plus
        if not self.freq:
            self.freq = self.get_freq(self.part)
        self.part_no_freq = self.remove_freq_tag(self.part)
        self.hands: List[Hand] = self._set_hands()
        # self.hands_str = self.get_hands_str()

    def _set_hands(self) -> List[Hand]:
        if self.is_range:
            return self.get_hands_from_range()
        else:
            return [Hand(self.part_no_freq, self.freq)]

    @property
    def combos(self) -> List[Combo]:
        """
        Collects all Combo objects from Hand objects and consolidates them
        in one list, that is returned
        """
        return [combo for hand in self.hands for combo in hand.combos]

    @property
    def is_range(self):
        """
        Checks if range part string represents a range of hands.
        (e.g. QQ-TT)
         Returns a Boolean.
        """
        r_id = self.range_identifier
        return (r_id in self.part_no_freq) or ('+' in self.part_no_freq)

    @property
    def is_plus_range(self):
        no_freq = self.part_no_freq
        plus = self.plus
        return (plus in no_freq) and (no_freq[-1:] == plus)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(part={self.part})"

    def __str__(self) -> str:
        return self.part

    def get_hands_str(self):
        """
        Gets hands from range string. Returns a list of all hands.
        """
        # raise NotImplementedError
        if self.is_range:
            return self.get_hands_from_range()
        if self.part_no_freq[0] == self.part_no_freq[1]:
            if len(self.part_no_freq) != 2:
                raise RangeError(self.part,
                                 msg=RangeError.ERR002_PAIR_LEN_NOT_2)
            return [self.part_no_freq]
        else:
            hand = Hand(input=self.part_no_freq)
            if hand.hand_type == 'nosuit':
                return [self.part_no_freq + 's', self.part_no_freq + 'o']
            elif hand.hand_type in ['suited', 'offsuit']:
                return [self.part_no_freq]
            elif hand.hand_type == 'pair':
                return [hand.hand]
            else:
                raise RangeError(self.part)

    def check_has_freq(self):
        """
        Checks if the range part includes a frequency.
        (e.g. [56.0]KQs-KTs[/56.0])
        Returns a boolean.
        """
        return '[/' in self.part


    @staticmethod
    def get_freq(input) -> float:
        """
        Extracts the frequency from a range part string that includes a
         frequency. Returns a Float or 100.
        """
        start = '['
        end = ']'
        s: str = input
        if (s.find(start) > -1) and (s.find(end) > -1):
            return float(s[s.find(start) + len(start):s.find(end)])
        else:
            return 100

    def get_start_hand_for_plus_range(self,
                                      end_hand: Hand) -> Hand:
        end_x = end_hand.index_x
        end_y = end_hand.index_y
        if end_hand.hand_type == 'suited':
            start_y = end_y
            start_x = end_y + 1
        elif end_hand.hand_type in ['offsuit', 'nosuit']:
            start_x = end_x
            start_y = end_x + 1
        elif end_hand.hand_type == 'pair':
            return Hand(input='AA', input_freq=self.freq)
        else:
            raise RangeError(self.part)
        d = self.my_range_obj.hands_dict.items()
        rv_list = [hand for hand, (_, x, y) in d if ((x == start_x)
                                                     and (start_y == y))]
        if len(rv_list) == 1:
            return Hand(input=rv_list[0], input_freq=self.freq)
        else:
            raise RangeError(self.part_no_freq)

    def get_hands_from_range(self):
        """
        Finds hands in a hand range (like QQ-TT). Will return a list
        with all hands including the starting hand (QQ)
        and the ending hand (TT).

        The rangepart string without frequency tags is used for this.

        'QQ-TT'
            -->
        ['QQ', 'JJ', 'TT']
        """
        rv = []
        s = self.part_no_freq
        start_hand = ''
        if (self.plus not in s) and (self.range_identifier in s):
            if s.count(self.range_identifier) > 1:
                raise RangeError(self.part,
                                 msg=RangeError.ERR004_TOO_DASHES
                                 )
            start_hand = Hand(input=s[:s.find(self.range_identifier)],
                              input_freq=self.freq)
            end_hand = Hand(input=s[s.find(self.range_identifier) + 1:],
                            input_freq=self.freq)
            if len(start_hand) != len(end_hand):
                raise RangeError(self.part,
                                 msg=RangeError.ERR001_LEN_NOT_EQUAL)
            elif start_hand.hand_type != end_hand.hand_type:
                raise RangeError(self.part)
        elif self.is_plus_range:
            end_hand = Hand(s.replace(self.plus, ''), self.freq)
            start_hand = self.get_start_hand_for_plus_range(end_hand)
        else:
            raise RangeError(self.part)
        start_x = start_hand.index_x
        start_y = start_hand.index_y
        end_x = end_hand.index_x
        end_y = end_hand.index_y

        rv.append(start_hand)
        new_hands_dict = {}
        h = self.my_range_obj.hands_dict
        if start_hand.hand_type == 'pair':
            # Pair: x-index (right) must be between start and end hand
            # and y-index (down) must be between start and end hand.
            new_hands_dict = {
                key: (x, y)
                for (key, (_, x, y)) in h.items() if ((y > start_y)
                                                      and (y < end_y)
                                                      and (x > start_x)
                                                      and (x < end_x)
                                                      and (y == x))
            }
        elif start_hand.hand_type == 'suited':
            # Suited: x-index (right) must lie between start and end
            # hand and y-index must remain the same.
            new_hands_dict = {
                key: (x, y)
                for (key, (_, x, y)) in h.items() if ((x > start_x)
                                                      and (x < end_x)
                                                      and (y == start_y)
                                                      and (y == end_y))
            }
        elif start_hand.hand_type == 'offsuit':
            # Offsuit: y-index (down) must be between start and end
            # hand x-index must remain the same.
            new_hands_dict = {
                key: (x, y)
                for (key, (_, x, y)) in h.items() if ((y > start_y)
                                                      and (y < end_y)
                                                      and (x == start_x)
                                                      and (x == end_x))
            }
        for key in new_hands_dict:
            rv.append(Hand(input=key, input_freq=self.freq))
        rv.append(end_hand)
        return rv

    def apply_rng(self) -> List[Combo]:
        return [combo for hand in self.hands
                for combo in hand.apply_rng()]

    @staticmethod
    def remove_freq_tag(input: str):
        """Removes the frequency tag from a range part string. Returns a
        String.
        """
        if '[' not in input:
            return input

        start = '['
        end = ']'
        clean = input[input.find(end) + 1:]
        clean = clean[:clean.find(start)]
        return clean

    def get_combos(self) -> List[Combo]:
        return [hand.get_combos() for hand in self.hands]
