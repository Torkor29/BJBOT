from bjbot.strategy import Action
from bjbot.vision_gate import Observation, StableObservationGate


def observation(confidence=0.999):
    return Observation(
        round_id="round-1",
        player_cards=("A", "7"),
        dealer_upcard="9",
        available_actions=frozenset({Action.HIT, Action.STAND}),
        confidence=confidence,
    )


def test_requires_three_stable_frames_and_consumes_round():
    gate = StableObservationGate(frames_required=3)
    assert gate.push(observation()) is None
    assert gate.push(observation()) is None
    assert gate.push(observation()) == observation()
    assert gate.push(observation()) is None


def test_low_confidence_resets_consensus():
    gate = StableObservationGate(frames_required=2)
    assert gate.push(observation()) is None
    assert gate.push(observation(0.8)) is None
    assert gate.push(observation()) is None
