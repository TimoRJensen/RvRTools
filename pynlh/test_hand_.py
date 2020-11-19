# import pytest

from pynlh import Hand


def test_get_all_combos_hand_n_type(debug=False):
    hand_offsuit = Hand(hand="AJ", hand_type='offsuit')
    hand_offsuit_str = Hand(handstring="AJo")
    hand_suited = Hand(hand="AJ", hand_type='suited')
    hand_suited_str = Hand(handstring="AJs")
    hand_pair = Hand(hand="AA", hand_type='pair')
    hand_pair_str = Hand(hand="AA", hand_type='pair')
    if debug:
        print(f"""
            --Hand & Type:
              Pair: {hand_pair.all_combos}
              with lenght of {len(hand_pair.all_combos)}\n
              Offsuit: {hand_offsuit.all_combos}
              with lenght of {len(hand_offsuit.all_combos)}\n
              Suited: {hand_suited.all_combos}
              with lenght of {len(hand_suited.all_combos)}\n
        """)
    else:
        assert(len(hand_offsuit.all_combos) == 12)
        assert(len(hand_offsuit_str.all_combos) == 12)
        assert(len(hand_suited.all_combos) == 4)
        assert(len(hand_suited_str.all_combos) == 4)
        assert(len(hand_pair.all_combos) == 6)
        assert(len(hand_pair_str.all_combos) == 6)


def test_get_all_combos_handstring(debug=False):
    hand_offsuit = Hand(handstring='QJo')
    hand_suited = Hand(handstring='QJs')
    hand_pair = Hand(handstring='22')
    if debug:
        print(f"""
            --Handstring:
              Pair: {hand_pair.all_combos}
              with lenght of {len(hand_pair.all_combos)}\n
              Offsuit: {hand_offsuit.all_combos}
              with lenght of {len(hand_offsuit.all_combos)}\n
              Suited: {hand_suited.all_combos}
              with lenght of {len(hand_suited.all_combos)}\n
        """)
    else:
        assert(len(hand_offsuit.all_combos) == 12)
        assert(len(hand_suited.all_combos) == 4)
        assert(len(hand_pair.all_combos) == 6)


if __name__ == "__main__":
    test_get_all_combos_handstring(True)
    test_get_all_combos_hand_n_type(True)
