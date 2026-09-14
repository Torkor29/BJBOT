# BJBOT

Assistant local pour **Gamdom Blackjack Original**.

## État du projet

Ce dépôt contient le socle testable du bot :

- moteur de stratégie blackjack indépendant de l'interface ;
- mise fixe de 1 unité sur 1 siège ;
- arrêt à 50 % du solde initial ;
- arrêt à +1000 % de bénéfice (solde cible = 11 fois le solde initial) ;
- refus systématique de l'assurance ;
- garde de confiance pour la reconnaissance d'écran ;
- clics réels désactivés par défaut.

> Le moteur ne garantit aucun gain. La stratégie de base réduit l'avantage de la
> maison mais ne le supprime pas. Vérifiez aussi les règles et conditions de
> Gamdom avant toute automatisation.

## Pourquoi l'intégration réelle est verrouillée

La capture fournie montre l'apparence générale du jeu, pas encore une capture
authentique et complète de Gamdom Original. Cliquer à partir de coordonnées
supposées pourrait miser ou choisir une action incorrecte. Le mode réel restera
donc verrouillé jusqu'à calibration sur des captures réelles.

Aucun contournement de CAPTCHA, d'authentification ou de protection anti-bot
n'est prévu.

## Installation

Python 3.11 ou plus récent :

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev,vision]"
pytest
```

Sous Linux/macOS, l'activation est : `source .venv/bin/activate`.

## Configuration retenue

Voir `config.example.json`. Une « unité » correspond au montant saisi dans le
champ de mise du jeu.

Exemple avec un solde initial de 100 unités :

- arrêt perte : 50 unités ;
- arrêt gain : 1 100 unités ;
- mise : 1 unité par nouvelle main.

Les doubles et séparations augmentent naturellement l'exposition d'une main.

## Étapes suivantes

1. Capturer Gamdom Original aux états : mise, distribution, tirer, doubler,
   séparer, résultat.
2. Relever les règles exactes affichées dans le panneau d'aide du jeu.
3. Calibrer les zones de cartes, solde et boutons.
4. Valider au moins 500 décisions en mode observation.
5. N'activer les clics qu'après un taux de lecture mesuré conforme.
