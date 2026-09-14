"""Limites de session contrôlées avant toute nouvelle exposition."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class StopReason(StrEnum):
    LOSS_LIMIT = "stop-loss atteint"
    PROFIT_LIMIT = "stop-win atteint"
    INSUFFICIENT_BALANCE = "solde insuffisant"
    ROUND_EXPOSURE = "exposition maximale de la main atteinte"


@dataclass(frozen=True)
class RiskConfig:
    stake_units: float = 1.0
    seats: int = 1
    stop_loss_fraction: float = 0.5
    take_profit_fraction: float = 10.0
    max_round_exposure_units: float = 4.0

    def __post_init__(self) -> None:
        if self.stake_units <= 0:
            raise ValueError("La mise doit être positive")
        if self.seats != 1:
            raise ValueError("Cette version est verrouillée à un seul siège")
        if not 0 < self.stop_loss_fraction < 1:
            raise ValueError("stop_loss_fraction doit être entre 0 et 1")
        if self.take_profit_fraction <= 0:
            raise ValueError("take_profit_fraction doit être positif")
        if self.max_round_exposure_units < 1:
            raise ValueError("max_round_exposure_units doit être >= 1")


@dataclass
class SessionRisk:
    starting_balance: float
    config: RiskConfig = RiskConfig()

    def __post_init__(self) -> None:
        if self.starting_balance <= 0:
            raise ValueError("Le solde initial doit être positif")

    @property
    def loss_floor(self) -> float:
        return self.starting_balance * self.config.stop_loss_fraction

    @property
    def profit_target(self) -> float:
        return self.starting_balance * (1 + self.config.take_profit_fraction)

    @property
    def max_round_exposure(self) -> float:
        return self.config.stake_units * self.config.max_round_exposure_units

    def stop_reason(self, balance: float) -> StopReason | None:
        if balance <= self.loss_floor:
            return StopReason.LOSS_LIMIT
        if balance >= self.profit_target:
            return StopReason.PROFIT_LIMIT
        return None

    def authorize_commit(
        self,
        *,
        balance: float,
        amount: float,
        round_exposure: float = 0.0,
    ) -> tuple[bool, StopReason | None]:
        reason = self.stop_reason(balance)
        if reason:
            return False, reason
        if amount <= 0 or balance < amount:
            return False, StopReason.INSUFFICIENT_BALANCE
        if balance - amount < self.loss_floor:
            return False, StopReason.LOSS_LIMIT
        if round_exposure + amount > self.max_round_exposure:
            return False, StopReason.ROUND_EXPOSURE
        return True, None
