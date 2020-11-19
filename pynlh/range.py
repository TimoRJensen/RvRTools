"""
Version: 0.02

Author: GTOHOLE 11-20
"""

from pandas import DataFrame
from random import sample
from pynlh import Hand


class RangeError(Exception):
    """
    Exception class of pynlh's Range class.
    """
    pass

    def __init__(self, range_string, msg='Not a valid range!'):
        self.range_string = range_string
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"'{self.range_string}' -> {self.msg}"


class Range:
    def __init__(self, range_str, game_uid=None):
        '''This class represents a range and is usually defined by a
        range string like 'AA,QQ-TT,AKs,QJo-Q9o,[56.0]KQs-KTs[/56.0]'.

        Attributes:

        - range_str (String): The range definition like:
        'AA,QQ-TT,AKs,QJo-Q9o,[56.0]KQs-KTs[/56.0]'
        - game_uid (String): The uid refering to the game this range belongs
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
        self.game_uid = game_uid
        self.range_str = range_str.replace(";", ",")
        self.parts = []
        self.hands_dict = self.build_0freq_hands_dict()
        self.converted_range_dict = self.convert_range_str_to_dict(game_uid)
        self._validate_input()

    def __repr__(self) -> str:
        if self.game_uid is not None:
            return f"Range({self.range_str}, {self.game_uid})"
        else:
            return f"Range({self.range_str})"

    def __str__(self) -> str:
        return self.range_str

    def _validate_input(self):
        """
        Validates the range string. Checks for valid characters.
        """
        for ch in self.range_str.upper():
            if ch not in 'AKQJT9876543210,-OS []./+':
                raise RangeError(self.range_str)

    @classmethod
    def _flatten_l_of_ls(cls, x):
        """
        Helperfunction thats flattens lists of lists.
        """
        rv = []
        for sub in x:
            for itm in sub:
                rv.append(itm)
        return rv

    @classmethod
    def build_0freq_hands_dict(cls):
        """
        Creates a dictionary with all No-Limit Holdem hands.
        (like {'AA': [0, 1, 1], 'AKo': [0, 1, 2] ...} ) Hands are the keys and
        the values represent [Frequency, Index_x, Index_y]. Whereas the
        Frequency will always be 0.
        """
        hands_dict = {}
        handranks = [
            "A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"
        ]
        i = 0
        for n, rank in enumerate(handranks):
            for n2, rank2 in enumerate(handranks):
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

    def build_df_freqs_and_combos_skl_mal(self):
        """
        Takes Range object and creates a DataFrame grouped by
        Sklansky-Malmuth-Groups and frequencies.
        """
        hands = []
        for h, f in self.converted_range_dict.items():
            hand = Hand(handstring=h)
            hand_dict = {'hand': hand.handstring,
                         'group': hand.class_skl_mal,
                         'combos': hand.all_combos,
                         'freq': f}
            hands.append(hand_dict)
        df = DataFrame(hands)
        df = df.groupby(['group', 'freq']).agg(list)
        return df

    def convert_range_str_to_dict(self, game_uid):
        """
        Converts rangestrings into single hands dictionary with frequences.

        Input: 'AA,QQ-TT,AKs,QJo-Q9o,[56.0]KQs-KTs[/56.0]'

        Output: {'AA': 100, 'QQ': 100, 'JJ': 100, 'TT': 100, 'AKs': 100
                , 'QJo': 100, 'QTo': 100, 'Q9o': 100, 'KQs': 56.0, 'KJs': 56.0
                , 'KTs': 56.0}"""

        rv = {}
        str_no_space = self.range_str.replace(" ", "")
        str_split = self.split_range_str_in_parts(str_no_space)
        for part_str in str_split:
            self.parts.append(RangeStringPart(part_str,
                                              game_uid=game_uid,
                                              my_range_obj=self))
        for part in self.parts:
            for h in part.hands:
                rv[h] = part.freq
        return rv

    def randomize_suits_for_range(self,
                                  grouping='skl-mal',
                                  combo_delimiter=',',
                                  debug=False):
        """
        Takes a Range object and creates rangestring with frequencies
        approximatly applied using suits.

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
                no_of_combos = (f/100) * len(hand.all_combos)
                combos_list.append(
                    sample(hand.all_combos, round(no_of_combos)))
            for x in combos_list:
                for combo in x:
                    rv += combo + combo_delimiter
            randomized_suits_string = rv[:-len(combo_delimiter)]
            return randomized_suits_string
        elif grouping == 'skl-mal':
            df = self.build_df_freqs_and_combos_skl_mal(self)
            ls_cmbs_hand = []
            rv_list = []
            df['flat_combos'] = df['combos'].apply(self._flatten_l_of_ls, 1)
            df['no. of combos'] = df['flat_combos'].apply(len, 1)
            df['Calc no. of combos'] = 0
            for (grp, freq), (_, combos_lists, _, _, _) in df.iterrows():
                ls_cmbs_hand = []
                for combos_list in combos_lists:
                    ls_cmbs_hand += combos_list
                no_of_combos = round((freq/100) * len(ls_cmbs_hand))
                df.loc[(grp, freq), 'Calc no. of combos'] = no_of_combos
                ls_combos_grp = sample(ls_cmbs_hand, no_of_combos)
                rv_list += ls_combos_grp
            for combo in rv_list:
                rv += combo + combo_delimiter
            randomized_suits_string = rv[:-len(combo_delimiter)]
            # print(df.head(10))
            return randomized_suits_string

    def split_range_str_in_parts(self, range_str: str = None) -> list(str):
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
            raise RangeError(self.range_str)
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
                elif '/' not in freq_str:
                    freq = float(freq_str.replace('[', '').replace(']', ''))
                read_freq = False
            else:
                read_part = True
        return rv


class RangeStringPart:

    def __init__(self,
                 part,
                 my_range_obj=None,
                 game_uid=None,
                 freq=None,
                 range_identifier='-',
                 plus_range_identifier='+'):
        """This class represents parts (like 'AA' or 'QQ-TT') of a
        range string (like 'AA,QQ-TT,AKs,QJo-Q9o,[56.0]KQs-KTs[/56.0]')
        separeted by commas. These can then be evaluated to find all the hands
        represented by this range string part.

        Attributes:
        ----------

        - part (String): The actual range string part like 'AA' or 'QQ-TT'
            or '[56.0]KQs-KTs[/56.0]'
        - game_uid (String): The uid refering to the game this range belongs
         to.
        - my_range_obj (Range): The instance of the range this part
            belongs to.
        - freq=None (Float): The frequency this range part will use. (e.g.
        instead of having '[56.0]KQs-KTs[/56.0]' as a part we could also have
        'KQs-KTs' and set the freq=56.)


        created by TJE 10-20
        """
        self.part = part
        self.game_uid = game_uid
        self.freq = freq
        self.my_range_obj = my_range_obj
        if self.my_range_obj is None:
            self.my_range_obj = Range(self.part)
        self.range_identifier = range_identifier
        self.plus_range_identifier = plus_range_identifier
        if not self.freq:
            self.freq = self.get_freq()
        # if self.freq < 100:
        self.part_no_freq = self.remove_freq_tag()
        # else:
        #     self.part_no_freq = self.part
        self.is_range = self.check_is_range()
        self.hands = self.get_hands()

    def get_hands(self):
        """
        Gets hands from range string. Returns a list of all hands.
        """
        if not self.is_range:
            return [self.part_no_freq]
        elif self.is_range:
            return self.get_hands_from_range()

    def check_has_freq(self):
        """
        hecks if the range part includes a frequency.
        (e.g. [56.0]KQs-KTs[/56.0])
        Returns a boolean.
        """
        if '[/' in self.part:
            return True
        else:
            return False

    def check_is_range(self):
        """
        Checks if range part string represents a range of hands.
        (e.g. QQ-TT)
         Returns a Boolean.
        """
        r_id = self.range_identifier
        if (r_id in self.part_no_freq) or ('+' in self.part_no_freq):
            return True
        else:
            return False

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

    def get_start_hand_for_plus_range(self, end_hand: str, suit: str):
        end_hand_idx = (self.my_range_obj.hands_dict[end_hand][1],
                        self.my_range_obj.hands_dict[end_hand][2])
        end_x = end_hand_idx[0]
        end_y = end_hand_idx[1]
        if suit == 's':
            start_y = end_y
            start_x = end_y + 1
        elif suit == 'o':
            start_x = end_x
            start_y = end_x + 1
        else:
            raise RangeError(self.part)
        d = self.my_range_obj.hands_dict.items()
        rv_list = [hand for hand, (_, x, y) in d if ((x == start_x)
                                                     and (start_y == y))]
        if len(rv_list) == 1:
            return rv_list[0]

    def get_hands_from_range(self):
        """Finds hands in a hand range (like QQ-TT). Will return a list
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
        suit = s[2:3]
        if ('+' not in s) and (self.range_identifier in s):
            start_hand = s[:s.find(self.range_identifier)]
            end_hand = s[s.find(self.range_identifier) + 1:]
            if (suit == 's') or (suit == 'o'):
                if suit != end_hand[2]:
                    raise RangeError(self.part)
        elif ('+' in s) and (s[len(s)-1:] == '+'):
            end_hand = s.replace('+', '')
            if suit == 's':
                start_hand = self.get_start_hand_for_plus_range(end_hand, suit)
            elif suit == 'o':
                start_hand = self.get_start_hand_for_plus_range(end_hand, suit)
            elif ((len(s) == 3) and
                    (s[len(s)-1:] == '+')):
                start_hand = 'AA'
            else:
                raise RangeError(s)
        else:
            raise RangeError(s)
        # Index x ist 2ter value in hands_dict - y der dritte
        start_hand_idx = (self.my_range_obj.hands_dict[start_hand][1],
                          self.my_range_obj.hands_dict[start_hand][2])
        start_x = start_hand_idx[0]
        start_y = start_hand_idx[1]

        end_hand_idx = (self.my_range_obj.hands_dict[end_hand][1],
                        self.my_range_obj.hands_dict[end_hand][2])
        end_x = end_hand_idx[0]
        end_y = end_hand_idx[1]

        rv.append(start_hand)
        new_hands_dict = {}
        h = self.my_range_obj.hands_dict
        if len(start_hand) == 2:
            # Pair: x-index (right) must be between start and end hand
            # and y-index (down) must be between start and end hand.
            new_hands_dict = {
                key: (x, y)
                for (key, (_, x, y)) in h.items() if (y > start_y) and (
                    y < end_y) and (x > start_x) and (x < end_x) and (y == x)
            }
        else:
            suit = start_hand[2].lower()
            if suit == 's':
                # Suited: x-index (right) must lie between start and end
                # hand and y-index must remain the same.
                new_hands_dict = {
                    key: (x, y)
                    for (key, (_, x, y)) in h.items() if (x > start_x) and (
                        x < end_x) and (y == start_y == end_y)
                }
            elif suit == 'o':
                # Offsuit: y-index (down) must be between start and end
                # hand x-index must remain the same.
                new_hands_dict = {
                    key: (x, y)
                    for (key, (_, x, y)) in h.items() if (y > start_y) and (
                        y < end_y) and (x == start_x == end_x)
                }
        for key in new_hands_dict:
            rv.append(key)
        rv.append(end_hand)
        return rv

    def remove_freq_tag(self):
        """Removes the frequency tag from a range part string. Rerturns a
         String.
        """
        if '[' in self.part:
            start = '['
            end = ']'
            clean = ''
            clean = self.part[self.part.find(end) + 1:]
            clean = clean[:clean.find(start)]
            return clean
        else:
            return self.part
