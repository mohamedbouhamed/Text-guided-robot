# Robot Virtuel Guidé par Texte

Un robot simulé en 2D qui comprend et exécute des instructions en langage naturel.

## Fonctionnalités

- 🤖 Robot simulé dans un environnement 2D (Pygame)
- 💬 Compréhension d'instructions en langage naturel (français et anglais)
- 🤖 **Parser LLM intelligent** avec Gemini pour commandes complexes
- 🎯 **Navigation multi-cibles** avec waypoints
- 🧭 Planification de chemin avec algorithme A*
- 🎯 Navigation vers des cibles colorées (carrés et cercles)
- 🧠 Raisonnement Chain-of-Thought avant l'action
- 📊 Système d'évaluation des performances
- 🎮 Interface graphique interactive en temps réel

## Installation

### Prérequis

- Python 3.7 ou supérieur
- pip
- **macOS** : Homebrew (pour installer SDL2)

### Installation des dépendances

#### Sur macOS

Pygame nécessite SDL2. Installez-le d'abord avec Homebrew :

```bash
# Installer SDL2 et ses dépendances (y compris pkg-config)
brew install pkg-config sdl2 sdl2_image sdl2_mixer sdl2_ttf portmidi

# Ensuite installer les packages Python
pip install -r requirements.txt
```

**Méthode rapide avec le script d'installation :**

```bash
./install.sh
```

#### Sur Linux

```bash
# Ubuntu/Debian
sudo apt-get install python3-dev python3-numpy libsdl2-dev libsdl2-image-dev \
    libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev libportmidi-dev

pip install -r requirements.txt
```

#### Sur Windows

```bash
pip install -r requirements.txt
```

Les dépendances incluent :
- `pygame` : Pour la simulation graphique 2D
- `numpy` : Pour les calculs mathématiques
- `google-generativeai` : Pour le parser LLM intelligent (optionnel)

## Utilisation

### Configuration du parser LLM (optionnel)

Pour activer le parser LLM intelligent avec Gemini :

1. Obtenez une clé API gratuite sur [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Configurez la clé API :

```bash
# Méthode 1 : Créer un fichier .env (recommandé)
cp .env.example .env
# Éditez .env et ajoutez votre clé API

# Méthode 2 : Variable d'environnement
export GEMINI_API_KEY='votre_clé_ici'
```

Le programme détectera automatiquement la clé et activera le parser LLM !

**Sans clé API**, le programme utilisera le parser simple (commandes basiques uniquement).

### Mode interactif

Lancez le programme principal :

**Méthode recommandée (détecte automatiquement le bon Python) :**
```bash
./run.sh
```

**Ou directement :**
```bash
python3 main.py
```

Le programme vous demande de choisir un environnement :
1. **Simple** : Environnement avec quelques obstacles
2. **Labyrinthe** : Environnement complexe avec de nombreux obstacles
3. **Ouvert** : Environnement spacieux avec plusieurs cibles

Ensuite, entrez des commandes textuelles pour guider le robot !

### Exemples de commandes

#### Avec parser simple (sans clé API)

Le robot comprend des commandes basiques en français et en anglais :

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

#### Avec parser LLM (avec clé API Gemini)

Le parser LLM comprend des commandes beaucoup plus complexes :

**Commandes multi-cibles avec waypoints :**
- "Va au carré rouge en passant par le cercle bleu"
- "Rejoins le cercle vert puis le carré jaune"
- "Passe d'abord par le cercle bleu, puis va au carré rouge, et finis au cercle vert"
- "Atteins le bleu" (plus naturel, sans structure rigide)

Le LLM distingue automatiquement les **waypoints** (points de passage) des **cibles finales** !

**Commandes spéciales :**
- `reset` : Réinitialise la position du robot
- `quit` : Quitte le programme
- `test` : Lance le mode test automatique

### Mode test automatique

Pour exécuter les scénarios de test automatiques :

**Méthode recommandée :**
```bash
./run_tests.sh
```

**Ou directement :**
```bash
python3 tests/test_scenarios.py
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
├── .env.example          # Template pour configuration API
├── main.py               # Point d'entrée principal
├── run.sh                # Script de lancement intelligent
├── install.sh            # Script d'installation (macOS)
├── src/                  # Code source
│   ├── __init__.py       # Package Python
│   ├── environment.py    # Environnement de simulation 2D
│   ├── robot.py          # Classe Robot avec mouvement
│   ├── nlp_parser.py     # Parser simple (règles)
│   ├── llm_parser.py     # Parser LLM (Gemini)
│   ├── pathfinding.py    # Algorithme A* pour planification
│   └── evaluator.py      # Système d'évaluation
├── tests/                # Tests
│   └── test_scenarios.py # Scénarios de test automatiques
└── test_llm.py           # Test du parser LLM
```

## Flux d'exécution

1. **Parsing de commande** : L'utilisateur saisit une commande textuelle
2. **Analyse intelligente** :
   - Avec LLM : Gemini analyse et extrait les cibles multiples avec waypoints
   - Sans LLM : Parser simple extrait une seule cible (couleur + forme)
3. **Planification multi-cibles** : Si plusieurs cibles, création d'un plan séquentiel
4. **Raisonnement** : Le robot génère des étapes de raisonnement (Chain-of-Thought)
5. **Identification de cible** : L'environnement trouve les objets correspondants
6. **Planification** : L'algorithme A* calcule le chemin optimal
7. **Navigation** : Le robot suit le chemin waypoint par waypoint
8. **Transition** : Passage automatique à la cible suivante si waypoints
9. **Évaluation** : Le système mesure le succès et les performances

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

Parser simple basé sur des règles :
- Extraction de couleur, forme, action
- Support français et anglais
- Système de confiance
- Validation de commandes
- Une seule cible par commande

### LLM Parser (llm_parser.py)

Parser intelligent utilisant Gemini :
- Compréhension avancée du langage naturel
- Support multi-cibles avec waypoints
- Distinction automatique waypoints/cibles finales
- Fallback automatique vers parser simple en cas d'erreur
- Format de sortie structuré avec confiance

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
- ✅ ~~Support de plusieurs cibles dans une commande~~ (Implémenté avec LLM parser)
- ✅ ~~Utilisation de modèles LLM pour parsing avancé~~ (Implémenté avec Gemini)
- Objets mobiles dans l'environnement
- Commandes conditionnelles ("si le chemin est bloqué, va au vert")
- Mode multijoueur avec plusieurs robots
- Enregistrement vidéo des simulations
- Interface web avec WebSocket
- Fine-tuning du LLM pour commandes spécialisées

## Auteur

Projet créé dans le cadre d'une démonstration de Vision-Language-Action miniature.

## Licence

Ce projet est open source et disponible pour usage éducatif.
