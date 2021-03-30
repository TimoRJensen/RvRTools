from typing import Union
import pandas as pd
import pytest

from pynlh import Range, RangeError, HandError, RangePart


def test_mixed_suit():
    with pytest.raises(RangeError):
        Range('KQs-K9o')


def test_mixed_rank():
    with pytest.raises(RangeError):
        Range('Q9s-K9o')


def test_omitted_suit_start():
    with pytest.raises(RangeError):
        Range('KQ-K9o')


def test_omitted_suit_end():
    with pytest.raises(RangeError):
        Range('KQs-K9')


def test_omitted_rank_start():
    with pytest.raises(HandError):
        Range('Qs-Q9s')


def test_omitted_rank_end():
    with pytest.raises(HandError):
        Range('Q9o-Qo')


def test_tripple_range():
    with pytest.raises(RangeError):
        Range('Q9o-Q7o-Q2o')


def test_suited_pair():
    with pytest.raises(RangeError):
        Range('JJs')


def test_not_expected_char():
    with pytest.raises(RangeError):
        Range('JJx')

# 2020-11-14  commented out and postponed.
# def test_gapper_suited():
#     range_gap_s = Range('JTs-43s')
#     assert(range_gap_s.converted_range_dict['JTs'] == 100)
#     assert(range_gap_s.converted_range_dict['98s'] == 100)
#     assert(range_gap_s.converted_range_dict['87s'] == 100)
#     assert(range_gap_s.converted_range_dict['76s'] == 100)
#     assert(range_gap_s.converted_range_dict['65s'] == 100)
#     assert(range_gap_s.converted_range_dict['54s'] == 100)
#     assert(range_gap_s.converted_range_dict['43s'] == 100)
#     assert(len(range_gap_s.converted_range_dict) == 7)


# def test_2gapper_suited():
#     range_2gap_s = Range('J9s-42s')
#     assert(range_2gap_s.converted_range_dict['J9s'] == 100)
#     assert(range_2gap_s.converted_range_dict['97s'] == 100)
#     assert(range_2gap_s.converted_range_dict['86s'] == 100)
#     assert(range_2gap_s.converted_range_dict['75s'] == 100)
#     assert(range_2gap_s.converted_range_dict['64s'] == 100)
#     assert(range_2gap_s.converted_range_dict['53s'] == 100)
#     assert(range_2gap_s.converted_range_dict['42s'] == 100)
#     assert(len(range_2gap_s.converted_range_dict) == 7)


# def test_gapper_offsuit():
#     range_gap_o = Range('JTo-43o')
#     assert(range_gap_o.converted_range_dict['JTs'] == 100)
#     assert(range_gap_o.converted_range_dict['98s'] == 100)
#     assert(range_gap_o.converted_range_dict['87s'] == 100)
#     assert(range_gap_o.converted_range_dict['76s'] == 100)
#     assert(range_gap_o.converted_range_dict['65s'] == 100)
#     assert(range_gap_o.converted_range_dict['54s'] == 100)
#     assert(range_gap_o.converted_range_dict['43s'] == 100)
#     assert(len(range_gap_o.converted_range_dict) == 7)


# def test_2gapper_offsuit():
#     range_2gap_o = Range('J9o-42o')
#     assert(range_2gap_o.converted_range_dict['J9o'] == 100)
#     assert(range_2gap_o.converted_range_dict['97o'] == 100)
#     assert(range_2gap_o.converted_range_dict['86o'] == 100)
#     assert(range_2gap_o.converted_range_dict['75o'] == 100)
#     assert(range_2gap_o.converted_range_dict['64o'] == 100)
#     assert(range_2gap_o.converted_range_dict['53o'] == 100)
#     assert(range_2gap_o.converted_range_dict['42o'] == 100)
#     assert(len(range_2gap_o.converted_range_dict) == 7)


