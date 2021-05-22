from pynlh import (Str2pynlh,
                   Hand,
                   OffsuitHand,
                   NoSuitHand,
                   SuitedHand,
                   PairHand,
                   Combo,
                   PairCombo,
                   SuitedCombo,
                   OffsuitCombo,
                   )


def test_get_offsuit_hand():
    AKo = Str2pynlh('AKo')
    AKo_obj = AKo.get_object()
    assert(str(AKo_obj) == 'AKo')
    assert(isinstance(AKo_obj, Hand))
    assert(isinstance(AKo_obj, OffsuitHand))


def test_get_suited_hand():
    AKs = Str2pynlh('AKs')
    AKs_obj = AKs.get_object()
    assert(str(AKs_obj) == 'AKs')
    assert(isinstance(AKs_obj, Hand))
    assert(isinstance(AKs_obj, SuitedHand))


def test_get_nosuit_hand():
    AK = Str2pynlh('AK')
    AK_obj = AK.get_object()
    assert(str(AK_obj) == 'AK')
    assert(isinstance(AK_obj, Hand))
    assert(isinstance(AK_obj, NoSuitHand))


def test_get_pair_hand():
    AA = Str2pynlh('AA')
    AA_obj = AA.get_object()
    assert(str(AA_obj) == 'AA')
    assert(isinstance(AA_obj, Hand))
    assert(isinstance(AA_obj, PairHand))


def test_get_offsuit_Combo():
    AKo = Str2pynlh('AhKs')
    AKo_obj = AKo.get_object()
    assert(str(AKo_obj) == 'AhKs')
    assert(isinstance(AKo_obj, Combo))
    assert(isinstance(AKo_obj, OffsuitCombo))


def test_get_suited_combo():
    AKs = Str2pynlh('AsKs')
    AKs_obj = AKs.get_object()
    assert(str(AKs_obj) == 'AsKs')
    assert(isinstance(AKs_obj, Combo))
    assert(isinstance(AKs_obj, SuitedCombo))


def test_get_pair_combo():
    AA = Str2pynlh('AcAh')
    AA_obj = AA.get_object()
    assert(str(AA_obj) == 'AcAh')
    assert(isinstance(AA_obj, Combo))
    assert(isinstance(AA_obj, PairCombo))
