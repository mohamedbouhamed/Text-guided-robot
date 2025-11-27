import pygame
import numpy as np
from typing import List, Tuple, Dict

class GameObject:
    """Représente un objet dans l'environnement"""
    def __init__(self, x: int, y: int, color: str, shape: str, size: int = 30):
        self.x = x
        self.y = y
        self.color = color
        self.shape = shape  # 'square' ou 'circle'
        self.size = size

        # Mapping des couleurs
        self.color_map = {
            'rouge': (255, 0, 0),
            'red': (255, 0, 0),
            'bleu': (0, 0, 255),
            'blue': (0, 0, 255),
            'vert': (0, 255, 0),
            'green': (0, 255, 0),
            'jaune': (255, 255, 0),
            'yellow': (255, 255, 0),
            'orange': (255, 165, 0),
            'violet': (128, 0, 128),
            'purple': (128, 0, 128),
        }

    def get_rgb_color(self) -> Tuple[int, int, int]:
        """Retourne la couleur RGB"""
        return self.color_map.get(self.color.lower(), (128, 128, 128))

    def draw(self, screen: pygame.Surface):
        """Dessine l'objet sur l'écran"""
        color_rgb = self.get_rgb_color()

        if self.shape == 'square' or self.shape == 'carré':
            pygame.draw.rect(screen, color_rgb,
                           (self.x - self.size//2, self.y - self.size//2,
                            self.size, self.size))
        elif self.shape == 'circle' or self.shape == 'cercle':
            pygame.draw.circle(screen, color_rgb, (self.x, self.y), self.size//2)

    def contains_point(self, px: int, py: int) -> bool:
        """Vérifie si un point est à l'intérieur de l'objet"""
        if self.shape == 'square' or self.shape == 'carré':
            return (abs(px - self.x) <= self.size//2 and
                   abs(py - self.y) <= self.size//2)
        else:  # circle
            distance = np.sqrt((px - self.x)**2 + (py - self.y)**2)
            return distance <= self.size//2


class Obstacle:
    """Représente un obstacle dans l'environnement"""
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (100, 100, 100)  # Gris

    def draw(self, screen: pygame.Surface):
        """Dessine l'obstacle"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def collides_with_point(self, px: int, py: int, margin: int = 0) -> bool:
        """Vérifie si un point entre en collision avec l'obstacle"""
        return (self.x - margin <= px <= self.x + self.width + margin and
                self.y - margin <= py <= self.y + self.height + margin)


class Environment:
    """Environnement 2D pour la simulation"""
    def __init__(self, width: int = 800, height: int = 600, grid_size: int = 20):
        self.width = width
        self.height = height
        self.grid_size = grid_size

        # Initialisation de Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Robot Virtuel Guidé par Texte")
        self.clock = pygame.time.Clock()

        # Objets et obstacles
        self.objects: List[GameObject] = []
        self.obstacles: List[Obstacle] = []

        # Grille pour la planification de chemin
        self.grid_width = width // grid_size
        self.grid_height = height // grid_size

    def add_object(self, x: int, y: int, color: str, shape: str, size: int = 30):
        """Ajoute un objet cible dans l'environnement"""
        obj = GameObject(x, y, color, shape, size)
        self.objects.append(obj)
        return obj

    def add_obstacle(self, x: int, y: int, width: int, height: int):
        """Ajoute un obstacle dans l'environnement"""
        obstacle = Obstacle(x, y, width, height)
        self.obstacles.append(obstacle)
        return obstacle

    def find_object(self, color: str = None, shape: str = None) -> GameObject:
        """Trouve un objet par couleur et/ou forme"""
        for obj in self.objects:
            color_match = color is None or obj.color.lower() == color.lower()
            shape_match = shape is None or obj.shape.lower() == shape.lower()

            if color_match and shape_match:
                return obj
        return None

    def is_position_valid(self, x: int, y: int, margin: int = 15) -> bool:
        """Vérifie si une position est valide (pas d'obstacle, dans les limites)"""
        # Vérifier les limites
        if x < margin or x >= self.width - margin or y < margin or y >= self.height - margin:
            return False

        # Vérifier les collisions avec les obstacles
        for obstacle in self.obstacles:
            if obstacle.collides_with_point(x, y, margin):
                return False

        return True

    def grid_to_pixel(self, grid_x: int, grid_y: int) -> Tuple[int, int]:
        """Convertit une coordonnée de grille en pixel"""
        return (grid_x * self.grid_size + self.grid_size // 2,
                grid_y * self.grid_size + self.grid_size // 2)

    def pixel_to_grid(self, px: int, py: int) -> Tuple[int, int]:
        """Convertit une coordonnée pixel en grille"""
        return (px // self.grid_size, py // self.grid_size)

    def draw(self, robot=None):
        """Dessine l'environnement complet"""
        # Fond blanc
        self.screen.fill((255, 255, 255))

        # Grille légère (optionnelle)
        for x in range(0, self.width, self.grid_size):
            pygame.draw.line(self.screen, (230, 230, 230), (x, 0), (x, self.height))
        for y in range(0, self.height, self.grid_size):
            pygame.draw.line(self.screen, (230, 230, 230), (0, y), (self.width, y))

        # Dessiner les obstacles
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        # Dessiner les objets cibles
        for obj in self.objects:
            obj.draw(self.screen)
            # Ajouter un label
            font = pygame.font.Font(None, 20)
            label = f"{obj.color} {obj.shape}"
            text = font.render(label, True, (0, 0, 0))
            self.screen.blit(text, (obj.x - 30, obj.y + obj.size))

        # Dessiner le robot
        if robot:
            robot.draw(self.screen)

        pygame.display.flip()

    def create_simple_environment(self):
        """Crée un environnement simple avec quelques objets et obstacles"""
        # Ajouter des objets cibles
        self.add_object(650, 100, 'rouge', 'square', 40)
        self.add_object(150, 450, 'bleu', 'circle', 40)
        self.add_object(650, 450, 'vert', 'square', 40)

        # Ajouter quelques obstacles
        self.add_obstacle(300, 200, 200, 30)
        self.add_obstacle(400, 350, 30, 150)

    def create_maze_environment(self):
        """Crée un environnement type labyrinthe"""
        # Objets cibles
        self.add_object(700, 500, 'rouge', 'square', 35)
        self.add_object(100, 500, 'bleu', 'circle', 35)

        # Obstacles formant un labyrinthe
        self.add_obstacle(150, 100, 500, 30)
        self.add_obstacle(150, 100, 30, 200)
        self.add_obstacle(150, 270, 350, 30)
        self.add_obstacle(470, 130, 30, 170)
        self.add_obstacle(470, 300, 180, 30)
        self.add_obstacle(620, 130, 30, 200)
        self.add_obstacle(300, 400, 350, 30)

    def create_open_environment(self):
        """Crée un environnement ouvert avec peu d'obstacles"""
        # Plusieurs objets cibles
        self.add_object(200, 150, 'rouge', 'square', 35)
        self.add_object(600, 150, 'bleu', 'circle', 35)
        self.add_object(400, 450, 'vert', 'square', 35)
        self.add_object(650, 450, 'jaune', 'circle', 35)

        # Quelques obstacles dispersés
        self.add_obstacle(350, 250, 100, 100)