def test_range_hands():
    range_hands = Range('AA,KK,AKs,AKo,97o,97s')
    assert(range_hands.converted_range_dict['AA'] == 100)
    assert(range_hands.converted_range_dict['KK'] == 100)
    assert(range_hands.converted_range_dict['AKo'] == 100)
    assert(range_hands.converted_range_dict['AKs'] == 100)
    assert(range_hands.converted_range_dict['97o'] == 100)
    assert(range_hands.converted_range_dict['97s'] == 100)
    assert(len(range_hands.converted_range_dict) == 6)


def test_range_ranges():
    range_ranges = Range('AA-JJ,AKs-ATs,KQo-K5o')
    assert(range_ranges.converted_range_dict['AA'] == 100)
    assert(range_ranges.converted_range_dict['KK'] == 100)
    assert(range_ranges.converted_range_dict['QQ'] == 100)
    assert(range_ranges.converted_range_dict['JJ'] == 100)
    assert(range_ranges.converted_range_dict['AKs'] == 100)
    assert(range_ranges.converted_range_dict['AQs'] == 100)
    assert(range_ranges.converted_range_dict['AJs'] == 100)
    assert(range_ranges.converted_range_dict['ATs'] == 100)
    assert(range_ranges.converted_range_dict['KQo'] == 100)
    assert(range_ranges.converted_range_dict['KJo'] == 100)
    assert(range_ranges.converted_range_dict['KTo'] == 100)
    assert(range_ranges.converted_range_dict['K9o'] == 100)
    assert(range_ranges.converted_range_dict['K8o'] == 100)
    assert(range_ranges.converted_range_dict['K7o'] == 100)
    assert(range_ranges.converted_range_dict['K6o'] == 100)
    assert(range_ranges.converted_range_dict['K5o'] == 100)
    assert(len(range_ranges.converted_range_dict) == 16)


def test_range_plus_ranges():
    range_plus_ranges = Range('22+,A5s+,A6o+')
    assert(range_plus_ranges.converted_range_dict['AA'] == 100)
    assert(range_plus_ranges.converted_range_dict['KK'] == 100)
    assert(range_plus_ranges.converted_range_dict['QQ'] == 100)
    assert(range_plus_ranges.converted_range_dict['JJ'] == 100)
    assert(range_plus_ranges.converted_range_dict['TT'] == 100)
    assert(range_plus_ranges.converted_range_dict['99'] == 100)
    assert(range_plus_ranges.converted_range_dict['88'] == 100)
    assert(range_plus_ranges.converted_range_dict['77'] == 100)
    assert(range_plus_ranges.converted_range_dict['66'] == 100)
    assert(range_plus_ranges.converted_range_dict['55'] == 100)
    assert(range_plus_ranges.converted_range_dict['44'] == 100)
    assert(range_plus_ranges.converted_range_dict['33'] == 100)
    assert(range_plus_ranges.converted_range_dict['22'] == 100)
    assert(range_plus_ranges.converted_range_dict['AKs'] == 100)
    assert(range_plus_ranges.converted_range_dict['AQs'] == 100)
    assert(range_plus_ranges.converted_range_dict['AJs'] == 100)
    assert(range_plus_ranges.converted_range_dict['ATs'] == 100)
    assert(range_plus_ranges.converted_range_dict['A9s'] == 100)
    assert(range_plus_ranges.converted_range_dict['A8s'] == 100)
    assert(range_plus_ranges.converted_range_dict['A7s'] == 100)
    assert(range_plus_ranges.converted_range_dict['A6s'] == 100)
    assert(range_plus_ranges.converted_range_dict['A5s'] == 100)
    assert(range_plus_ranges.converted_range_dict['AKo'] == 100)
    assert(range_plus_ranges.converted_range_dict['AQo'] == 100)
    assert(range_plus_ranges.converted_range_dict['AJo'] == 100)
    assert(range_plus_ranges.converted_range_dict['ATo'] == 100)
    assert(range_plus_ranges.converted_range_dict['A9o'] == 100)
    assert(range_plus_ranges.converted_range_dict['A8o'] == 100)
    assert(range_plus_ranges.converted_range_dict['A7o'] == 100)
    assert(range_plus_ranges.converted_range_dict['A6o'] == 100)
    assert(len(range_plus_ranges.converted_range_dict) == 30)


