import time
from typing import List, Dict

class Evaluator:
    """Évalue les performances du robot"""

    def __init__(self):
        self.results: List[Dict] = []
        self.current_test = None

    def start_test(self, command: str, environment_name: str):
        """Démarre un nouveau test"""
        self.current_test = {
            'command': command,
            'environment': environment_name,
            'start_time': time.time(),
            'end_time': None,
            'success': False,
            'actions_count': 0,
            'distance_traveled': 0,
            'path_length': 0,
            'reasoning_steps': []
        }

    def end_test(self, success: bool, robot):
        """Termine le test en cours"""
        if self.current_test is None:
            return

        self.current_test['end_time'] = time.time()
        self.current_test['success'] = success
        self.current_test['actions_count'] = robot.total_actions
        self.current_test['path_length'] = len(robot.path)
        self.current_test['reasoning_steps'] = robot.reasoning_steps.copy()

        # Calculer le temps d'exécution
        execution_time = self.current_test['end_time'] - self.current_test['start_time']
        self.current_test['execution_time'] = execution_time

        self.results.append(self.current_test)
        self.current_test = None

    def get_success_rate(self) -> float:
        """Calcule le taux de réussite"""
        if not self.results:
            return 0.0

        successes = sum(1 for r in self.results if r['success'])
        return (successes / len(self.results)) * 100

    def get_average_actions(self) -> float:
        """Calcule le nombre moyen d'actions"""
        if not self.results:
            return 0.0

        successful_results = [r for r in self.results if r['success']]
        if not successful_results:
            return 0.0

        total_actions = sum(r['actions_count'] for r in successful_results)
        return total_actions / len(successful_results)

    def get_average_execution_time(self) -> float:
        """Calcule le temps d'exécution moyen"""
        if not self.results:
            return 0.0

        successful_results = [r for r in self.results if r['success']]
        if not successful_results:
            return 0.0

        total_time = sum(r['execution_time'] for r in successful_results)
        return total_time / len(successful_results)

    def print_summary(self):
        """Affiche un résumé des résultats"""
        print("\n" + "="*60)
        print("RESUME DES TESTS")
        print("="*60)

        print(f"\nNombre total de tests : {len(self.results)}")
        print(f"Taux de reussite : {self.get_success_rate():.1f}%")
        print(f"Actions moyennes (succes) : {self.get_average_actions():.1f}")
        print(f"Temps d'execution moyen : {self.get_average_execution_time():.2f}s")

        print("\n" + "-"*60)
        print("Details des tests :")
        print("-"*60)

        for i, result in enumerate(self.results, 1):
            status = "SUCCES" if result['success'] else "ECHEC"
            print(f"\nTest {i}: {status}")
            print(f"  Commande : '{result['command']}'")
            print(f"  Environnement : {result['environment']}")
            print(f"  Actions : {result['actions_count']}")
            print(f"  Waypoints : {result['path_length']}")
            print(f"  Temps : {result['execution_time']:.2f}s")

            if result['reasoning_steps']:
                print(f"  Etapes de raisonnement :")
                for step in result['reasoning_steps']:
                    print(f"    - {step}")

        print("\n" + "="*60)

    def export_results(self, filename: str = "results.txt"):
        """Exporte les résultats dans un fichier"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("RESUME DES TESTS - ROBOT VIRTUEL\n")
            f.write("="*60 + "\n\n")

            f.write(f"Nombre total de tests : {len(self.results)}\n")
            f.write(f"Taux de reussite : {self.get_success_rate():.1f}%\n")
            f.write(f"Actions moyennes : {self.get_average_actions():.1f}\n")
            f.write(f"Temps moyen : {self.get_average_execution_time():.2f}s\n\n")

            f.write("-"*60 + "\n")
            f.write("DETAILS DES TESTS\n")
            f.write("-"*60 + "\n\n")

            for i, result in enumerate(self.results, 1):
                status = "SUCCES" if result['success'] else "ECHEC"
                f.write(f"Test {i}: {status}\n")
                f.write(f"  Commande : {result['command']}\n")
                f.write(f"  Environnement : {result['environment']}\n")
                f.write(f"  Actions : {result['actions_count']}\n")
                f.write(f"  Temps : {result['execution_time']:.2f}s\n")

                if result['reasoning_steps']:
                    f.write(f"  Raisonnement :\n")
                    for step in result['reasoning_steps']:
                        f.write(f"    - {step}\n")

                f.write("\n")

        print(f"\nResultats exportes dans '{filename}'")
