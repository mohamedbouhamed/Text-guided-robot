#!/bin/bash
# Script de vérification que le LLM est bien activé

echo "============================================================"
echo "VÉRIFICATION DE L'ACTIVATION DU LLM"
echo "============================================================"
echo ""

# Charger .env comme le fait run.sh
if [ -f .env ]; then
    echo "✓ Fichier .env trouvé"
    set -a
    source .env
    set +a
else
    echo "✗ Fichier .env non trouvé"
    exit 1
fi

# Vérifier la clé API
if [ -z "$GEMINI_API_KEY" ]; then
    echo "✗ GEMINI_API_KEY non définie"
    exit 1
else
    echo "✓ GEMINI_API_KEY définie: ${GEMINI_API_KEY:0:20}..."
fi

# Tester que Python voit la variable
echo ""
echo "Test Python:"
python3 -c "
import os
from src.llm_parser import LLMParser

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print('✗ Python ne voit pas GEMINI_API_KEY')
    exit(1)

print(f'✓ Python voit GEMINI_API_KEY: {api_key[:20]}...')

try:
    parser = LLMParser()
    print('✓ LLMParser initialisé')

    result = parser.parse_command('Va au carré rouge en passant par le cercle bleu')
    targets = result.get('targets', [])
    print(f'✓ Test de parsing: {len(targets)} cibles détectées')

    if len(targets) == 2:
        print('✓ Multi-cibles fonctionne !')
        print('')
        print('✅ LE LLM EST BIEN ACTIVÉ ET FONCTIONNEL !')
    else:
        print(f'✗ Attendu 2 cibles, obtenu {len(targets)}')
except Exception as e:
    print(f'✗ Erreur: {e}')
    exit(1)
"

echo ""
echo "============================================================"
echo "Vous pouvez maintenant lancer: ./run.sh"
echo "Le parser LLM sera automatiquement activé !"
echo "============================================================"
