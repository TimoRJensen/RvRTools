from .hand import Hand, HandError  # noqa: F401,E402
from .combo import Combo  # noqa: F401,E402
from .rank import RANKS, Rank  # noqa: F401,E402
from .suit import SUITS, Suit  # noqa: F401,E402
from .range import Range, RangePart, RangeError  # noqa: F401,E402
from .tools import timer  # noqa: F401,E402


def FullRange() -> Range:
    return Range('''22+,23o,42o+,52o+,62o+,72o+,82o+,92o+,T2o+,J2o+,Q2o+,K2o+,
                 A2o+,23s,42s+,52s+,62s+,72s+,82s+,92s+,T2s+,J2s+,Q2s+,K2s+,
                 A2s+''')
