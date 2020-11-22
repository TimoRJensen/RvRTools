from pynlh import RANKS
from pynlh import SUITS

print(SUITS)
for suit in SUITS:
    print(suit.short)

print(RANKS)
for rank in RANKS:
    print(rank)
print(type(RANKS['A']))
