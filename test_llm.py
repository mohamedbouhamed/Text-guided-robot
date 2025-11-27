#!/usr/bin/env python3
"""
Test du parser LLM avec Gemini
"""

import os
from src.llm_parser import LLMParser


def main():
    print("="*60)
    print("TEST DU PARSER LLM (GEMINI)")
    print("="*60)

    # Vérifier la clé API
    api_key = os.getenv('GEMINI_API_KEY')

    if not api_key:
        print("\n❌ Clé API Gemini non trouvée !")
        print("\nPour configurer:")
        print("1. Obtenir une clé API sur: https://makersuite.google.com/app/apikey")
        print("2. Définir la variable d'environnement:")
        print("   export GEMINI_API_KEY='votre_clé_ici'")
        print("\nOu créer un fichier .env:")
        print("   cp .env.example .env")
        print("   # Éditer .env et ajouter votre clé")
        return

    print(f"\n✅ Clé API trouvée: {api_key[:10]}...")

    # Initialiser le parser
    try:
        parser = LLMParser(api_key=api_key)
        print("✅ Parser LLM initialisé\n")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return

    # Commandes de test
    test_commands = [
        # Commandes simples
        "Va vers le carré rouge",
        "Atteins le cercle bleu",

        # Commandes complexes avec waypoints
        "Va au carré rouge en passant par le cercle bleu",
        "Rejoins le cercle vert puis le carré jaune",

        # Commandes très complexes
        "Passe d'abord par le cercle bleu, puis va au carré rouge, et finis au cercle vert",

        # Commandes ambiguës
        "Va là-bas",
        "Bouge un peu",
    ]

    print("-"*60)
    print("TESTS DES COMMANDES")
    print("-"*60)

    for i, command in enumerate(test_commands, 1):
        print(f"\n[Test {i}/{len(test_commands)}]")
        print(parser.explain_parsing(command))

        # Afficher le résultat brut
        result = parser.parse_command(command)
        print(f"  - Résultat brut:")
        print(f"    Targets: {len(result.get('targets', []))}")

        if result.get('fallback'):
            print(f"    ⚠️  Mode fallback utilisé")

        print()

    print("="*60)
    print("Tests terminés !")
    print("="*60)


if __name__ == "__main__":
    main()
