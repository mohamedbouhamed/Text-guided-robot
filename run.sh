#!/bin/bash
# Script de lancement pour le Robot Virtuel

# Chercher le bon Python avec pygame installé
PYTHON=""

# Liste des Python à essayer
PYTHONS=(
    "python3"
    "/opt/homebrew/bin/python3.11"
    "/opt/homebrew/bin/python3"
    "/usr/bin/python3"
    "python"
)

echo "Recherche d'un Python avec pygame installé..."

for py in "${PYTHONS[@]}"; do
    if command -v "$py" &> /dev/null; then
        if "$py" -c "import pygame" 2>/dev/null; then
            PYTHON="$py"
            echo "✅ Trouvé: $py"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo "❌ Aucun Python avec pygame n'a été trouvé !"
    echo "Installez pygame avec: pip install pygame"
    exit 1
fi

echo ""
echo "Lancement du robot virtuel..."
echo "Python utilisé: $PYTHON ($($PYTHON --version))"
echo ""

"$PYTHON" main.py "$@"
