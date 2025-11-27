#!/usr/bin/env python3
"""
Robot Virtuel Guidé par Texte
Point d'entrée principal du programme
"""

import pygame
import sys
import os
from src.environment import Environment
from src.robot import Robot
from src.nlp_parser import NLPParser
from src.pathfinding import PathFinder
from src.evaluator import Evaluator

# Essayer d'importer le parser LLM (optionnel)
try:
    from src.llm_parser import LLMParser
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False


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
    pathfinder = PathFinder(env)
    evaluator = Evaluator()

    # Détecter et initialiser le parser (LLM ou simple)
    parser = None
    use_llm = False

    if LLM_AVAILABLE and os.getenv('GEMINI_API_KEY'):
        try:
            parser = LLMParser()
            use_llm = True
            print("✅ Parser LLM (Gemini) activé - Commandes complexes supportées !")
            print("   Exemple: 'Va au carré rouge en passant par le cercle bleu'\n")
        except Exception as e:
            print(f"⚠️  Erreur LLM ({e}), utilisation du parser simple")
            parser = NLPParser()
    else:
        parser = NLPParser()
        if not os.getenv('GEMINI_API_KEY'):
            print("ℹ️  Parser simple utilisé (pas de clé API Gemini)")
            print("   Pour activer le parser LLM: export GEMINI_API_KEY='votre_cle'\n")

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

    if use_llm:
        # Exemples complexes pour LLM
        examples = [
            "Va vers le carré rouge",
            "Va au carré rouge en passant par le cercle bleu",
            "Rejoins le cercle vert puis le carré jaune",
            "Atteins le bleu",
        ]
    else:
        # Exemples simples
        if hasattr(parser, 'get_alternative_commands'):
            examples = parser.get_alternative_commands()[:5]
        else:
            examples = ["Va vers le carré rouge", "Atteins le cercle bleu"]

    for cmd in examples:
        print(f"  - {cmd}")
    print("-"*60)
    print("\nEntrez 'quit' pour quitter")
    print("Entrez 'reset' pour recommencer\n")

    # Variables de contrôle
    running = True
    clock = pygame.time.Clock()
    waiting_for_command = True
    current_command = ""
    current_targets = []  # Liste des cibles à atteindre
    current_target_index = 0  # Index de la cible actuelle

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

            # Analyser la commande
            print(parser.explain_parsing(command))

            # Parser la commande
            parsed = parser.parse_command(command)

            # Gérer le format LLM (avec targets) ou simple
            targets_to_reach = []

            if use_llm and 'targets' in parsed:
                # Format LLM : liste de targets
                for target_info in parsed['targets']:
                    color = target_info.get('color')
                    shape = target_info.get('shape')
                    target_type = target_info.get('type', 'target')

                    target_obj = env.find_object(color, shape)
                    if target_obj:
                        targets_to_reach.append({
                            'object': target_obj,
                            'type': target_type,
                            'color': color,
                            'shape': shape
                        })
                    else:
                        print(f"⚠️  Cible non trouvée: {color} {shape}")

            else:
                # Format simple : une seule cible
                if not (parsed.get('color') or parsed.get('shape')):
                    print("\nCommande invalide ! Essayez d'inclure une couleur ou une forme.")
                    continue

                target = env.find_object(parsed.get('color'), parsed.get('shape'))
                if target:
                    targets_to_reach.append({
                        'object': target,
                        'type': 'target',
                        'color': parsed.get('color'),
                        'shape': parsed.get('shape')
                    })

            if not targets_to_reach:
                print("\nAucune cible trouvée !")
                print("Cibles disponibles :")
                for obj in env.objects:
                    print(f"  - {obj.color} {obj.shape}")
                continue

            # Afficher le plan
            print("\n" + "="*60)
            print("PLAN D'EXECUTION")
            print("="*60)
            for i, t in enumerate(targets_to_reach, 1):
                t_type = "🎯 Cible finale" if t['type'] == 'target' else "📍 Point de passage"
                print(f"{i}. {t_type}: {t['color']} {t['shape']}")

            # Stocker les cibles
            current_targets = targets_to_reach
            current_target_index = 0
            current_command = command

            # Générer le raisonnement pour la première cible
            first_target = current_targets[0]['object']
            print("\n" + "="*60)
            print("ETAPES DE RAISONNEMENT (Chain-of-Thought)")
            print("="*60)
            reasoning_steps = robot.generate_reasoning(command, first_target, env)
            for step in reasoning_steps:
                robot.add_reasoning_step(step)

            # Planifier le chemin vers la première cible
            print(f"\nPlanification du chemin vers cible {current_target_index + 1}/{len(current_targets)}...")
            path = pathfinder.find_path_to_target(
                robot.get_position(),
                (first_target.x, first_target.y)
            )

            if path is None:
                print("\nAucun chemin trouve vers la cible !")
                continue

            print(f"Chemin trouve avec {len(path)} waypoints !")

            # Définir le chemin pour le robot
            robot.set_path(path)

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

                target_info = f"Cible: {current_target_index + 1}/{len(current_targets)}"
                target_surface = font.render(target_info, True, (0, 0, 0))
                env.screen.blit(target_surface, (10, 35))

                progress_text = f"Waypoint: {robot.current_path_index}/{len(robot.path)}"
                progress_surface = font.render(progress_text, True, (0, 0, 0))
                env.screen.blit(progress_surface, (10, 60))

                pygame.display.flip()
                clock.tick(60)  # 60 FPS

            else:
                # Le robot a atteint la cible actuelle
                current_target = current_targets[current_target_index]
                target_obj = current_target['object']

                success = robot.has_reached_target(target_obj.x, target_obj.y)

                if success:
                    t_type = current_target['type']
                    if t_type == 'waypoint':
                        print(f"\n✅ Point de passage atteint: {current_target['color']} {current_target['shape']}")
                    else:
                        print(f"\n✅ Cible atteinte: {current_target['color']} {current_target['shape']}")

                    # Vérifier s'il y a d'autres cibles
                    current_target_index += 1

                    if current_target_index < len(current_targets):
                        # Aller à la cible suivante
                        next_target = current_targets[current_target_index]
                        next_obj = next_target['object']

                        print(f"\n→ Passage à la cible suivante: {next_target['color']} {next_target['shape']}")

                        # Planifier le nouveau chemin
                        path = pathfinder.find_path_to_target(
                            robot.get_position(),
                            (next_obj.x, next_obj.y)
                        )

                        if path:
                            robot.set_path(path)
                            robot.reached_target = False
                            print(f"Nouveau chemin planifié avec {len(path)} waypoints")
                        else:
                            print("⚠️  Aucun chemin trouvé vers la cible suivante")
                            current_target_index = len(current_targets)  # Terminer

                    else:
                        # Toutes les cibles atteintes
                        print("\n🎉 Toutes les cibles ont été atteintes !")

                        # Terminer l'évaluation
                        evaluator.end_test(True, robot)

                        # Dessiner l'état final
                        env.draw(robot)
                        pygame.display.flip()

                        # Petite pause avant la prochaine commande
                        pygame.time.wait(1500)

                        # Réinitialiser
                        robot.reset()
                        current_targets = []
                        current_target_index = 0
                        waiting_for_command = True

                else:
                    print("\nEchec : cible non atteinte")

                    # Terminer l'évaluation
                    evaluator.end_test(False, robot)

                    # Dessiner l'état final
                    env.draw(robot)
                    pygame.display.flip()

                    # Petite pause
                    pygame.time.wait(1000)

                    # Réinitialiser
                    robot.reset()
                    current_targets = []
                    current_target_index = 0
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
