from pynlh import Combo, Str2pynlh, Pynlh

three_four_off = Combo.new('3s4d')
six_four_suited_50 = Combo.new('6d4d', 50)
threes = Str2pynlh('3s3c').get_object()
threes2 = Str2pynlh('3s3c').get_object()
fives = Str2pynlh('5h5c').get_object()
AKo = Str2pynlh('AcKh').get_object()
# AQs = Str2pynlh('AhQh').get_object()
AQs = Pynlh('AhQh').get()
AcKc = Pynlh('[99]AcKc[/99]').get()
deuces_dc = Pynlh('2c2d').get()


def test_init():
    assert(three_four_off is not None)
    assert(threes is not None)
    assert(fives is not None)


def test_freq_input():
    assert(three_four_off.freq == 100)
    assert(six_four_suited_50.freq == 50)


def test_comparisons():
    assert(six_four_suited_50 > three_four_off)
    assert(six_four_suited_50 >= three_four_off)
    assert(fives > threes)
    assert(fives != threes)
    assert(threes2 == threes)
    assert(fives >= threes)
    assert(not (fives <= threes))
    assert(not (fives < threes))
    assert(AKo > AQs)
    assert(AKo >= AQs)
    assert(threes > AKo)
    assert(threes >= AKo)
    assert(threes != AKo)
    assert(deuces_dc > AcKc)
    assert(AcKc == AKo)


def test_combo_repr():
    assert(repr(six_four_suited_50) == "Combo('[50]6d4d[/50]', freq=50)")
    assert(repr(three_four_off) == "Combo('4d3s')")


def test_combo_str():
    assert(str(six_four_suited_50) == '[50]6d4d[/50]')
    assert(str(three_four_off) == '4d3s')


if __name__ == "__main__":
    test_comparisons()
