import re
from typing import Dict, Tuple, Optional

class NLPParser:
    """Parse les commandes en langage naturel pour extraire les intentions"""

    def __init__(self):
        # Dictionnaires de mots-clés
        self.color_keywords = {
            'rouge': 'rouge',
            'red': 'rouge',
            'bleu': 'bleu',
            'blue': 'bleu',
            'vert': 'vert',
            'green': 'vert',
            'jaune': 'jaune',
            'yellow': 'jaune',
            'orange': 'orange',
            'violet': 'violet',
            'purple': 'violet',
        }

        self.shape_keywords = {
            'carré': 'square',
            'carre': 'square',
            'square': 'square',
            'cercle': 'circle',
            'circle': 'circle',
        }

        self.action_keywords = {
            'va': 'move',
            'aller': 'move',
            'go': 'move',
            'déplace': 'move',
            'deplace': 'move',
            'move': 'move',
            'atteins': 'reach',
            'atteindre': 'reach',
            'reach': 'reach',
            'rejoins': 'reach',
            'vers': 'to',
            'to': 'to',
            'au': 'to',
            'à': 'to',
            'a': 'to',
        }

        self.object_keywords = ['objet', 'object', 'cible', 'target']

    def parse_command(self, command: str) -> Dict:
        """
        Parse une commande textuelle et extrait l'intention

        Args:
            command: Commande en langage naturel

        Returns:
            Dict avec 'action', 'color', 'shape', 'raw_command'
        """
        command = command.lower().strip()

        result = {
            'action': None,
            'color': None,
            'shape': None,
            'raw_command': command,
            'confidence': 0.0
        }

        # Extraire l'action
        for keyword, action in self.action_keywords.items():
            if keyword in command:
                if result['action'] is None or action in ['move', 'reach']:
                    result['action'] = action

        # Si aucune action trouvée, assumer "move"
        if result['action'] is None:
            result['action'] = 'move'

        # Extraire la couleur
        for keyword, color in self.color_keywords.items():
            if keyword in command:
                result['color'] = color
                break

        # Extraire la forme
        for keyword, shape in self.shape_keywords.items():
            if keyword in command:
                result['shape'] = shape
                break

        # Calculer la confiance
        confidence = 0.0
        if result['color']:
            confidence += 0.5
        if result['shape']:
            confidence += 0.3
        if result['action']:
            confidence += 0.2

        result['confidence'] = confidence

        return result

    def extract_target_description(self, command: str) -> str:
        """Extrait une description lisible de la cible"""
        parsed = self.parse_command(command)

        parts = []
        if parsed['color']:
            parts.append(parsed['color'])
        if parsed['shape']:
            parts.append(parsed['shape'])

        if parts:
            return ' '.join(parts)
        return "cible inconnue"

    def is_valid_command(self, command: str) -> bool:
        """Vérifie si une commande est valide (contient au moins une couleur ou une forme)"""
        parsed = self.parse_command(command)
        return parsed['color'] is not None or parsed['shape'] is not None

    def get_alternative_commands(self) -> list:
        """Retourne des exemples de commandes valides"""
        return [
            "Va vers le carré rouge",
            "Déplace-toi vers le cercle bleu",
            "Atteins l'objet vert",
            "Va au cercle jaune",
            "Rejoins le carré vert",
            "Va vers le rouge",
            "Atteins le cercle",
        ]

    def explain_parsing(self, command: str) -> str:
        """Explique comment une commande a été parsée (pour debug)"""
        parsed = self.parse_command(command)

        explanation = f"\n📝 Analyse de la commande: '{command}'\n"
        explanation += f"  - Action: {parsed['action'] or 'Non détectée'}\n"
        explanation += f"  - Couleur: {parsed['color'] or 'Non détectée'}\n"
        explanation += f"  - Forme: {parsed['shape'] or 'Non détectée'}\n"
        explanation += f"  - Confiance: {parsed['confidence']*100:.0f}%\n"

        return explanation
