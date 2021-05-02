NLH_SHORTS = 'csdh'
NLH_NAMES = ['Club', 'Spade', 'Diamond', 'Heart']


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
    def __init__(self, name: str, short: str) -> None:
        self.name = name
        self.short = short

    def __repr__(self) -> str:
        return f"Suit(name={self.name}, short={self.short})"

    def __str__(self) -> str:
        return self.name


zipper = dict(zip(NLH_SHORTS, NLH_NAMES))
SUITS = tuple(Suit(zipper[short], short) for short in zipper)

SUITS = dict(zip(NLH_SHORTS, SUITS))
