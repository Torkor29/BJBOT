from bjbot.risk import RiskConfig, SessionRisk, StopReason


def test_selected_session_thresholds():
    risk = SessionRisk(100, RiskConfig())
    assert risk.loss_floor == 50
    assert risk.profit_target == 1100
    assert risk.stop_reason(50) is StopReason.LOSS_LIMIT
    assert risk.stop_reason(1100) is StopReason.PROFIT_LIMIT


def test_commit_cannot_cross_loss_floor():
    risk = SessionRisk(100)
    allowed, reason = risk.authorize_commit(balance=50.5, amount=1)
    assert not allowed
    assert reason is StopReason.LOSS_LIMIT


def test_round_exposure_is_capped():
    risk = SessionRisk(100)
    allowed, reason = risk.authorize_commit(
        balance=100, amount=1, round_exposure=4
    )
    assert not allowed
    assert reason is StopReason.ROUND_EXPOSURE
