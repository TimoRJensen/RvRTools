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
                   Range,
                   )


def test_get_offsuit_hand():
    AKo = Str2pynlh('AKo')
    AKo_50 = Str2pynlh('[50]AKo[/50]')
    AKo_obj = AKo.get_object()
    AKo_50_obj = AKo_50.get_object()
    assert(str(AKo_obj) == 'AKo')
    assert(isinstance(AKo_obj, Hand))
    assert(isinstance(AKo_obj, OffsuitHand))
    assert(str(AKo_50_obj) == 'AKo')
    assert(isinstance(AKo_50_obj, Hand))
    assert(isinstance(AKo_50_obj, OffsuitHand))
    assert(AKo_50_obj['AsKh'].freq == 50)


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


def test_get_pair_dash_range():
    aa_dash_jj = Str2pynlh('AA-JJ')
    aa_dash_jj_obj = aa_dash_jj.get_object()
    assert(isinstance(aa_dash_jj_obj, Range))
    assert(len(aa_dash_jj_obj) == 4 * 6)


def test_get_offsuit_dash_range():
    ako_dash_ajo = Str2pynlh('AKo-AJo')
    ako_dash_ajo_obj = ako_dash_ajo.get_object()
    assert(isinstance(ako_dash_ajo_obj, Range))
    assert(len(ako_dash_ajo_obj) == 3 * 12)


def test_get_comma_range_with_freq():
    range_50 = Str2pynlh('[50]AA[/50],KK-JJ').get_object()
    assert(isinstance(range_50, Range))
    assert(len(range_50) == 4 * 6)
    assert(range_50['AsAh'].freq == 50)