def test_range_hands_freq():
    rhf = '[20]AA,KK,AKs[/20],[79]AKo[/79],97o,97s'
    range_hands_freq = Range(rhf)
    assert(range_hands_freq.converted_range_dict['AA'] == 20)
    assert(range_hands_freq.converted_range_dict['KK'] == 20)
    assert(range_hands_freq.converted_range_dict['AKs'] == 20)
    assert(range_hands_freq.converted_range_dict['AKo'] == 79)
    assert(range_hands_freq.converted_range_dict['97o'] == 100)
    assert(range_hands_freq.converted_range_dict['97s'] == 100)
    assert(len(range_hands_freq.converted_range_dict) == 6)


def test_range_ranges_freq():
    rrf = '[20]AA-JJ[/20],[5.2]AKs-ATs,KQo-K5o[/5.2]'
    range_ranges_freq = Range(rrf)
    assert(range_ranges_freq.converted_range_dict['AA'] == 20)
    assert(range_ranges_freq.converted_range_dict['KK'] == 20)
    assert(range_ranges_freq.converted_range_dict['QQ'] == 20)
    assert(range_ranges_freq.converted_range_dict['JJ'] == 20)
    assert(range_ranges_freq.converted_range_dict['AKs'] == 5.2)
    assert(range_ranges_freq.converted_range_dict['AQs'] == 5.2)
    assert(range_ranges_freq.converted_range_dict['AJs'] == 5.2)
    assert(range_ranges_freq.converted_range_dict['ATs'] == 5.2)
    assert(range_ranges_freq.converted_range_dict['KQo'] == 5.2)
    assert(range_ranges_freq.converted_range_dict['KJo'] == 5.2)
    assert(range_ranges_freq.converted_range_dict['KTo'] == 5.2)
    assert(range_ranges_freq.converted_range_dict['K9o'] == 5.2)
    assert(range_ranges_freq.converted_range_dict['K8o'] == 5.2)
    assert(range_ranges_freq.converted_range_dict['K7o'] == 5.2)
    assert(range_ranges_freq.converted_range_dict['K6o'] == 5.2)
    assert(range_ranges_freq.converted_range_dict['K5o'] == 5.2)
    assert(len(range_ranges_freq.converted_range_dict) == 16)


