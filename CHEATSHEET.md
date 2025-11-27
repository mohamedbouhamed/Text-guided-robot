# Aide-Mémoire - Robot Virtuel

## 🚀 Commandes Rapides

```bash
# Lancer le programme
./run.sh

# Lancer les tests
./run_tests.sh

# Installer les dépendances
./install.sh
```

## 💬 Exemples de Commandes Robot

### Français
```
Va vers le carré rouge
Déplace-toi vers le cercle bleu
Atteins l'objet vert
Va au cercle jaune
Rejoins le carré vert
```

### Anglais
```
Go to the red square
Move to the blue circle
Reach the green object
```

### Commandes Spéciales
```
reset  - Réinitialiser le robot
quit   - Quitter le programme
test   - Mode test automatique
```

## 🎨 Couleurs Disponibles

| Français | English | RGB         |
|----------|---------|-------------|
| rouge    | red     | 255, 0, 0   |
| bleu     | blue    | 0, 0, 255   |
| vert     | green   | 0, 255, 0   |
| jaune    | yellow  | 255, 255, 0 |
| orange   | orange  | 255, 165, 0 |
| violet   | purple  | 128, 0, 128 |

## 🔷 Formes Disponibles

| Français | English | Visuel  |
|----------|---------|---------|
| carré    | square  | ▢       |
| cercle   | circle  | ○       |

## 🗺️ Environnements

| ID | Nom        | Objets | Obstacles | Difficulté |
|----|------------|--------|-----------|------------|
| 1  | Simple     | 3      | 2         | ⭐         |
| 2  | Labyrinthe | 2      | 7         | ⭐⭐⭐     |
| 3  | Ouvert     | 4      | 1         | ⭐⭐       |

## 📊 Métriques Évaluées

- **Taux de réussite** : % de cibles atteintes
- **Actions moyennes** : Nombre de déplacements
- **Temps d'exécution** : Durée totale
- **Longueur du chemin** : Nombre de waypoints

## 🔧 Dépannage Express

### Le programme ne démarre pas
```bash
# Vérifier pygame
python3 -c "import pygame; print('OK')"

# Réinstaller si nécessaire
pip install pygame
```

### Mauvaise version de Python
```bash
# Utiliser le script automatique
./run.sh
```

### Erreur SDL2 sur macOS
```bash
# Installer SDL2
brew install pkg-config sdl2 sdl2_image sdl2_mixer sdl2_ttf portmidi
```

## 📂 Structure des Fichiers

```
main.py           - Programme principal
run.sh            - Lanceur automatique
src/
  environment.py  - Environnement 2D
  robot.py        - Robot avec IA
  nlp_parser.py   - Parser de texte
  pathfinding.py  - Algorithme A*
  evaluator.py    - Évaluation
tests/
  test_scenarios.py - Tests auto
```

## 🎯 Workflow Typique

1. Lancer : `./run.sh`
2. Choisir environnement : `1`
3. Commande : `Va vers le carré rouge`
4. Observer l'animation
5. Commande : `reset` (pour recommencer)
6. Commande : `quit` (pour quitter)

## 📝 Commandes Git Utiles

```bash
# Voir l'historique
git log --oneline --graph

# Voir les modifications
git status
git diff

# Créer une branche
git checkout -b ma-nouvelle-fonctionnalite
```

## 🔍 Debug

```python
# Tester l'import des modules
python3 -c "import pygame; import numpy; print('Modules OK')"

# Vérifier la version
python3 --version

# Lister les packages
pip list | grep -E 'pygame|numpy'
```

## 📦 Installation Manuelle

```bash
# macOS
brew install pkg-config sdl2 sdl2_image sdl2_mixer sdl2_ttf portmidi
pip install pygame numpy

# Linux (Ubuntu/Debian)
sudo apt-get install python3-dev libsdl2-dev
pip install pygame numpy

# Windows
pip install pygame numpy
```

## 🎓 Concepts Clés

- **NLP** : Analyse de langage naturel
- **A\*** : Algorithme de recherche de chemin optimal
- **Chain-of-Thought** : Raisonnement étape par étape
- **Waypoint** : Point intermédiaire sur le chemin
- **Grid** : Grille pour la navigation

## ⚡ Raccourcis

| Action               | Commande          |
|----------------------|-------------------|
| Lancer               | `./run.sh`        |
| Tester               | `./run_tests.sh`  |
| Installer            | `./install.sh`    |
| Voir les docs        | `cat README.md`   |
| Guide rapide         | `cat QUICKSTART.md` |
| État du projet       | `cat STATUS.md`   |

---

**Astuce** : Garde ce fichier ouvert dans un onglet pour référence rapide ! 📌
