from typing import Union
import pandas as pd
import pytest

from pynlh import Range, RangeError, HandError, RangePart, Str2pynlh


def test_mixed_suit():
    with pytest.raises(RangeError):
        r = Range('KQs-K9o')
        print(r)


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
    with pytest.raises(HandError):
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
    assert(range_hands['AA'].freq == 100)
    assert('AA' in range_hands)
    assert(range_hands['KK'].freq == 100)
    assert('KK' in range_hands)
    assert(range_hands['AKo'].freq == 100)
    assert('AKo' in range_hands)
    assert(range_hands['AKs'].freq == 100)
    assert('AKs' in range_hands)
    assert(range_hands['97o'].freq == 100)
    assert('97o' in range_hands)
    assert(range_hands['97s'].freq == 100)
    assert('97s' in range_hands)
    assert(len(range_hands) == 2 * 6 + 2 * 12 + 2 * 4)


def test_range_ranges():
    range_ranges = Range('AA-JJ,AKs-ATs,KQo-K5o')
    assert(range_ranges['AA'].freq == 100)
    assert('AA' in range_ranges)
    assert(range_ranges['KK'].freq == 100)
    assert('KK' in range_ranges)
    assert(range_ranges['QQ'].freq == 100)
    assert('QQ' in range_ranges)
    assert(range_ranges['JJ'].freq == 100)
    assert('JJ' in range_ranges)
    assert(range_ranges['AKs'].freq == 100)
    assert('AKs' in range_ranges)
    assert(range_ranges['AQs'].freq == 100)
    assert('AQs' in range_ranges)
    assert(range_ranges['AJs'].freq == 100)
    assert('AJs' in range_ranges)
    assert(range_ranges['ATs'].freq == 100)
    assert('ATs' in range_ranges)
    assert(range_ranges['KQo'].freq == 100)
    assert('ATs' in range_ranges)
    assert(range_ranges['KJo'].freq == 100)
    assert('KJo' in range_ranges)
    assert(range_ranges['KTo'].freq == 100)
    assert('KTo' in range_ranges)
    assert(range_ranges['K9o'].freq == 100)
    assert('K9o' in range_ranges)
    assert(range_ranges['K8o'].freq == 100)
    assert('K8o' in range_ranges)
    assert(range_ranges['K7o'].freq == 100)
    assert('K7o' in range_ranges)
    assert(range_ranges['K6o'].freq == 100)
    assert('K6o' in range_ranges)
    assert(range_ranges['K5o'].freq == 100)
    assert('K5o' in range_ranges)
    assert(len(range_ranges) == 4 * 6 + 4 * 4 + 8 * 12)


def test_range_plus_ranges():
    range_plus_ranges = Range('22+,A5s+,A6o+')
    assert('AA' in range_plus_ranges)
    assert('KK' in range_plus_ranges)
    assert('QQ' in range_plus_ranges)
    assert('JJ' in range_plus_ranges)
    assert('TT' in range_plus_ranges)
    assert('99' in range_plus_ranges)
    assert('88' in range_plus_ranges)
    assert('77' in range_plus_ranges)
    assert('66' in range_plus_ranges)
    assert('55' in range_plus_ranges)
    assert('44' in range_plus_ranges)
    assert('33' in range_plus_ranges)
    assert('22' in range_plus_ranges)
    assert('AKs' in range_plus_ranges)
    assert('AQs' in range_plus_ranges)
    assert('AJs' in range_plus_ranges)
    assert('ATs' in range_plus_ranges)
    assert('A9s' in range_plus_ranges)
    assert('A8s' in range_plus_ranges)
    assert('A7s' in range_plus_ranges)
    assert('A6s' in range_plus_ranges)
    assert('A5s' in range_plus_ranges)
    assert('AKo' in range_plus_ranges)
    assert('AQo' in range_plus_ranges)
    assert('AJo' in range_plus_ranges)
    assert('ATo' in range_plus_ranges)
    assert('A9o' in range_plus_ranges)
    assert('A8o' in range_plus_ranges)
    assert('A7o' in range_plus_ranges)
    assert('A6o' in range_plus_ranges)
    assert(len(range_plus_ranges) == 210)


def test_range_hands_freq():
    rhf = '[20]AA,KK,AKs[/20],[79]AKo[/79],97o,97s'
    range_hands_freq = Range(rhf)
    assert(range_hands_freq['AA'].freq == 20)
    assert(range_hands_freq['KK'].freq == 20)
    assert(range_hands_freq['AKs'].freq == 20)
    assert(range_hands_freq['AKo'].freq == 79)
    assert(range_hands_freq['97o'].freq == 100)
    assert(range_hands_freq['97s'].freq == 100)