def test_range_plus_ranges_freq(debug=False):
    range_plus_ranges_freq = Range('[20]22+,A2s+[/20],[2]A6o+[/2]')
    if debug:
        print(range_plus_ranges_freq.converted_range_dict)
    assert(range_plus_ranges_freq.converted_range_dict['AA'] == 20)
    assert(range_plus_ranges_freq.converted_range_dict['KK'] == 20)
    assert(range_plus_ranges_freq.converted_range_dict['QQ'] == 20)
    assert(range_plus_ranges_freq.converted_range_dict['JJ'] == 20)
    assert(range_plus_ranges_freq.converted_range_dict['TT'] == 20)
    assert(range_plus_ranges_freq.converted_range_dict['99'] == 20)
    assert(range_plus_ranges_freq.converted_range_dict['88'] == 20)
    assert(range_plus_ranges_freq.converted_range_dict['77'] == 20)
    assert(range_plus_ranges_freq.converted_range_dict['66'] == 20)
    assert(range_plus_ranges_freq.converted_range_dict['55'] == 20)
    assert(range_plus_ranges_freq.converted_range_dict['44'] == 20)
    assert(range_plus_ranges_freq.converted_range_dict['33'] == 20)
    assert(range_plus_ranges_freq.converted_range_dict['22'] == 20)
    assert(range_plus_ranges_freq.converted_range_dict['AKs'] == 20)
    assert(range_plus_ranges_freq.converted_range_dict['AQs'] == 20)
    assert(range_plus_ranges_freq.converted_range_dict['AJs'] == 20)
    assert(range_plus_ranges_freq.converted_range_dict['ATs'] == 20)
    assert(range_plus_ranges_freq.converted_range_dict['A9s'] == 20)
    assert(range_plus_ranges_freq.converted_range_dict['A8s'] == 20)
    assert(range_plus_ranges_freq.converted_range_dict['A7s'] == 20)
    assert(range_plus_ranges_freq.converted_range_dict['A6s'] == 20)
    assert(range_plus_ranges_freq.converted_range_dict['A5s'] == 20)
    assert(range_plus_ranges_freq.converted_range_dict['A4s'] == 20)
    assert(range_plus_ranges_freq.converted_range_dict['A3s'] == 20)
    assert(range_plus_ranges_freq.converted_range_dict['A2s'] == 20)
    assert(range_plus_ranges_freq.converted_range_dict['AKo'] == 2)
    assert(range_plus_ranges_freq.converted_range_dict['AQo'] == 2)
    assert(range_plus_ranges_freq.converted_range_dict['AJo'] == 2)
    assert(range_plus_ranges_freq.converted_range_dict['ATo'] == 2)
    assert(range_plus_ranges_freq.converted_range_dict['A9o'] == 2)
    assert(range_plus_ranges_freq.converted_range_dict['A8o'] == 2)
    assert(range_plus_ranges_freq.converted_range_dict['A7o'] == 2)
    assert(range_plus_ranges_freq.converted_range_dict['A6o'] == 2)
    assert(len(range_plus_ranges_freq.converted_range_dict) == 33)


def test_hand_no_suit():
    range = Range('54')
    assert(range.converted_range_dict['54s'] == 100)
    assert(range.converted_range_dict['54o'] == 100)


# def test_hand_no_suit_plus():
#     range = Range('53+')
#     assert(range.converted_range_dict['54s'] == 100)
#     assert(range.converted_range_dict['54o'] == 100)
#     assert(range.converted_range_dict['53s'] == 100)
#     assert(range.converted_range_dict['53o'] == 100)
#     assert(len(range.converted_range_dict) == 4)


# def test_hand_no_suit_range():
#     range = Range('54-52')
#     assert(range.converted_range_dict['54s'] == 100)
#     assert(range.converted_range_dict['54o'] == 100)
#     assert(range.converted_range_dict['53s'] == 100)
#     assert(range.converted_range_dict['53o'] == 100)
#     assert(range.converted_range_dict['52s'] == 100)
#     assert(range.converted_range_dict['52o'] == 100)
#     assert(len(range.converted_range_dict) == 6)


def test_split_range_str_in_parts():
    range_ = Range('[20]AA,KK,AKs[/20],[79]AKo[/79],97o,97s')
    assert(len(range_.split_range_str_in_parts()) == 6)


def test_part_combos_count():
    range_part_hand = RangePart('[20]AA[/20]')
    range_part_dash = RangePart('[79]AKo-AJo[/79]')
    range_part_plus = RangePart('[79]QTs+[/79]')
    assert(len(range_part_hand.combos) == 6)
    assert(len(range_part_dash.combos) == 36)
    assert(len(range_part_plus.combos) == 8)


def test_range_combos_count():
    range_hands = Range('[20]AA,KK,AK[/20]')
    range_dash = Range('[79]AKo-AJo[/79],AA')
    range_plus = Range('[79]QTs+[/79],[99]KTs+[/99]')
    assert(len(range_hands.combos) == 28)
    assert(len(range_dash.combos) == 42)
    assert(len(range_plus.combos) == 20)


