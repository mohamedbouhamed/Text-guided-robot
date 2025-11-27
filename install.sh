#!/bin/bash
# Script d'installation pour le Robot Virtuel Guidé par Texte

echo "==================================================="
echo "Installation du Robot Virtuel Guidé par Texte"
echo "==================================================="
echo ""

# Détecter le système d'exploitation
OS="$(uname -s)"

case "${OS}" in
    Darwin*)
        echo "Système détecté: macOS"
        echo ""
        echo "Étape 1/2: Installation de SDL2 via Homebrew..."

        # Vérifier si Homebrew est installé
        if ! command -v brew &> /dev/null; then
            echo "❌ Homebrew n'est pas installé !"
            echo "Installez Homebrew depuis: https://brew.sh"
            exit 1
        fi

        echo "Installation des dépendances SDL2 et pkg-config..."
        brew install pkg-config sdl2 sdl2_image sdl2_mixer sdl2_ttf portmidi

        if [ $? -eq 0 ]; then
            echo "✅ SDL2 installé avec succès"
        else
            echo "❌ Erreur lors de l'installation de SDL2"
            exit 1
        fi
        ;;

    Linux*)
        echo "Système détecté: Linux"
        echo ""
        echo "Étape 1/2: Installation des dépendances système..."

        # Détecter la distribution
        if [ -f /etc/debian_version ]; then
            echo "Distribution: Debian/Ubuntu"
            sudo apt-get update
            sudo apt-get install -y python3-dev python3-numpy libsdl2-dev \
                libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
                libfreetype6-dev libportmidi-dev
        elif [ -f /etc/redhat-release ]; then
            echo "Distribution: RedHat/Fedora"
            sudo dnf install -y python3-devel numpy SDL2-devel SDL2_image-devel \
                SDL2_mixer-devel SDL2_ttf-devel portmidi-devel
        else
            echo "⚠️  Distribution non reconnue, tentative d'installation de pygame seulement"
        fi
        ;;

    MINGW*|MSYS*|CYGWIN*)
        echo "Système détecté: Windows"
        echo ""
        echo "Les dépendances SDL2 sont incluses dans les wheels pygame pour Windows"
        ;;

    *)
        echo "⚠️  Système non reconnu: ${OS}"
        echo "Tentative d'installation de pygame..."
        ;;
esac

echo ""
echo "Étape 2/2: Installation des packages Python..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "==================================================="
    echo "✅ Installation terminée avec succès !"
    echo "==================================================="
    echo ""
    echo "Pour lancer le programme :"
    echo "  python main.py"
    echo ""
    echo "Pour lancer les tests :"
    echo "  python tests/test_scenarios.py"
    echo ""
else
    echo ""
    echo "❌ Erreur lors de l'installation des packages Python"
    exit 1
fi
