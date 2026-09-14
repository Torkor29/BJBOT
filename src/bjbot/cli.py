"""Petit outil local pour vérifier le moteur avant l'intégration écran."""

from __future__ import annotations

import argparse

from .strategy import recommend


def main() -> None:
    parser = argparse.ArgumentParser(description="Recommandation Blackjack BJBOT")
    parser.add_argument("--cards", required=True, help="Cartes séparées par des virgules")
    parser.add_argument("--dealer", required=True, help="Carte visible du croupier")
    parser.add_argument("--no-double", action="store_true")
    parser.add_argument("--no-split", action="store_true")
    parser.add_argument("--surrender", action="store_true")
    args = parser.parse_args()

    cards = [card.strip() for card in args.cards.split(",") if card.strip()]
    action = recommend(
        cards,
        args.dealer,
        can_double=not args.no_double,
        can_split=not args.no_split,
        can_surrender=args.surrender,
    )
    print(action.value)


if __name__ == "__main__":
    main()
