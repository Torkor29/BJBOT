"""Stratégie de base paramétrable, indépendante de Gamdom et de l'écran."""

from __future__ import annotations

from enum import StrEnum


class Action(StrEnum):
    HIT = "tirer"
    STAND = "rester"
    DOUBLE = "doubler"
    SPLIT = "partager"
    SURRENDER = "abandonner"


_RANKS = {
    "A": 11,
    "K": 10,
    "Q": 10,
    "J": 10,
    "10": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


def normalize_rank(rank: str) -> str:
    value = rank.strip().upper()
    if value not in _RANKS:
        raise ValueError(f"Rang de carte invalide: {rank!r}")
    return value


def dealer_value(rank: str) -> int:
    return _RANKS[normalize_rank(rank)]


def hand_value(cards: list[str] | tuple[str, ...]) -> tuple[int, bool]:
    """Retourne (total, main_souple)."""
    if not cards:
        raise ValueError("Une main ne peut pas être vide")
    values = [_RANKS[normalize_rank(card)] for card in cards]
    total = sum(values)
    aces_as_eleven = values.count(11)
    while total > 21 and aces_as_eleven:
        total -= 10
        aces_as_eleven -= 1
    return total, aces_as_eleven > 0


def _pair_action(rank: str, dealer: int) -> Action | None:
    value = _RANKS[normalize_rank(rank)]
    if value == 11 or value == 8:
        return Action.SPLIT
    if value == 10:
        return Action.STAND
    if value == 9:
        return Action.SPLIT if dealer in {2, 3, 4, 5, 6, 8, 9} else Action.STAND
    if value == 7:
        return Action.SPLIT if dealer <= 7 else Action.HIT
    if value == 6:
        return Action.SPLIT if dealer <= 6 else Action.HIT
    if value == 5:
        return Action.DOUBLE if dealer <= 9 else Action.HIT
    if value == 4:
        return Action.SPLIT if dealer in {5, 6} else Action.HIT
    if value in {2, 3}:
        return Action.SPLIT if dealer <= 7 else Action.HIT
    return None


def _soft_action(total: int, dealer: int) -> Action:
    if total >= 19:
        return Action.STAND
    if total == 18:
        if dealer in {3, 4, 5, 6}:
            return Action.DOUBLE
        if dealer in {2, 7, 8}:
            return Action.STAND
        return Action.HIT
    if total == 17:
        return Action.DOUBLE if dealer in {3, 4, 5, 6} else Action.HIT
    if total in {15, 16}:
        return Action.DOUBLE if dealer in {4, 5, 6} else Action.HIT
    if total in {13, 14}:
        return Action.DOUBLE if dealer in {5, 6} else Action.HIT
    return Action.HIT


def _hard_action(total: int, dealer: int, surrender: bool) -> Action:
    if total >= 17:
        return Action.STAND
    if total == 16 and surrender and dealer in {9, 10, 11}:
        return Action.SURRENDER
    if total == 15 and surrender and dealer == 10:
        return Action.SURRENDER
    if 13 <= total <= 16:
        return Action.STAND if dealer <= 6 else Action.HIT
    if total == 12:
        return Action.STAND if dealer in {4, 5, 6} else Action.HIT
    if total == 11:
        return Action.DOUBLE if dealer <= 10 else Action.HIT
    if total == 10:
        return Action.DOUBLE if dealer <= 9 else Action.HIT
    if total == 9:
        return Action.DOUBLE if dealer in {3, 4, 5, 6} else Action.HIT
    return Action.HIT


def recommend(
    cards: list[str] | tuple[str, ...],
    dealer_upcard: str,
    *,
    can_double: bool = True,
    can_split: bool = True,
    can_surrender: bool = False,
) -> Action:
    """Recommande une action; l'assurance n'est jamais proposée."""
    normalized = [normalize_rank(card) for card in cards]
    dealer = dealer_value(dealer_upcard)

    if can_split and len(normalized) == 2 and normalized[0] == normalized[1]:
        pair = _pair_action(normalized[0], dealer)
        if pair is Action.SPLIT:
            return pair
        if pair is Action.DOUBLE:
            return pair if can_double else Action.HIT
        if pair is Action.STAND:
            return pair

    total, soft = hand_value(normalized)
    action = _soft_action(total, dealer) if soft else _hard_action(
        total, dealer, can_surrender
    )
    if action is Action.DOUBLE and not can_double:
        return Action.HIT
    return action
