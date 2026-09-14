from bjbot.strategy import Action, hand_value, recommend


def test_ace_adjustment_and_soft_hand():
    assert hand_value(["A", "7"]) == (18, True)
    assert hand_value(["A", "7", "10"]) == (18, False)


def test_pair_aces_and_eights_are_split():
    assert recommend(["A", "A"], "10") is Action.SPLIT
    assert recommend(["8", "8"], "A") is Action.SPLIT


def test_never_split_tens():
    assert recommend(["10", "10"], "6") is Action.STAND


def test_soft_eighteen():
    assert recommend(["A", "7"], "6") is Action.DOUBLE
    assert recommend(["A", "7"], "8") is Action.STAND
    assert recommend(["A", "7"], "10") is Action.HIT


def test_hard_twelve():
    assert recommend(["10", "2"], "3") is Action.HIT
    assert recommend(["10", "2"], "4") is Action.STAND


def test_double_falls_back_to_hit():
    assert recommend(["5", "6"], "6", can_double=False) is Action.HIT


def test_surrender_is_optional():
    assert recommend(["10", "6"], "10", can_surrender=True) is Action.SURRENDER
    assert recommend(["10", "6"], "10", can_surrender=False) is Action.HIT
