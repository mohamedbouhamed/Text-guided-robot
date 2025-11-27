import pygame
import numpy as np
from typing import List, Tuple

class Robot:
    """Robot virtuel qui peut naviguer dans l'environnement"""
    def __init__(self, x: int, y: int, size: int = 25):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.size = size
        self.color = (0, 150, 255)  # Bleu clair
        self.speed = 3
        self.path: List[Tuple[int, int]] = []
        self.current_path_index = 0
        self.reached_target = False
        self.total_actions = 0
        self.reasoning_steps = []

    def reset(self):
        """Réinitialise le robot à sa position de départ"""
        self.x = self.start_x
        self.y = self.start_y
        self.path = []
        self.current_path_index = 0
        self.reached_target = False
        self.total_actions = 0
        self.reasoning_steps = []

    def set_path(self, path: List[Tuple[int, int]]):
        """Définit le chemin que le robot doit suivre"""
        self.path = path
        self.current_path_index = 0
        self.reached_target = False

    def add_reasoning_step(self, step: str):
        """Ajoute une étape de raisonnement (Chain-of-Thought)"""
        self.reasoning_steps.append(step)
        print(f"💭 Raisonnement: {step}")

    def move_along_path(self):
        """Déplace le robot le long du chemin planifié"""
        if self.current_path_index >= len(self.path):
            return

        target_x, target_y = self.path[self.current_path_index]

        # Calculer la direction
        dx = target_x - self.x
        dy = target_y - self.y
        distance = np.sqrt(dx**2 + dy**2)

        if distance < self.speed:
            # Atteindre exactement le point cible
            self.x = target_x
            self.y = target_y
            self.current_path_index += 1
            self.total_actions += 1

            # Vérifier si le chemin est terminé
            if self.current_path_index >= len(self.path):
                self.reached_target = True
        else:
            # Se déplacer vers le point cible
            self.x += int(self.speed * dx / distance)
            self.y += int(self.speed * dy / distance)

    def distance_to_target(self, target_x: int, target_y: int) -> float:
        """Calcule la distance euclidienne jusqu'à la cible"""
        return np.sqrt((self.x - target_x)**2 + (self.y - target_y)**2)

    def has_reached_target(self, target_x: int, target_y: int, threshold: int = 30) -> bool:
        """Vérifie si le robot a atteint la cible"""
        return self.distance_to_target(target_x, target_y) < threshold

    def draw(self, screen: pygame.Surface):
        """Dessine le robot sur l'écran"""
        # Corps du robot (triangle pointant vers le haut)
        points = [
            (self.x, self.y - self.size // 2),  # Haut
            (self.x - self.size // 2, self.y + self.size // 2),  # Bas gauche
            (self.x + self.size // 2, self.y + self.size // 2)   # Bas droit
        ]
        pygame.draw.polygon(screen, self.color, points)
        pygame.draw.polygon(screen, (0, 0, 0), points, 2)  # Contour noir

        # Dessiner le chemin planifié (optionnel)
        if len(self.path) > 1:
            path_color = (200, 200, 255, 128)  # Bleu clair semi-transparent
            for i in range(len(self.path) - 1):
                pygame.draw.line(screen, path_color, self.path[i], self.path[i + 1], 2)

            # Marquer les waypoints
            for i, (px, py) in enumerate(self.path):
                if i < self.current_path_index:
                    # Points déjà visités (vert)
                    pygame.draw.circle(screen, (0, 255, 0), (px, py), 3)
                else:
                    # Points à venir (bleu)
                    pygame.draw.circle(screen, (0, 100, 255), (px, py), 3)

    def get_position(self) -> Tuple[int, int]:
        """Retourne la position actuelle du robot"""
        return (self.x, self.y)

    def get_grid_position(self, grid_size: int) -> Tuple[int, int]:
        """Retourne la position du robot dans la grille"""
        return (self.x // grid_size, self.y // grid_size)

    def generate_reasoning(self, instruction: str, target, environment) -> List[str]:
        """Génère des étapes de raisonnement (Chain-of-Thought) avant l'action"""
        steps = []

        # Étape 1 : Comprendre l'instruction
        steps.append(f"Je dois exécuter : '{instruction}'")

        # Étape 2 : Identifier la cible
        if target:
            steps.append(f"J'ai identifié la cible : {target.color} {target.shape} à la position ({target.x}, {target.y})")
        else:
            steps.append("❌ Je n'ai pas trouvé de cible correspondante")
            return steps

        # Étape 3 : Analyser la situation
        distance = self.distance_to_target(target.x, target.y)
        steps.append(f"Je suis à ({self.x}, {self.y}), distance jusqu'à la cible : {int(distance)} pixels")

        # Étape 4 : Planifier l'approche
        obstacles_count = len(environment.obstacles)
        if obstacles_count > 0:
            steps.append(f"Il y a {obstacles_count} obstacle(s) dans l'environnement, je vais planifier un chemin optimal avec A*")
        else:
            steps.append("L'environnement est ouvert, je peux aller directement vers la cible")

        # Étape 5 : Stratégie de navigation
        steps.append("Je vais décomposer le chemin en waypoints et me déplacer progressivement")

        return steps
