from functools import total_ordering


NLH_SHORTS = 'cdhs'
NLH_NAMES = ['Club', 'Diamond', 'Heart', 'Spade']
ZIPPER = dict(zip(NLH_SHORTS, NLH_NAMES))


class SuitError(Exception):
    pass

    def __init__(self, name: str, msg: str = 'Not a valid Suit!'):
        """
        Exception class pf pynlh's Suit class.
        """
        self.name = name
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"'{self.name}' -> {self.msg}"


class Suit():
    def __init__(self,
                 short: str,
                 ) -> None:
        self.short = short
        self.name = ZIPPER[short]
        self.order = (NLH_SHORTS.find(short)+1)

    def __repr__(self) -> str:
        return f"Suit(short={self.short}, name={self.name})"

    def __str__(self) -> str:
        return self.short

    def __eq__(self, other: 'Suit') -> bool:
        if self.__class__ is not other.__class__:
            return NotImplemented
        return True

    def __ne__(self, other: 'Suit') -> bool:
        if self.__class__ is not other.__class__:
            return NotImplemented
        return False

    def __gt__(self, other: 'Suit') -> bool:
        if self.__class__ is not other.__class__:
            return NotImplemented
        return False

    def __lt__(self, other: 'Suit') -> bool:
        if self.__class__ is not other.__class__:
            return NotImplemented
        return False

    def __ge__(self, other: 'Suit') -> bool:
        if self.__class__ is not other.__class__:
            return NotImplemented
        return False

    def __le__(self, other: 'Suit') -> bool:
        if self.__class__ is not other.__class__:
            return NotImplemented
        return False


SUITS = tuple(Suit(short) for short in NLH_SHORTS)
SUITS = dict(zip(NLH_SHORTS, SUITS))
