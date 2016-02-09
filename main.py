from ge.core.genetic_executor import GeneticExecutor
from ge.problems.sphere_problem import SphereIndividual

if __name__ == '__main__':
    ge_config = {'individual_class': SphereIndividual,
                 'individual_kwargs': {'size': 10},
                 'population_size': 200,
                 'max_generations_number': 100,
                 'debug': False,
                 'log_metadata': False,
                }
    ge = GeneticExecutor(**ge_config)
    solution = ge.get_solution()
    print(solution.chromosome)
    print(solution.get_fitness_value())