def test_range_ranges_freq():
    rrf = '[20]AA-JJ[/20],[5.2]AKs-ATs,KQo-K5o[/5.2]'
    range_ranges_freq = Range(rrf)
    assert(range_ranges_freq['AA'].freq == 20)
    assert(range_ranges_freq['KK'].freq == 20)
    assert(range_ranges_freq['QQ'].freq == 20)
    assert(range_ranges_freq['JJ'].freq == 20)
    assert(range_ranges_freq['AKs'].freq == 5.2)
    assert(range_ranges_freq['AQs'].freq == 5.2)
    assert(range_ranges_freq['AJs'].freq == 5.2)
    assert(range_ranges_freq['ATs'].freq == 5.2)
    assert(range_ranges_freq['KQo'].freq == 5.2)
    assert(range_ranges_freq['KJo'].freq == 5.2)
    assert(range_ranges_freq['KTo'].freq == 5.2)
    assert(range_ranges_freq['K9o'].freq == 5.2)
    assert(range_ranges_freq['K8o'].freq == 5.2)
    assert(range_ranges_freq['K7o'].freq == 5.2)
    assert(range_ranges_freq['K6o'].freq == 5.2)
    assert(range_ranges_freq['K5o'].freq == 5.2)


def test_range_plus_ranges_freq():
    range_plus_ranges_freq = Range('[20]22+,A2s+[/20],[2]A6o+[/2]')
    assert(range_plus_ranges_freq['AsAc'].freq == 20)
    assert(range_plus_ranges_freq['KsKc'].freq == 20)
    assert(range_plus_ranges_freq['QsQc'].freq == 20)
    assert(range_plus_ranges_freq['JsJc'].freq == 20)
    assert(range_plus_ranges_freq['TsTc'].freq == 20)
    assert(range_plus_ranges_freq['9s9c'].freq == 20)
    assert(range_plus_ranges_freq['8s8c'].freq == 20)
    assert(range_plus_ranges_freq['7s7c'].freq == 20)
    assert(range_plus_ranges_freq['6s6c'].freq == 20)
    assert(range_plus_ranges_freq['5s5c'].freq == 20)
    assert(range_plus_ranges_freq['4s4c'].freq == 20)
    assert(range_plus_ranges_freq['3s3c'].freq == 20)
    assert(range_plus_ranges_freq['2s2c'].freq == 20)
    assert(range_plus_ranges_freq['AsKs'].freq == 20)
    assert(range_plus_ranges_freq['AsQs'].freq == 20)
    assert(range_plus_ranges_freq['AsJs'].freq == 20)
    assert(range_plus_ranges_freq['AsTs'].freq == 20)
    assert(range_plus_ranges_freq['As9s'].freq == 20)
    assert(range_plus_ranges_freq['As8s'].freq == 20)
    assert(range_plus_ranges_freq['As7s'].freq == 20)
    assert(range_plus_ranges_freq['As6s'].freq == 20)
    assert(range_plus_ranges_freq['As5s'].freq == 20)
    assert(range_plus_ranges_freq['As4s'].freq == 20)
    assert(range_plus_ranges_freq['As3s'].freq == 20)
    assert(range_plus_ranges_freq['As2s'].freq == 20)
    assert(range_plus_ranges_freq['AsKh'].freq == 2)
    assert(range_plus_ranges_freq['AsQh'].freq == 2)
    assert(range_plus_ranges_freq['AsJh'].freq == 2)
    assert(range_plus_ranges_freq['AsTh'].freq == 2)
    assert(range_plus_ranges_freq['As9h'].freq == 2)
    assert(range_plus_ranges_freq['As8h'].freq == 2)
    assert(range_plus_ranges_freq['As7h'].freq == 2)
    assert(range_plus_ranges_freq['As6h'].freq == 2)
    assert(len(range_plus_ranges_freq) == ((13 * 6) + (12 * 4) + (8 * 12)))


def test_hand_no_suit():
    r = Range('54')
    assert('54s' in r)
    assert('54o' in r)
    assert('65s' not in r)


# def test_hand_no_suit_plus():
#     range = Range('53+')
#     assert(range['54s'].freq == 100)
#     assert(range['54o'].freq == 100)
#     assert(range['53s'].freq == 100)
#     assert(range['53o'].freq == 100)
#     assert('54s' in range)
#     assert('54o' in range)
#     assert('53s' in range)
#     assert('53o' in range)
#     assert(len(range) == 2 * 4 + 2 * 12)
#  2021-05-22 TJ: +-ranges do not work with nosuit hands yet
#                 and I don't think I need that.

