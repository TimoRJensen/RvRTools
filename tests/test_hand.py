# import pytest

from pynlh import Hand, Combo


def test_hand_combo():
    combo1 = Hand('AsKs')
    combo2 = Hand('7s3d')
    assert(len(combo1) == 1)
    assert(len(combo2) == 1)


def test_get_all_combos_str_input():
    hand_offsuit = Hand(input='QJo')
    hand_suited = Hand(input='QJs')
    hand_pair = Hand(input='22')
    hand_nosuit = Hand(input='92')

    assert(len(hand_offsuit.all_combos_str) == 12)
    assert(len(hand_suited.all_combos_str) == 4)
    assert(len(hand_pair.all_combos_str) == 6)
    assert(len(hand_nosuit.all_combos_str) == 16)


def test_get_combos_str_input():
    hand_offsuit = Hand(input='QJo')
    hand_suited = Hand(input='QJs')
    hand_pair = Hand(input='22')
    hand_nosuit = Hand(input='92')

    assert(len(hand_offsuit.combos) == 12)
    assert(len(hand_suited.combos) == 4)
    assert(len(hand_pair.combos) == 6)
    assert(len(hand_nosuit.combos) == 16)


def test_get_combos_str_input_freq():
    hand_offsuit = Hand(input='QJo', input_freq=20)
    hand_suited = Hand(input='QJs', input_freq=20)
    hand_pair = Hand(input='22', input_freq=20)
    hand_nosuit = Hand(input='92', input_freq=20)

    assert(len(hand_offsuit.combos) == 12)
    assert(hand_offsuit.combos['QsJc'].freq == 20)
    assert(len(hand_suited.combos) == 4)
    assert(hand_suited.combos['QhJh'].freq == 20)
    assert(len(hand_pair.combos) == 6)
    assert(hand_pair.combos['2c2h'].freq == 20)
    assert(len(hand_nosuit.combos) == 16)
    assert(hand_nosuit.combos['9c2h'].freq == 20)


def test_hand_index():
    hand_offsuit = Hand(input='QJo')
    hand_suited = Hand(input='QJs')
    hand_pair = Hand(input='22')
    hand_nosuit = Hand(input='92')

    assert(hand_offsuit.index_x == 3 and hand_offsuit.index_y == 4)
    assert(hand_suited.index_x == 4 and hand_suited.index_y == 3)
    assert(hand_pair.index_x == 13 and hand_pair.index_y == 13)
    assert(hand_nosuit.index_x == 6 and hand_nosuit.index_y == 13)


def test_pick_combos():
    hand_offsuit = Hand(input='QJo', input_freq=20)
    hand_suited = Hand(input='QJs', input_freq=20)
    hand_pair = Hand(input='22', input_freq=20)
    hand_nosuit = Hand(input='92', input_freq=20)

    assert(len(hand_offsuit.apply_rng()) < 13 or hand_offsuit == [])
    assert(hand_offsuit.apply_rng() is not None)
    assert(len(hand_suited.apply_rng()) < 5 or hand_suited == [])
    assert(hand_suited.apply_rng() is not None)
    assert(len(hand_pair.apply_rng()) < 7 or hand_pair == [])
    assert(hand_pair.apply_rng() is not None)
    assert(len(hand_nosuit.apply_rng()) < 17 or hand_offsuit == [])
    assert(hand_nosuit.apply_rng() is not None)
    for combo in hand_nosuit.apply_rng():
        assert(isinstance(combo, Combo))


def test_ordering():
    threes = Hand("33")
    deuces = Hand("22")
    deuces2 = Hand("22")
    AKs = Hand("AKs")
    AKo = Hand("AKo")
    AQs = Hand("AQs")
    AJo = Hand("AJo")
    ten_nine = Hand("T9")
    ten_nine_off = Hand("T9o")
    ten_eight_suited = Hand("T8s")
    assert(deuces > AKs > AQs)
    assert(deuces > AKs > AQs > AJo > ten_nine)
    assert(AKo >= AQs)
    assert(AKo == AKs)
    assert(threes > deuces)
    assert(deuces2 >= deuces)
    assert(ten_nine < AJo)
    assert(ten_nine_off == ten_nine)
    assert(ten_nine_off > ten_eight_suited)
    assert(ten_eight_suited < ten_nine)


if __name__ == "__main__":
    # test_get_all_combos_str_input()
    # test_get_all_combos_str_hand_n_type()
    # test_hand_index()
    # print('jup')
    # test_hand_combo()
    # test_pick_combos_str()
    test_ordering()
