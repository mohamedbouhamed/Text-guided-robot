# Robot Virtuel Guidé par Texte

Un robot simulé en 2D qui comprend et exécute des instructions en langage naturel.

## Fonctionnalités

- 🤖 Robot simulé dans un environnement 2D (Pygame)
- 💬 Compréhension d'instructions en langage naturel (français et anglais)
- 🧭 Planification de chemin avec algorithme A*
- 🎯 Navigation vers des cibles colorées (carrés et cercles)
- 🧠 Raisonnement Chain-of-Thought avant l'action
- 📊 Système d'évaluation des performances
- 🎮 Interface graphique interactive en temps réel

## Installation

### Prérequis

- Python 3.7 ou supérieur
- pip

### Installation des dépendances

```bash
pip install -r requirements.txt
```

Les dépendances incluent :
- `pygame` : Pour la simulation graphique 2D
- `numpy` : Pour les calculs mathématiques

## Utilisation

### Mode interactif

Lancez le programme principal :

```bash
python main.py
```

Le programme vous demande de choisir un environnement :
1. **Simple** : Environnement avec quelques obstacles
2. **Labyrinthe** : Environnement complexe avec de nombreux obstacles
3. **Ouvert** : Environnement spacieux avec plusieurs cibles

Ensuite, entrez des commandes textuelles pour guider le robot !

### Exemples de commandes

Le robot comprend des commandes en français et en anglais :

**Français :**
- "Va vers le carré rouge"
- "Déplace-toi vers le cercle bleu"
- "Atteins l'objet vert"
- "Va au cercle jaune"
- "Rejoins le carré vert"

**Anglais :**
- "Go to the red square"
- "Move to the blue circle"
- "Reach the green object"

**Commandes spéciales :**
- `reset` : Réinitialise la position du robot
- `quit` : Quitte le programme
- `test` : Lance le mode test automatique

### Mode test automatique

Pour exécuter les scénarios de test automatiques :

```bash
python tests/test_scenarios.py
```

Ce script :
- Teste 3 environnements différents
- Exécute plusieurs commandes par environnement
- Génère des statistiques de performance
- Exporte les résultats dans des fichiers texte

## Architecture du projet

```
Text-guided-robot/
├── README.md              # Documentation
├── requirements.txt       # Dépendances Python
├── .gitignore            # Fichiers à ignorer par Git
├── main.py               # Point d'entrée principal
├── src/                  # Code source
│   ├── __init__.py       # Package Python
│   ├── environment.py    # Environnement de simulation 2D
│   ├── robot.py          # Classe Robot avec mouvement
│   ├── nlp_parser.py     # Parsing des commandes textuelles
│   ├── pathfinding.py    # Algorithme A* pour planification
│   └── evaluator.py      # Système d'évaluation
└── tests/                # Tests
    └── test_scenarios.py # Scénarios de test automatiques
```

## Flux d'exécution

1. **Parsing de commande** : L'utilisateur saisit une commande textuelle
2. **Analyse NLP** : Le parser extrait l'action, la couleur et la forme
3. **Raisonnement** : Le robot génère des étapes de raisonnement (Chain-of-Thought)
4. **Identification de cible** : L'environnement trouve l'objet correspondant
5. **Planification** : L'algorithme A* calcule le chemin optimal
6. **Navigation** : Le robot suit le chemin waypoint par waypoint
7. **Évaluation** : Le système mesure le succès et les performances

## Composants détaillés

### Environment (environment.py)

Gère l'environnement de simulation :
- Création d'objets cibles (GameObject) avec couleurs et formes
- Placement d'obstacles (Obstacle)
- Système de grille pour la planification de chemin
- Rendu graphique avec Pygame
- 3 environnements prédéfinis

### Robot (robot.py)

Représente le robot virtuel :
- Position et déplacement
- Suivi de chemin (path following)
- Génération de raisonnement Chain-of-Thought
- Métriques de performance (actions, distance)
- Rendu visuel (triangle avec chemin)

### NLP Parser (nlp_parser.py)

Parse les commandes textuelles :
- Extraction de couleur, forme, action
- Support français et anglais
- Système de confiance
- Validation de commandes

### PathFinder (pathfinding.py)

Planification de chemin avec A* :
- Algorithme A* complet
- Heuristique euclidienne
- Mouvement 8-directionnel
- Évitement d'obstacles
- Simplification de chemin

### Evaluator (evaluator.py)

Système d'évaluation :
- Suivi des tests
- Calcul de métriques (taux de réussite, actions moyennes, temps)
- Génération de rapports
- Export de résultats

## Évaluation et métriques

Le système évalue automatiquement :

- **Taux de réussite** : Pourcentage de cibles atteintes avec succès
- **Nombre d'actions** : Actions nécessaires pour atteindre la cible
- **Temps d'exécution** : Durée totale de l'exécution
- **Longueur du chemin** : Nombre de waypoints dans le chemin
- **Étapes de raisonnement** : Chain-of-Thought généré par le robot

Les résultats peuvent être exportés dans des fichiers texte pour analyse ultérieure.

## Exemples d'utilisation

### Session interactive typique

```
$ python main.py

Choisissez un environnement :
1. Simple (quelques obstacles)
2. Labyrinthe (complexe)
3. Ouvert (plusieurs cibles)

Votre choix (1-3) : 1

Commande > Va vers le carré rouge

📝 Analyse de la commande: 'Va vers le carré rouge'
  - Action: move
  - Couleur: rouge
  - Forme: square
  - Confiance: 100%

💭 Raisonnement: Je dois exécuter : 'Va vers le carré rouge'
💭 Raisonnement: J'ai identifié la cible : rouge square à la position (650, 100)
💭 Raisonnement: Je suis à (100, 100), distance jusqu'à la cible : 550 pixels
💭 Raisonnement: Il y a 2 obstacle(s), je vais planifier un chemin optimal avec A*

Planification du chemin avec A*...
Chemin trouvé avec 15 waypoints !

[Animation du robot se déplaçant vers la cible]

Cible atteinte avec succès !
```

## Extensions possibles

- Ajouter plus de formes (triangles, pentagones)
- Support de plusieurs cibles dans une commande
- Objets mobiles dans l'environnement
- Commandes plus complexes (conditions, séquences)
- Mode multijoueur avec plusieurs robots
- Enregistrement vidéo des simulations
- Interface web avec WebSocket
- Utilisation de modèles LLM pour parsing avancé

## Auteur

Projet créé dans le cadre d'une démonstration de Vision-Language-Action miniature.

## Licence

Ce projet est open source et disponible pour usage éducatif.
