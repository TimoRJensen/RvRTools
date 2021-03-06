"""
Version: 0.02

Author: GTOHOLE 11-20
"""
from typing import List
from pandas import DataFrame
from random import sample
from copy import deepcopy

from .hand import Hand
from .rank import RANKS


class Range():
    def __init__(self, range_str: str):
        '''This class represents a range and is usually defined by a
        range string like 'AA,QQ-TT,AKs,QJo-Q9o,[56.0]KQs-KTs[/56.0]'.

        Attributes:

        - range_str (String): The range definition like:
        'AA,QQ-TT,AKs,QJo-Q9o,[56.0]KQs-KTs[/56.0]'
        - game_uid (String): The uid referring to the game this range belongs
          to.

        Currently supported Rangestring formats include:
        - AA, KK, QQ
        - AA-QQ --> AA, KK, QQ
        - AKo-AJo --> AKo, AQo, Ajo
        - AK-AJ --> AKo, AKs, AQs, AQo, ,AJs, Ajo
        - [50]AA, KK[/50], QQ
        - [50]AA-QQ[/50]
        - ...

        Remarks:

        ";" will be replaced by a ","
        '''
        self.range_str = range_str.replace(";", ",").replace('\n', '')
        self.parts: List[RangePart] = []
        self.hands_dict: dict = self.build_0freq_hands_dict()
        self.converted_range_dict: dict = self.convert_range_str_to_dict()
        self._validate_input()

    def __delitem__(self, hand):
        del self.converted_range_dict[hand]

    def __setitem__(self, hand, freq):
        self.converted_range_dict[hand] = freq

    def __getitem__(self, hand):
        return self.converted_range_dict[hand]

    def __iter__(self):
        return iter(self.converted_range_dict.items())

    def __contains__(self, key) -> bool:
        return key in self.converted_range_dict

    def __sub__(self, other: 'Range') -> 'Range':
        diff = deepcopy(self)
        for hand, freq in other:
            if hand in self:
                s_freq = self[hand]
                if freq < s_freq:
                    diff[hand] = s_freq - freq
                else:
                    del diff[hand]
        return diff

    def __len__(self):
        return len(self.converted_range_dict)

    def __add__(self, other: 'Range') -> 'Range':
        sum_ = deepcopy(self)
        for hand, o_freq in other:
            if hand in self:
                s_freq = self[hand]
                if s_freq < 100:
                    new_freq = s_freq + o_freq
                    sum_[hand] = min(new_freq, 100)
            else:
                sum_[hand] = o_freq

        return sum_

    @property
    def combos(self) -> list:
        """
        Collects all Combo objects from RangePart objects and
        consolidates them in one list, that is returned
        """
        return [combo for part in self.parts for combo in part.combos]

    def __repr__(self) -> str:
        return f"Range({self.range_str})"

    def __str__(self) -> str:
        return self.range_str

    def _validate_input(self):
        """
        Validates the range string. Checks for valid characters.
        """
        for ch in self.range_str.upper():
            if ch not in 'AKQJT9876543210,-OS []./+':
                err_msg = ch + RangeError.ERR003_NOT_VALID_CHAR
                raise RangeError(self.range_str, msg=err_msg)

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
    def full_range() -> 'Range':
        return Range('''22+,23o,42o+,52o+,62o+,72o+,82o+,92o+,T2o+,J2o+,Q2o+,K2o+,
                     A2o+,23s,42s+,52s+,62s+,72s+,82s+,92s+,T2s+,J2s+,Q2s+,K2s+,
                     A2s+''')

    @classmethod
    def build_xy_dict(cls: 'Range') -> dict:
        return {(x, y): hand for hand, (_, x, y)
                in cls.build_0freq_hands_dict().items()}

    def build_df_freqs_and_combos_skl_mal(self) -> DataFrame:
        """
        Takes Range object and creates a DataFrame grouped by
        Sklansky-Malmuth-Groups and frequencies.
        """
        hands = []
        for h, f in self.converted_range_dict.items():
            hand = Hand(handstring=h)
            hand_dict = {'hand': hand.handstring,
                         'group': hand.class_skl_mal,
                         'combos': hand.all_combos_str,
                         'freq': f}
            hands.append(hand_dict)
        df = DataFrame(hands)
        df = df.groupby(['group', 'freq']).agg(list)
        return df

    def convert_range_str_to_dict(self) -> dict:
        """
        Converts rangestrings into single hands dictionary with frequencies.

        Input: 'AA,QQ-TT,AKs,QJo-Q9o,[56.0]KQs-KTs[/56.0]'

        Output: {'AA': 100, 'QQ': 100, 'JJ': 100, 'TT': 100, 'AKs': 100
                , 'QJo': 100, 'QTo': 100, 'Q9o': 100, 'KQs': 56.0, 'KJs': 56.0
                , 'KTs': 56.0}"""

        rv = {}
        str_no_space = self.range_str.replace(" ", "")
        str_split = self.split_range_str_in_parts(str_no_space)
        for part_str in str_split:
            self.parts.append(RangePart(part=part_str,
                                        my_range_obj=self))
        for part in self.parts:
            for h in part.hands_str:
                rv[h] = part.freq
        return rv

    def pick_combos(self, as_str=False):
        if not as_str:
            return [combo for part in self.parts
                    for combo in part.pick_combos()]

        combos_list = [str(combo) for part in self.parts
                       for combo in part.pick_combos()]
        return ','.join(combos_list)

    def randomize_suits_for_range(self,
                                  grouping='skl-mal',
                                  combo_delimiter=',',
                                  debug=False):
        """
        Takes a Range object and creates rangestring with frequencies
        approximately applied using suits.

        Grouping options are:

        - grouping='by_hand'  -  this will approximate the
            number of combos per hand with the frequencies applied.
            This is the least precise grouping.

        - grouping='skl-mal'  -  uses the Sklansky-Malmuth groups to return the
            number of combos per group with frequencies applied.
        """
        randomized_suits_string = ''
        combos_list = []
        rv = ''
        if grouping == 'by_hand':
            for h, f in self.converted_range_dict.items():
                hand = Hand(handstring=h)
                no_of_combos = (f/100) * len(hand.all_combos_str)
                combos_list.append(
                    sample(hand.all_combos_str, round(no_of_combos)))
            for x in combos_list:
                for combo in x:
                    rv += combo + combo_delimiter
            randomized_suits_string = rv[:-len(combo_delimiter)]
            return randomized_suits_string
        elif grouping == 'skl-mal':
            df = self.build_df_freqs_and_combos_skl_mal()
            ls_comobs_hand = []
            rv_list = []
            df['flat_combos'] = df['combos'].apply(self._flatten_l_of_ls, 1)
            df['no. of combos'] = df['flat_combos'].apply(len, 1)
            df['Calc no. of combos'] = 0
            for (grp, freq), (_, combos_lists, _, _, _) in df.iterrows():
                ls_comobs_hand = []
                for combos_list in combos_lists:
                    ls_comobs_hand += combos_list
                no_of_combos = round((freq/100) * len(ls_comobs_hand))
                df.loc[(grp, freq), 'Calc no. of combos'] = no_of_combos
                ls_combos_grp = sample(ls_comobs_hand, no_of_combos)
                rv_list += ls_combos_grp
            for combo in rv_list:
                rv += combo + combo_delimiter
            randomized_suits_string = rv[:-len(combo_delimiter)]
            # print(df.head(10))
            return randomized_suits_string

    def split_range_str_in_parts(self, range_str: str = None) -> List[str]:
        """
        Parses the given rangestring and returns a list with it's partial
        strings in a list.
        """
        r_str = ''
        if range_str is not None:
            r_str = range_str
        elif self.range_str != '':
            r_str = self.range_str
        else:
            raise RangeError(self.range_str, msg="Unknown Error!")
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

    def __init__(self, range_str: str, msg: str = 'Not a valid range!'):
        self.range_str = range_str
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"'{self.range_str}' -> {self.msg}"


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
            self.freq = self.get_freq()
        self.part_no_freq = self.remove_freq_tag()
        self.hands_str = self.get_hands_str()

    @property
    def combos(self):
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

    @property
    def hands(self) -> List[Hand]:
        return [Hand(handstring=hand, freq=self.freq)
                for hand in self.hands_str]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(part={self.part})"

    def __str__(self) -> str:
        return self.part

    def get_hands_str(self):
        """
        Gets hands from range string. Returns a list of all hands.
        """
        if self.is_range:
            return self.get_hands_from_range()
        if self.part_no_freq[0] == self.part_no_freq[1]:
            if len(self.part_no_freq) != 2:
                raise RangeError(self.part,
                                 msg=RangeError.ERR002_PAIR_LEN_NOT_2)
            return [self.part_no_freq]
        else:
            hand = Hand(handstring=self.part_no_freq)
            if hand.hand_type == 'nosuit':
                return [self.part_no_freq + 's', self.part_no_freq + 'o']
            elif hand.hand_type in ['suited', 'offsuit']:
                return [self.part_no_freq]
            else:
                raise RangeError(self.part)

    def check_has_freq(self):
        """
        Checks if the range part includes a frequency.
        (e.g. [56.0]KQs-KTs[/56.0])
        Returns a boolean.
        """
        return '[/' in self.part

    def get_freq(self):
        """
        Extracts the frequency from a range part string that includes a
         frequency. Returns a Float or 100.
        """
        start = '['
        end = ']'
        s = self.part
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
            return Hand(handstring='AA')
        else:
            raise RangeError(self.part)
        d = self.my_range_obj.hands_dict.items()
        rv_list = [hand for hand, (_, x, y) in d if ((x == start_x)
                                                     and (start_y == y))]
        if len(rv_list) == 1:
            return Hand(handstring=rv_list[0])
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
            start_hand = Hand(handstring=s[:s.find(self.range_identifier)])
            end_hand = Hand(handstring=s[s.find(self.range_identifier) + 1:])
            if len(start_hand) != len(end_hand):
                raise RangeError(self.part,
                                 msg=RangeError.ERR001_LEN_NOT_EQUAL)
            elif start_hand.hand_type != end_hand.hand_type:
                raise RangeError(self.part)
        elif self.is_plus_range:
            end_hand = Hand(handstring=s.replace(self.plus, ''))
            start_hand = self.get_start_hand_for_plus_range(end_hand)
        else:
            raise RangeError(self.part)
        start_x = start_hand.index_x
        start_y = start_hand.index_y
        end_x = end_hand.index_x
        end_y = end_hand.index_y

        rv.append(start_hand.handstring)
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
            rv.append(Hand(handstring=key).handstring)
        rv.append(end_hand.handstring)
        return rv

    def pick_combos(self, as_str=False):
        if not as_str:
            return [combo for hand in self.hands
                    for combo in hand.pick_combos()]
        combos_list = [str(combo) for hand in self.hands
                       for combo in hand.pick_combos()]
        return ','.join(combos_list)

    def remove_freq_tag(self):
        """Removes the frequency tag from a range part string. Returns a
        String.
        """
        if '[' not in self.part:
            return self.part

        start = '['
        end = ']'
        clean = self.part[self.part.find(end) + 1:]
        clean = clean[:clean.find(start)]
        return clean
