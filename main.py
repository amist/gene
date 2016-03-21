'''An example for usage to get one solution
'''
from ge.core.genetic_executor import GeneticExecutor
from ge.problems.sphere_problem import SphereIndividual
from ge.problems.schwefel_sin_naive_problem import SchwefelSinNaiveIndividual
from ge.core.populations.basic_population import BasicPopulation
from ge.core.populations.medium_population import MediumPopulation

def get_solution():
    ge_config = {'individual_class': SphereIndividual,
                 'individual_kwargs': {'size': 10},
                 'population_class': MediumPopulation,
                 'population_size': 200,
                 'max_generations_number': 100,
                 'debug': False,
                 'log_metadata': {'log_filename': 'generations_data.p'},
                 'mutation_a_b': True,
                }
    ge = GeneticExecutor(**ge_config)
    return ge.get_solution()
    

def main():
    solution = get_solution()
    print(solution.chromosome)
    print(solution.get_fitness_value())

if __name__ == '__main__':
    main()