def test_part_pick_combo():
    range_part_hand = RangePart('[20]AA[/20]')
    assert(cycle_pick_combos_for(range_part_hand))
    range_part_dash = RangePart('[79]AKo-AJo[/79]')
    assert(cycle_pick_combos_for(range_part_dash))
    range_part_plus = RangePart('[99]KTs+[/99]')
    assert(cycle_pick_combos_for(range_part_plus))


def test_range_pick_combo():
    range_hands = Range('[20]AA,KK,AK[/20]')
    assert(cycle_pick_combos_for(range_hands))
    range_dash = Range('AA,22,33,55,[79]AKo-AJo[/79]')
    assert(cycle_pick_combos_for(range_dash))
    range_plus = Range('[79]QTs+[/79],[99]KTs+[/99]')
    assert(cycle_pick_combos_for(range_plus))


def cycle_pick_combos_for(obj: Union[RangePart, Range]):
    CYCLES = 1000
    TOL = 0.1
    combos = obj.combos
    calc_combos = 0
    if isinstance(obj, RangePart):
        calc_combos = (obj.freq / 100) * len(combos)
    elif isinstance(obj, Range):
        for part in obj.parts:
            calc_combos += len(part.combos) * (part.freq / 100)
    else:
        raise ValueError
    bottom = calc_combos * (1 - TOL)
    top = calc_combos * (1 + TOL)
    picks = []
    for _ in range(CYCLES):
        x = len(obj.pick_combos())
        picks.append(x)
    count_picks = pd.DataFrame(picks, columns=['picks'])
    mean = count_picks.picks.mean()
    return (top > mean > bottom)


def test_randomizer_skl_mal():
    """
    Tests the Suits Randomizer using the Sklansky Malmuth grouping
    """
    range_50 = Range('[50]AA[/50]')
    range_15 = Range('[15]AA[/15]')
    rand_combos_50 = range_50.randomize_suits_for_range(grouping='skl-mal')
    rand_combos_15 = range_15.randomize_suits_for_range(grouping='skl-mal')
    assert(len(rand_combos_50) == 14)
    assert(len(rand_combos_15) == 4)


def test_range_subtraction():
    range_50 = Range('[50]AA[/50],KK-JJ')
    range_15 = Range('[15]AA[/15],JJ')
    range_diff = range_50 - range_15
    assert('JJ' not in range_diff)
    assert('KK' in range_diff)
    assert(range_diff['AA'] == 35)
    assert(range_50['AA'] == 50)


def test_range_addition():
    range_50 = Range('[50]AA[/50],KK-JJ')
    range_15 = Range('[15]AA[/15],TT')
    range_sum = range_50 + range_15
    assert('TT' in range_sum)
    assert('99' not in range_sum)
    assert(range_sum['AA'] == 65)
    assert(range_50['AA'] == 50)
    assert(range_15['AA'] == 15)


def test_range_iter():
    range_50 = Range('[50]AA[/50],KK-JJ')
    i = sum(1 for hand, freq in range_50)
    assert(i == 4)
    assert(i != 5)


def test_range_len():
    range_50 = Range('[50]AA[/50],KK-JJ')
    assert(len(range_50) == 4)
    assert(len(range_50) != 3)


def test_full_range():
    full_range = Range.full_range()
    assert(len(full_range) == 169)
    assert(full_range['54s'] == 100)


def test_combo_range():
    combo_range = Range('AsKh,AsKd,AhQs')
    assert(len(combo_range) == 2)


if __name__ == "__main__":
    # test_range_hands()
    # test_range_ranges()
    # test_range_plus_ranges()
    # test_range_hands_freq()
    # test_range_ranges_freq()
    # test_range_plus_ranges_freq(True)
    # test_split_range_str_in_parts()
    # test_part_pick_combo()
    # test_omitted_rank_start()
    test_tripple_range()
    # plt.show()
    # test_mixed_rank()
    # test_range_subtraction()
