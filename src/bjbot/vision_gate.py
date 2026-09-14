"""Validation temporelle des observations avant toute décision."""

from __future__ import annotations

from dataclasses import dataclass

from .strategy import Action


@dataclass(frozen=True)
class Observation:
    round_id: str
    player_cards: tuple[str, ...]
    dealer_upcard: str
    available_actions: frozenset[Action]
    confidence: float


class StableObservationGate:
    """N'accepte qu'une lecture identique sur plusieurs images consécutives."""

    def __init__(self, minimum_confidence: float = 0.995, frames_required: int = 3):
        if not 0 < minimum_confidence <= 1:
            raise ValueError("minimum_confidence doit être dans ]0, 1]")
        if frames_required < 2:
            raise ValueError("frames_required doit être >= 2")
        self.minimum_confidence = minimum_confidence
        self.frames_required = frames_required
        self._last: Observation | None = None
        self._count = 0
        self._consumed_rounds: set[str] = set()

    def push(self, observation: Observation) -> Observation | None:
        if observation.confidence < self.minimum_confidence:
            self._last = None
            self._count = 0
            return None
        if observation.round_id in self._consumed_rounds:
            return None

        if observation == self._last:
            self._count += 1
        else:
            self._last = observation
            self._count = 1

        if self._count < self.frames_required:
            return None
        self._consumed_rounds.add(observation.round_id)
        return observation