# def test_hand_no_suit_range():
#     range = Range('54-52')
#     assert(range['54s'].freq == 100)
#     assert(range['54o'].freq == 100)
#     assert(range['53s'].freq == 100)
#     assert(range['53o'].freq == 100)
#     assert(range['52s'].freq == 100)
#     assert(range['52o'].freq == 100)
#     assert('54s' in range)
#     assert('54o' in range)
#     assert('53s' in range)
#     assert('53o' in range)
#     assert(len(range) == 2 * 4 + 2 * 12)


def test_split_range_str_in_parts():
    range_ = Range('[20]AA,KK,AKs[/20],[79]AKo[/79],97o,97s')
    assert(len(range_._split_range_str_in_parts(range_.input)) == 6)


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
        for part in obj._parts:
            calc_combos += len(part.combos) * (part.freq / 100)
    else:
        raise ValueError
    bottom = calc_combos * (1 - TOL)
    top = calc_combos * (1 + TOL)
    picks = []
    for _ in range(CYCLES):
        x = len(obj.apply_rng())
        picks.append(x)
    count_picks = pd.DataFrame(picks, columns=['picks'])
    mean = count_picks.picks.mean()
    return (top > mean > bottom)


def test_range_subtraction():
    range_50 = Range('[50]AA[/50],KK-JJ')
    range_15 = Range('[15]AA[/15],JJ,KcKh')
    range_diff = range_50 - range_15
    assert('JJ' not in range_diff)
    assert('KsKc' in range_diff)
    assert('KhKc' not in range_diff)
    assert('KcKh' not in range_diff)
    assert(range_diff['KsKc'].freq == 100)
    assert(range_diff['AcAs'].freq == 35)
    assert(range_50['AhAc'].freq == 50)


def test_range_addition():
    range_50 = Range('[50]AA[/50],KK-JJ')
    range_15 = Range('[15]AA[/15],TT')
    range_sum = range_50 + range_15
    assert('TT' in range_sum)
    assert('99' not in range_sum)
    assert(range_sum['AcAh'].freq == 65)
    assert(range_50['AsAd'].freq == 50)
    assert(range_15['AdAc'].freq == 15)


def test_range_addition_with_combos():
    range_50 = Str2pynlh('[50]AA[/50],KK-JJ').get_object()
    range_15 = Str2pynlh('[15]AA[/15],TT,9c9s,[10]8s8c[/10]').get_object()
    range_sum = range_50 + range_15
    assert('TT' in range_sum)
    assert('66' not in range_sum)
    assert('9c9s' in range_sum)
    assert(range_sum['AsAh'].freq == 65)
    assert(range_sum['9s9c'].freq == 100)
    assert(range_sum['8s8c'].freq == 10)
    assert(range_50['AcAs'].freq == 50)
    assert(range_15['AhAd'].freq == 15)


def test_range_iter():
    range_50 = Range('[50]AA[/50],KK-JJ')
    for i, _ in enumerate(range_50):
        pass
    assert(i == 23)


def test_range_len():
    range_50 = Range('[50]AA[/50],KK-JJ')
    assert(len(range_50) == 24)
    assert(len(range_50) != 23)


def test_full_range():
    full_range = Range.full_range()
    assert(len(full_range) == 1326)
    assert('54s' in full_range)


def test_combo_range():
    combo_range = Range('AsKh,AsKd,AhQs')
    assert(len(combo_range) == 3)


def test_combo_contain():
    combo_range = Range('AsKh,AsKd,AhQs')
    assert('AsKh' in combo_range)
    assert('AhKh' not in combo_range)


def test_contain_subrange():
    r = Range('22+')
    b = '55-33' in r
    c = 'QQ+' in r
    assert b
    assert c


def test_contain_subrange_reversed():
    r = Range('22+')
    b = '33-55' in r
    assert b


def test_get_object():
    str2 = Str2pynlh('AKo')
    obj = str2.get_object()
    assert(obj is not None)


if __name__ == "__main__":
    # test_range_hands()
    # test_range_ranges()
    # test_range_plus_ranges()
    # test_range_hands_freq()
    # test_range_ranges_freq()
    # test_range_plus_ranges_freq(True)
    test_split_range_str_in_parts()
    # test_part_pick_combo()
    # test_omitted_rank_start()
    # test_tripple_range()
    # plt.show()
    # test_mixed_suit()
    # test_range_subtraction()
    # test_range_pick_combo()
    # test_combo_range()
    test_contain_subrange()
