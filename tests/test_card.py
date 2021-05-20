from pynlh import Card
four_hearts = Card.from_str('4h')
hearts_four = Card.from_str('h4')
hearts_five = Card.from_str('h5')
five_club = Card.from_str('5c')


def test_alternative_constructor():
    assert(isinstance(four_hearts, Card))
    assert(four_hearts is not None)


def test_eq():
    assert(four_hearts == hearts_four)
    assert(four_hearts != hearts_five)
    assert(five_club == hearts_five)


def test_gt():
    assert(hearts_five > four_hearts)
    assert(hearts_four < hearts_five)
