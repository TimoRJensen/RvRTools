import re

from typing import Union

from .range import Range, RangeError
from .combo import Combo, PairCombo, SuitedCombo, OffsuitCombo
from .hand import Hand, PairHand, SuitedHand, OffsuitHand, NoSuitHand


class Str2pynlh():
    RANK = '[AKQJT987654321]'
    RANK2 = r'[AKQJT987654321]{2}'
    SUIT = '[SDCH]'
    TYPE = r"[SO]{0,1}"

    def __init__(self, input: str) -> None:
        """Class to turn a String into an Pynlh object."""
        self.input = input
        self.is_combo = self._is_combo()
        self.is_range = self._is_range()
        self.is_hand = self._is_hand()
        self._validate_input()
        self._parent = self._get_parent_object()

    def get_object(self) -> Union[Combo, Hand, Range]:
        parent = str(self._parent)
        if self.is_combo:
            if self.is_combo_pair:
                return PairCombo(parent)
            elif self.is_combo_suited:
                return SuitedCombo(parent)
            elif self.is_combo_offsuit:
                return OffsuitCombo(parent)
        elif self.is_hand:
            if self.is_hand_pair:
                return PairHand(parent)
            elif self.is_hand_suited:
                return SuitedHand(parent)
            elif self.is_hand_offsuit:
                return OffsuitHand(parent)
            elif self.is_hand_nosuit:
                return NoSuitHand(parent)
        elif self.is_range:
            return Range(parent)

    def _validate_input(self):
        """
        Validates the range string. Checks for valid characters.
        """
        for ch in self.input.upper():
            if ch not in 'AKQJT9876543210,-OS []./+SDCH':
                err_msg = (f"'{self.input}' -> '{ch}' -> is not a valid"
                           + " character for Pynlh.")
                raise AttributeError(err_msg)
        if (not self.is_range) and (not self.is_hand) and (not self.is_combo):
            raise RangeError(self.input)

    def _get_parent_object(self) -> Union[Combo, Hand, Range]:
        if self.is_range:
            return Range(self.input)
        elif self.is_hand:
            return Hand(self.input)
        elif self.is_combo:
            return Combo(self.input)
        else:
            raise Exception('Unexpected Error.')

    def _is_range(self) -> bool:
        regex = re.compile('[-+]')
        match = regex.search(self.input)
        return bool(match)

    def _is_hand(self) -> bool:
        regex = re.compile(f'(^{self.RANK2}{self.TYPE}$)')
        match = regex.match(self.input.upper())
        return bool(match)

    def _is_combo(self) -> bool:
        regex = re.compile(f'(^{self.RANK}{self.SUIT}{self.RANK}{self.SUIT}$)')
        match = regex.match(self.input.upper())
        return bool(match)

    @property
    def is_combo_pair(self) -> bool:
        if self.is_combo:
            return str(self._parent)[0] == str(self._parent)[2]
        else:
            return False

    @property
    def is_combo_suited(self) -> bool:
        if self.is_combo:
            return str(self._parent)[1] == str(self._parent)[3]
        else:
            return False

    @property
    def is_combo_offsuit(self) -> bool:
        if self.is_combo:
            return str(self._parent)[1] != str(self._parent)[3]
        else:
            return False

    @property
    def is_hand_nosuit(self) -> bool:
        if not self.is_hand:
            return False

        parent = str(self._parent)
        if len(parent) == 2:
            return (parent[0] != parent[1])
        else:
            return False

    @property
    def is_hand_pair(self) -> bool:
        if not self.is_hand:
            return False

        parent = str(self._parent)
        if len(parent) == 2:
            return (parent[0] == parent[1])
        else:
            return False

    @property
    def is_hand_suited(self) -> bool:
        if self.is_hand:
            parent = str(self._parent)
            return (parent[0] != parent[1]) and (parent[2] == 's')
        else:
            return False

    @property
    def is_hand_offsuit(self) -> bool:
        if not self.is_hand:
            return False

        parent = str(self._parent)
        if len(parent[2]) == 3:
            return (parent[2] == 'o')
        else:
            return False