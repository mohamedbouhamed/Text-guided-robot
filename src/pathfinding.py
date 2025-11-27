import heapq
import numpy as np
from typing import List, Tuple, Optional

class Node:
    """Représente un nœud dans l'algorithme A*"""
    def __init__(self, position: Tuple[int, int], parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  # Coût depuis le début
        self.h = 0  # Heuristique (estimation jusqu'à la fin)
        self.f = 0  # Coût total (g + h)

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

    def __hash__(self):
        return hash(self.position)


class PathFinder:
    """Implémente l'algorithme A* pour la planification de chemin"""

    def __init__(self, environment):
        self.environment = environment

    def heuristic(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """Calcule la distance euclidienne entre deux positions"""
        return np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    def get_neighbors(self, position: Tuple[int, int], grid_size: int) -> List[Tuple[int, int]]:
        """Retourne les voisins valides d'une position (8 directions)"""
        x, y = position
        neighbors = []

        # 8 directions : haut, bas, gauche, droite, et diagonales
        directions = [
            (0, -1), (0, 1), (-1, 0), (1, 0),  # Cardinaux
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonales
        ]

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy

            # Vérifier si dans les limites de la grille
            if (0 <= new_x < self.environment.grid_width and
                0 <= new_y < self.environment.grid_height):

                # Convertir en coordonnées pixel
                pixel_x, pixel_y = self.environment.grid_to_pixel(new_x, new_y)

                # Vérifier si la position est valide (pas d'obstacle)
                if self.environment.is_position_valid(pixel_x, pixel_y):
                    neighbors.append((new_x, new_y))

        return neighbors

    def a_star(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        Algorithme A* pour trouver le chemin optimal

        Args:
            start: Position de départ (x, y) en pixels
            goal: Position d'arrivée (x, y) en pixels

        Returns:
            Liste de positions (en pixels) formant le chemin, ou None si pas de chemin
        """
        # Convertir les positions pixel en grille
        start_grid = self.environment.pixel_to_grid(start[0], start[1])
        goal_grid = self.environment.pixel_to_grid(goal[0], goal[1])

        # Initialiser les nœuds
        start_node = Node(start_grid)
        goal_node = Node(goal_grid)

        # Listes ouvertes et fermées
        open_list = []
        closed_set = set()

        heapq.heappush(open_list, start_node)

        # Compteur d'itérations (pour éviter les boucles infinies)
        max_iterations = 10000
        iterations = 0

        while open_list and iterations < max_iterations:
            iterations += 1

            # Obtenir le nœud avec le plus petit f
            current_node = heapq.heappop(open_list)

            # Ajouter à la liste fermée
            closed_set.add(current_node.position)

            # Vérifier si on a atteint le but
            if current_node.position == goal_node.position:
                # Reconstruire le chemin
                path = []
                node = current_node
                while node is not None:
                    # Convertir les coordonnées de grille en pixels
                    pixel_pos = self.environment.grid_to_pixel(node.position[0], node.position[1])
                    path.append(pixel_pos)
                    node = node.parent

                # Inverser pour avoir le chemin du début à la fin
                path.reverse()

                # Simplifier le chemin (enlever les points intermédiaires inutiles)
                simplified_path = self.simplify_path(path)

                return simplified_path

            # Générer les voisins
            neighbors = self.get_neighbors(current_node.position, self.environment.grid_size)

            for neighbor_pos in neighbors:
                # Ignorer si déjà visité
                if neighbor_pos in closed_set:
                    continue

                # Créer le nœud voisin
                neighbor_node = Node(neighbor_pos, current_node)

                # Calculer les coûts
                # Coût supplémentaire pour les diagonales
                dx = abs(neighbor_pos[0] - current_node.position[0])
                dy = abs(neighbor_pos[1] - current_node.position[1])
                move_cost = 1.414 if (dx == 1 and dy == 1) else 1.0

                neighbor_node.g = current_node.g + move_cost
                neighbor_node.h = self.heuristic(neighbor_pos, goal_node.position)
                neighbor_node.f = neighbor_node.g + neighbor_node.h

                # Vérifier si ce voisin est déjà dans la liste ouverte avec un meilleur coût
                skip = False
                for open_node in open_list:
                    if neighbor_node == open_node and neighbor_node.g >= open_node.g:
                        skip = True
                        break

                if not skip:
                    heapq.heappush(open_list, neighbor_node)

        # Aucun chemin trouvé
        return None

    def simplify_path(self, path: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Simplifie le chemin en enlevant les points intermédiaires alignés

        Args:
            path: Chemin complet avec tous les waypoints

        Returns:
            Chemin simplifié
        """
        if len(path) <= 2:
            return path

        simplified = [path[0]]  # Garder le point de départ

        for i in range(1, len(path) - 1):
            prev = simplified[-1]
            current = path[i]
            next_point = path[i + 1]

            # Vérifier si le point actuel peut être sauté (ligne directe possible)
            if not self.is_line_clear(prev, next_point):
                simplified.append(current)

        simplified.append(path[-1])  # Garder le point d'arrivée

        return simplified

    def is_line_clear(self, pos1: Tuple[int, int], pos2: Tuple[int, int], num_checks: int = 10) -> bool:
        """
        Vérifie s'il y a une ligne claire entre deux points (pas d'obstacles)

        Args:
            pos1: Position de départ
            pos2: Position d'arrivée
            num_checks: Nombre de points à vérifier le long de la ligne

        Returns:
            True si la ligne est claire, False sinon
        """
        for i in range(num_checks + 1):
            t = i / num_checks
            x = int(pos1[0] + t * (pos2[0] - pos1[0]))
            y = int(pos1[1] + t * (pos2[1] - pos1[1]))

            if not self.environment.is_position_valid(x, y):
                return False

        return True

    def find_path_to_target(self, robot_pos: Tuple[int, int], target_pos: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        Trouve un chemin du robot vers la cible

        Args:
            robot_pos: Position actuelle du robot (x, y)
            target_pos: Position de la cible (x, y)

        Returns:
            Liste de waypoints formant le chemin, ou None si aucun chemin
        """
        return self.a_star(robot_pos, target_pos)
