from pynlh import Combo

three_four_off = Combo.new('3s4d')
six_four_suited_50 = Combo.new('6d4d', 50)


def test_init():
    assert(three_four_off is not None)


def test_freq_input():
    assert(three_four_off.freq == 100)
    assert(six_four_suited_50.freq == 50)


def test_gt():
    assert(six_four_suited_50 > three_four_off)


if __name__ == "__main__":
    test_gt()
