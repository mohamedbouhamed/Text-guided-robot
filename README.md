# Robot Virtuel Guidé par Texte

Un robot simulé en 2D qui comprend et exécute des instructions en langage naturel.

## Fonctionnalités

- 🤖 Robot simulé dans un environnement 2D (Pygame)
- 💬 Compréhension d'instructions en langage naturel
- 🧭 Planification de chemin avec algorithme A*
- 🎯 Navigation vers des cibles colorées
- 📊 Système d'évaluation des performances

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

```bash
python main.py
```

### Exemples de commandes

- "Va vers le carré rouge"
- "Déplace-toi vers le cercle bleu"
- "Atteins l'objet vert"

## Structure du projet

```
.
├── main.py                 # Point d'entrée principal
├── requirements.txt        # Dépendances
├── src/
│   ├── environment.py      # Environnement de simulation 2D
│   ├── robot.py            # Classe Robot
│   ├── nlp_parser.py       # Parsing des commandes textuelles
│   ├── pathfinding.py      # Algorithme A*
│   └── evaluator.py        # Système d'évaluation
└── tests/
    └── test_scenarios.py   # Scénarios de test
```

## Évaluation

Le système évalue :
- Taux de réussite (% d'atteinte de la cible)
- Nombre d'actions nécessaires
- Temps d'exécution
