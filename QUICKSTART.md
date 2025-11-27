# Guide de Démarrage Rapide

## Installation (déjà effectuée !)

Les dépendances sont déjà installées sur ce système :
- ✅ SDL2 et ses bibliothèques
- ✅ pkg-config
- ✅ pygame 2.6.1
- ✅ numpy 2.3.5

## Lancer le programme

### Mode interactif

```bash
python main.py
```

Ensuite :
1. Choisissez un environnement (1, 2, ou 3)
2. Entrez des commandes textuelles comme :
   - "Va vers le carré rouge"
   - "Atteins le cercle bleu"
   - "Va vers le vert"

### Mode test automatique

Pour lancer les tests automatiques sur tous les environnements :

```bash
python tests/test_scenarios.py
```

## Exemples de commandes

### Français
- "Va vers le carré rouge"
- "Déplace-toi vers le cercle bleu"
- "Atteins l'objet vert"
- "Va au cercle jaune"
- "Rejoins le carré vert"

### Anglais
- "Go to the red square"
- "Move to the blue circle"
- "Reach the green object"

### Commandes spéciales
- `reset` : Réinitialise la position du robot
- `quit` : Quitte le programme
- `test` : Lance le mode test automatique

## Structure du projet

```
Text-guided-robot/
├── main.py               # Programme principal
├── install.sh            # Script d'installation
├── requirements.txt      # Dépendances
├── README.md            # Documentation complète
├── QUICKSTART.md        # Ce fichier
├── src/                 # Code source
│   ├── environment.py   # Environnement 2D
│   ├── robot.py         # Robot avec IA
│   ├── nlp_parser.py    # Parser de commandes
│   ├── pathfinding.py   # Algorithme A*
│   └── evaluator.py     # Évaluation
└── tests/
    └── test_scenarios.py # Tests automatiques
```

## Fonctionnement

1. **Tu entres une commande** : "Va vers le carré rouge"
2. **Le parser NLP analyse** : couleur=rouge, forme=carré, action=move
3. **Le robot raisonne** : Génère des étapes de raisonnement (Chain-of-Thought)
4. **L'algorithme A* planifie** : Calcule le meilleur chemin
5. **Le robot navigue** : Suit le chemin en évitant les obstacles
6. **Le système évalue** : Mesure le succès et les performances

## Environnements disponibles

### 1. Simple
- 3 objets cibles
- 2 obstacles
- Idéal pour débuter

### 2. Labyrinthe
- 2 objets cibles
- Nombreux obstacles formant un labyrinthe
- Teste l'algorithme A*

### 3. Ouvert
- 4 objets cibles
- 1 obstacle central
- Environnement spacieux

## Résultats

Après chaque session, tu peux :
- Voir les statistiques dans la console
- Exporter les résultats dans un fichier texte

## Commits Git

Le projet a été créé avec 11 commits structurés :
1. Structure de base
2. Environnement 2D
3. Classe Robot
4. Parser NLP
5. Algorithme A*
6. Système d'évaluation
7. Programme principal
8. Tests automatiques
9. .gitignore
10. Documentation README
11. Script d'installation et fixes macOS

## Prochaines étapes

Tu peux maintenant :
1. ✅ Tester le programme : `python main.py`
2. ✅ Lancer les tests : `python tests/test_scenarios.py`
3. Modifier les environnements dans `src/environment.py`
4. Ajouter de nouvelles couleurs/formes
5. Améliorer le parser NLP
6. Ajouter des fonctionnalités (voir Extensions dans README.md)

Amuse-toi bien avec ton robot ! 🤖
