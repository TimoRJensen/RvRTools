from functools import total_ordering


NLH_SHORTS = 'AKQJT98765432'
NLH_NAMES = ['Ace', 'King', 'Queen', 'Jack', 'Ten', 'Nine', 'Eight', 'Seven',
             'Six', 'Five', 'Four', 'Three', 'Deuce']
ZIPPER = dict(zip(NLH_SHORTS, NLH_NAMES))


class RankError(Exception):
    pass

    def __init__(self, name: str, msg: str = 'Not a valid Rank!'):
        """
    Exception class pf pynlh's Rank class.
        """
        self.name = name
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"'{self.name}' -> {self.msg}"


@total_ordering
class Rank():

    def __init__(self,
                 short: str,
                 ) -> None:
        """
        Pynlh's Rank class Object.
        """
        self.short = short
        self.order = (NLH_SHORTS.find(short)+1)
        self.name = (ZIPPER[short])
        self.check_input()

    def check_input(self):
        if not isinstance(self.name, str):
            raise TypeError('The attribute "name" has to be of type str.')

        if self.order not in range(1, 14):
            raise ValueError(f"""The order has to be between 1 and 13, but is
                             {self.order}.""")
        if not isinstance(self.order, int):
            raise TypeError('The attribute "order" has to be of type int.')

        if len(self.short) > 1:
            raise ValueError("""The attribute "short" should only be 1
                             character.""")
        if not isinstance(self.short, str):
            raise TypeError('The attribute "short" has to be of type str.')

    def __repr__(self) -> str:
        return (f"Rank(short={self.short}, name={self.name}" +
                f", order={self.order})")

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: 'Rank') -> bool:
        if self.__class__ is not other.__class__:
            return NotImplemented

        return self.order == other.order

    def __gt__(self, other: 'Rank') -> bool:
        if self.__class__ is not other.__class__:
            return NotImplemented
        return self.order > other.order


RANKS = tuple(Rank(short)
              for short in NLH_SHORTS
              )

RANKS = dict(zip(NLH_SHORTS, RANKS))
