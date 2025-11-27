#!/usr/bin/env python3
"""
Scénarios de test automatiques pour le robot virtuel
Teste différents environnements et commandes
"""

import pygame
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.environment import Environment
from src.robot import Robot
from src.nlp_parser import NLPParser
from src.pathfinding import PathFinder
from src.evaluator import Evaluator


def run_test_scenario(env_name: str, env_setup_func, commands: list, headless: bool = False):
    """
    Exécute un scénario de test complet

    Args:
        env_name: Nom de l'environnement
        env_setup_func: Fonction pour configurer l'environnement
        commands: Liste de commandes à tester
        headless: Si True, ne pas afficher la fenêtre (plus rapide)
    """
    print("\n" + "="*60)
    print(f"TEST SCENARIO: {env_name}")
    print("="*60)

    # Initialiser les composants
    if not headless:
        env = Environment(width=800, height=600, grid_size=20)
    else:
        # Mode headless pour tests rapides
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        env = Environment(width=800, height=600, grid_size=20)

    robot = Robot(x=100, y=100, size=25)
    parser = NLPParser()
    pathfinder = PathFinder(env)
    evaluator = Evaluator()

    # Configurer l'environnement
    env_setup_func(env)

    print(f"\nEnvironnement: {env_name}")
    print(f"Nombre de tests: {len(commands)}")
    print(f"Objets disponibles: {len(env.objects)}")
    print(f"Obstacles: {len(env.obstacles)}\n")

    # Exécuter chaque commande
    for i, command in enumerate(commands, 1):
        print(f"\n[Test {i}/{len(commands)}] Commande: '{command}'")

        # Parser la commande
        parsed = parser.parse_command(command)
        print(f"  Parse: color={parsed['color']}, shape={parsed['shape']}")

        # Trouver la cible
        target = env.find_object(parsed['color'], parsed['shape'])

        if target is None:
            print(f"  ECHEC: Cible non trouvee")
            evaluator.start_test(command, env_name)
            evaluator.end_test(False, robot)
            robot.reset()
            continue

        # Générer le raisonnement
        reasoning_steps = robot.generate_reasoning(command, target, env)
        for step in reasoning_steps:
            robot.add_reasoning_step(step)

        # Planifier le chemin
        path = pathfinder.find_path_to_target(
            robot.get_position(),
            (target.x, target.y)
        )

        if path is None:
            print(f"  ECHEC: Aucun chemin trouve")
            evaluator.start_test(command, env_name)
            evaluator.end_test(False, robot)
            robot.reset()
            continue

        print(f"  Chemin: {len(path)} waypoints")

        # Définir le chemin
        robot.set_path(path)

        # Démarrer l'évaluation
        evaluator.start_test(command, env_name)

        # Simuler le mouvement (mode rapide)
        max_iterations = 1000
        iterations = 0

        while not robot.reached_target and iterations < max_iterations:
            robot.move_along_path()
            iterations += 1

            # Affichage visuel (si pas headless)
            if not headless and iterations % 10 == 0:
                env.draw(robot)
                pygame.display.flip()

        # Vérifier le succès
        success = robot.has_reached_target(target.x, target.y)

        if success:
            print(f"  SUCCES: Cible atteinte en {robot.total_actions} actions")
        else:
            print(f"  ECHEC: Cible non atteinte apres {iterations} iterations")

        # Terminer l'évaluation
        evaluator.end_test(success, robot)

        # Réinitialiser le robot
        robot.reset()

    # Afficher le résumé
    evaluator.print_summary()

    return evaluator


def main():
    """Fonction principale des tests"""
    print("="*60)
    print("TESTS AUTOMATIQUES - ROBOT VIRTUEL")
    print("="*60)

    all_evaluators = []

    # Test 1 : Environnement Simple
    simple_commands = [
        "Va vers le carre rouge",
        "Va vers le cercle bleu",
        "Atteins le carre vert",
        "Va vers le rouge",
        "Deplace-toi vers le bleu"
    ]
    evaluator1 = run_test_scenario(
        "Simple",
        lambda e: e.create_simple_environment(),
        simple_commands,
        headless=True
    )
    all_evaluators.append(evaluator1)

    # Test 2 : Environnement Labyrinthe
    maze_commands = [
        "Va vers le carre rouge",
        "Atteins le cercle bleu",
        "Va vers le rouge",
    ]
    evaluator2 = run_test_scenario(
        "Labyrinthe",
        lambda e: e.create_maze_environment(),
        maze_commands,
        headless=True
    )
    all_evaluators.append(evaluator2)

    # Test 3 : Environnement Ouvert
    open_commands = [
        "Va vers le carre rouge",
        "Va vers le cercle bleu",
        "Atteins le carre vert",
        "Va vers le cercle jaune",
        "Va vers le vert"
    ]
    evaluator3 = run_test_scenario(
        "Ouvert",
        lambda e: e.create_open_environment(),
        open_commands,
        headless=True
    )
    all_evaluators.append(evaluator3)

    # Résumé global
    print("\n" + "="*60)
    print("RESUME GLOBAL DE TOUS LES TESTS")
    print("="*60)

    total_tests = sum(len(e.results) for e in all_evaluators)
    total_successes = sum(sum(1 for r in e.results if r['success']) for e in all_evaluators)
    global_success_rate = (total_successes / total_tests * 100) if total_tests > 0 else 0

    print(f"\nNombre total de tests: {total_tests}")
    print(f"Nombre de succes: {total_successes}")
    print(f"Nombre d'echecs: {total_tests - total_successes}")
    print(f"Taux de reussite global: {global_success_rate:.1f}%")

    # Calculer les moyennes globales
    all_actions = []
    all_times = []

    for evaluator in all_evaluators:
        for result in evaluator.results:
            if result['success']:
                all_actions.append(result['actions_count'])
                all_times.append(result['execution_time'])

    if all_actions:
        avg_actions = sum(all_actions) / len(all_actions)
        avg_time = sum(all_times) / len(all_times)
        print(f"Actions moyennes: {avg_actions:.1f}")
        print(f"Temps moyen: {avg_time:.2f}s")

    print("\n" + "="*60)

    # Exporter les résultats
    print("\nExportation des resultats...")
    for i, evaluator in enumerate(all_evaluators, 1):
        evaluator.export_results(f"test_results_{i}.txt")

    pygame.quit()
    print("\nTests termines !")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterruption par l'utilisateur.")
        pygame.quit()
        sys.exit(0)
