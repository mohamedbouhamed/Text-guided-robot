#!/usr/bin/env python3
"""
Robot Virtuel Guidé par Texte
Point d'entrée principal du programme
"""

import pygame
import sys
from src.environment import Environment
from src.robot import Robot
from src.nlp_parser import NLPParser
from src.pathfinding import PathFinder
from src.evaluator import Evaluator


def main():
    """Fonction principale du programme"""
    print("="*60)
    print("ROBOT VIRTUEL GUIDE PAR TEXTE")
    print("="*60)
    print("\nBienvenue ! Ce robot peut comprendre et executer des")
    print("commandes en langage naturel.\n")

    # Initialiser les composants
    env = Environment(width=800, height=600, grid_size=20)
    robot = Robot(x=100, y=100, size=25)
    parser = NLPParser()
    pathfinder = PathFinder(env)
    evaluator = Evaluator()

    # Choix de l'environnement
    print("\nChoisissez un environnement :")
    print("1. Simple (quelques obstacles)")
    print("2. Labyrinthe (complexe)")
    print("3. Ouvert (plusieurs cibles)")

    choice = input("\nVotre choix (1-3) : ").strip()

    if choice == "1":
        env.create_simple_environment()
        env_name = "Simple"
    elif choice == "2":
        env.create_maze_environment()
        env_name = "Labyrinthe"
    elif choice == "3":
        env.create_open_environment()
        env_name = "Ouvert"
    else:
        print("Choix invalide, utilisation de l'environnement simple.")
        env.create_simple_environment()
        env_name = "Simple"

    print(f"\nEnvironnement '{env_name}' charge !")
    print("\n" + "-"*60)
    print("EXEMPLES DE COMMANDES :")
    print("-"*60)
    for cmd in parser.get_alternative_commands()[:5]:
        print(f"  - {cmd}")
    print("-"*60)
    print("\nEntrez 'quit' pour quitter")
    print("Entrez 'reset' pour recommencer")
    print("Entrez 'test' pour mode test automatique\n")

    # Variables de contrôle
    running = True
    clock = pygame.time.Clock()
    waiting_for_command = True
    current_command = ""
    mode = "manual"  # "manual" ou "auto"

    while running:
        # Gestion des événements Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if waiting_for_command:
            # Dessiner l'état actuel
            env.draw(robot)
            pygame.display.flip()

            # Attendre une commande de l'utilisateur
            command = input("\nCommande > ").strip()

            if not command:
                continue

            if command.lower() == 'quit':
                running = False
                continue

            if command.lower() == 'reset':
                robot.reset()
                print("\nRobot reinitialise !")
                continue

            if command.lower() == 'test':
                print("\nPassage en mode test automatique...")
                print("Le robot va executer plusieurs commandes automatiquement.\n")
                mode = "auto"
                waiting_for_command = False
                continue

            # Analyser la commande
            print(parser.explain_parsing(command))

            if not parser.is_valid_command(command):
                print("\nCommande invalide ! Essayez d'inclure une couleur ou une forme.")
                continue

            # Parser la commande
            parsed = parser.parse_command(command)

            # Trouver l'objet cible
            target = env.find_object(parsed['color'], parsed['shape'])

            if target is None:
                print(f"\nAucune cible trouvee pour : {parsed['color']} {parsed['shape']}")
                print("Cibles disponibles :")
                for obj in env.objects:
                    print(f"  - {obj.color} {obj.shape}")
                continue

            # Générer le raisonnement (Chain-of-Thought)
            print("\n" + "="*60)
            print("ETAPES DE RAISONNEMENT (Chain-of-Thought)")
            print("="*60)
            reasoning_steps = robot.generate_reasoning(command, target, env)
            for step in reasoning_steps:
                robot.add_reasoning_step(step)

            # Planifier le chemin avec A*
            print("\nPlanification du chemin avec A*...")
            path = pathfinder.find_path_to_target(
                robot.get_position(),
                (target.x, target.y)
            )

            if path is None:
                print("\nAucun chemin trouve vers la cible !")
                continue

            print(f"Chemin trouve avec {len(path)} waypoints !")

            # Définir le chemin pour le robot
            robot.set_path(path)

            current_command = command
            waiting_for_command = False

            # Démarrer l'évaluation
            evaluator.start_test(command, env_name)

        else:
            # Mode animation : déplacer le robot
            if not robot.reached_target:
                robot.move_along_path()

                # Dessiner la scène
                env.draw(robot)

                # Afficher les informations
                font = pygame.font.Font(None, 24)
                status_text = f"Commande: {current_command}"
                text_surface = font.render(status_text, True, (0, 0, 0))
                env.screen.blit(text_surface, (10, 10))

                progress_text = f"Waypoint: {robot.current_path_index}/{len(robot.path)}"
                progress_surface = font.render(progress_text, True, (0, 0, 0))
                env.screen.blit(progress_surface, (10, 35))

                pygame.display.flip()
                clock.tick(60)  # 60 FPS

            else:
                # Le robot a atteint la cible
                target_obj = env.find_object(
                    parser.parse_command(current_command)['color'],
                    parser.parse_command(current_command)['shape']
                )

                success = robot.has_reached_target(target_obj.x, target_obj.y)

                if success:
                    print("\nCible atteinte avec succes !")
                else:
                    print("\nEchec : cible non atteinte")

                # Terminer l'évaluation
                evaluator.end_test(success, robot)

                # Dessiner l'état final
                env.draw(robot)
                pygame.display.flip()

                # Petite pause avant la prochaine commande
                pygame.time.wait(1000)

                # Réinitialiser le robot
                robot.reset()

                waiting_for_command = True

    # Fin du programme
    print("\n" + "="*60)
    print("Fermeture du programme...")

    if len(evaluator.results) > 0:
        evaluator.print_summary()
        export = input("\nExporter les resultats dans un fichier ? (o/n) : ").strip().lower()
        if export == 'o':
            evaluator.export_results("results.txt")

    pygame.quit()
    print("\nAu revoir !")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterruption par l'utilisateur. Au revoir !")
        pygame.quit()
        sys.exit(0)
