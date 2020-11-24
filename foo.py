# from pynlh import RANKS
# from pynlh import SUITS

# print(SUITS)
# for suit in SUITS:
#     print(suit.short)

# print(RANKS)
# for rank in RANKS:
#     print(rank)
# print(type(RANKS['A']))


import pandas as pd
s = pd.Series([1, 3, 2])
s.plot.line()