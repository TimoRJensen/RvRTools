# import pytest

from pynlh import Hand


def test_get_all_combos_hand_n_type(debug=False):
    hand_offsuit = Hand(hand="AJ", hand_type='offsuit')
    hand_suited = Hand(hand="AJ", hand_type='suited')
    hand_pair = Hand(hand="AA", hand_type='pair')
    hand_nosuit = Hand(hand="83", hand_type='nosuit')

    assert(len(hand_offsuit.all_combos) == 12)
    assert(len(hand_suited.all_combos) == 4)
    assert(len(hand_pair.all_combos) == 6)
    assert(len(hand_nosuit.all_combos) == 16)


def test_get_all_combos_handstring():
    hand_offsuit = Hand(handstring='QJo')
    hand_suited = Hand(handstring='QJs')
    hand_pair = Hand(handstring='22')
    hand_nosuit = Hand(handstring='92')

    assert(len(hand_offsuit.all_combos) == 12)
    assert(len(hand_suited.all_combos) == 4)
    assert(len(hand_pair.all_combos) == 6)
    assert(len(hand_nosuit.all_combos) == 16)


def test_hand_index():
    hand_offsuit = Hand(handstring='QJo')
    hand_suited = Hand(handstring='QJs')
    hand_pair = Hand(handstring='22')
    hand_nosuit = Hand(handstring='92')

    assert(hand_offsuit.index_x == 3 and hand_offsuit.index_y == 4)
    assert(hand_suited.index_x == 4 and hand_suited.index_y == 3)
    assert(hand_pair.index_x == 13 and hand_pair.index_y == 13)
    assert(hand_nosuit.index_x == 6 and hand_nosuit.index_y == 13)


if __name__ == "__main__":
    test_get_all_combos_handstring()
    test_get_all_combos_hand_n_type()
    test_hand_index()
    print('jup')
