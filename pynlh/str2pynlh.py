import re
from typing import Union

from .combo import Combo
from .hand import Hand
from .range import Range

RANK = 'AKQJT987654321'
SUIT = 'SDCH'


class Str2pynlh():
    def __init__(self, input: str) -> None:
        """Class to turn a String into an Pynlh object."""
        self.input = input
        self._validate_input()

    def _validate_input(self):
        """
        Validates the range string. Checks for valid characters.
        """
        for ch in self.input.upper():
            if ch not in 'AKQJT9876543210,-OS []./+SDCH':
                err_msg = (f"'{self.input}' -> '{ch}' -> is not a valid"
                           + " character for Pynlh.")
                raise AttributeError(err_msg)

    def get_object(self) -> Union[Combo, Hand, Range]:
        pass

    @property
    def isRange(self) -> bool:
        regex = re.compile('[-+]')
        match = regex.search(self.input)
        return bool(match)

    @property
    def isHand(self) -> bool:
        pass

    @property
    def isCombo(self) -> bool:
        regex = re.compile(f'/([{RANK}][{SUIT}][{RANK}][{SUIT}])/')
        match = regex.search(self.input.upper())
        return bool(match)
