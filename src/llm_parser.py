"""
Parser NLP intelligent utilisant Gemini
Comprend des commandes complexes avec plusieurs cibles et waypoints
"""

import os
import json
import google.generativeai as genai
from typing import Dict, List, Optional


class LLMParser:
    """Parser intelligent utilisant l'API Gemini de Google"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialise le parser LLM

        Args:
            api_key: Clé API Gemini (ou via variable d'environnement GEMINI_API_KEY)
        """
        # Récupérer la clé API
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')

        if not self.api_key:
            raise ValueError(
                "Clé API Gemini requise. "
                "Définissez la variable d'environnement GEMINI_API_KEY "
                "ou passez api_key au constructeur."
            )

        # Configurer Gemini
        genai.configure(api_key=self.api_key)
        # Utiliser le modèle Gemini 2.5 Flash (rapide et gratuit)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

        # Prompt système pour guider Gemini
        self.system_prompt = """Tu es un assistant qui convertit des commandes en langage naturel en instructions structurées pour un robot.

Le robot peut naviguer vers des objets dans un environnement 2D.

Couleurs disponibles: rouge, bleu, vert, jaune, orange, violet
Formes disponibles: carré (square), cercle (circle)

Tu dois extraire de la commande:
1. Les cibles (objets à atteindre) - peut être plusieurs
2. Les waypoints (points de passage) - optionnel
3. La séquence d'actions

Réponds UNIQUEMENT avec un JSON valide dans ce format:
{
    "targets": [
        {"color": "rouge", "shape": "square", "type": "target"},
        {"color": "bleu", "shape": "circle", "type": "waypoint"}
    ],
    "confidence": 0.95,
    "interpretation": "Aller au carré rouge en passant par le cercle bleu"
}

Si la commande n'est pas claire, mets confidence < 0.5.
"""

    def parse_command(self, command: str) -> Dict:
        """
        Parse une commande avec Gemini

        Args:
            command: Commande en langage naturel

        Returns:
            Dict avec targets, confidence, interpretation
        """
        try:
            # Créer le prompt complet
            prompt = f"{self.system_prompt}\n\nCommande: {command}\n\nRéponds uniquement avec le JSON:"

            # Appeler Gemini
            response = self.model.generate_content(prompt)

            # Extraire le JSON de la réponse
            response_text = response.text.strip()

            # Nettoyer la réponse (enlever les balises markdown si présentes)
            if response_text.startswith('```'):
                # Extraire le contenu entre ```json et ```
                lines = response_text.split('\n')
                json_lines = []
                in_json = False
                for line in lines:
                    if line.strip().startswith('```'):
                        in_json = not in_json
                        continue
                    if in_json:
                        json_lines.append(line)
                response_text = '\n'.join(json_lines)

            # Parser le JSON
            result = json.loads(response_text)

            # Valider le résultat
            if 'targets' not in result:
                return self._fallback_parse(command)

            # Ajouter la commande brute
            result['raw_command'] = command

            return result

        except Exception as e:
            print(f"Erreur LLM: {e}")
            # Fallback sur le parser simple
            return self._fallback_parse(command)

    def _fallback_parse(self, command: str) -> Dict:
        """Parser simple en cas d'échec du LLM"""
        from src.nlp_parser import NLPParser

        simple_parser = NLPParser()
        simple_result = simple_parser.parse_command(command)

        # Convertir au format LLM
        targets = []
        if simple_result['color'] or simple_result['shape']:
            targets.append({
                'color': simple_result['color'],
                'shape': simple_result['shape'],
                'type': 'target'
            })

        return {
            'targets': targets,
            'confidence': simple_result['confidence'],
            'interpretation': command,
            'raw_command': command,
            'fallback': True
        }

    def explain_parsing(self, command: str) -> str:
        """Explique comment une commande a été parsée"""
        parsed = self.parse_command(command)

        explanation = f"\n📝 Analyse de la commande (LLM): '{command}'\n"
        explanation += f"  - Interprétation: {parsed.get('interpretation', 'N/A')}\n"
        explanation += f"  - Confiance: {parsed.get('confidence', 0)*100:.0f}%\n"

        if parsed.get('fallback'):
            explanation += "  - Mode: Fallback (parser simple)\n"
        else:
            explanation += "  - Mode: LLM (Gemini)\n"

        explanation += f"  - Nombre de cibles: {len(parsed.get('targets', []))}\n"

        for i, target in enumerate(parsed.get('targets', []), 1):
            target_type = target.get('type', 'target')
            color = target.get('color', 'N/A')
            shape = target.get('shape', 'N/A')
            explanation += f"    {i}. [{target_type}] {color} {shape}\n"

        return explanation
