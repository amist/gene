'''Run the algorithm a number of times to get runs' statistics
'''
import argparse
import statistics
from ge.core.genetic_executor import GeneticExecutor
from ge.problems import *
            
def run_itarations(individual_class, ge_config):
    parser = argparse.ArgumentParser(description='Run genetic executor a number of times')
    parser.add_argument('n', type=int, nargs='?', default=1, help='number of iterations')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='debug mode: show the best solution for each generation')
    args = parser.parse_args()
    
    iterations_num = args.n
    debug = args.debug
    results = []
        
    for _ in range(iterations_num):
        genetic_executor = GeneticExecutor(**ge_config)
        solution = genetic_executor.get_solution()
        
        if debug:
            solution.print_chromosome()
        print(solution.get_fitness_value())
        results.append(solution.get_fitness_value())
    print_statistics(results)
    
        
def print_statistics(results):
    [mean, std] = [results[0], 0]
    if len(results) > 1:
        [mean, std] = [statistics.mean(results), statistics.stdev(results)]
        
    print('==============================')
    print('Mean: ' + str(mean))
    print('STD:  ' + str(std))
    
        
if __name__ == '__main__':
    ge_config = {'individual_class': SphereIndividual,
                 'individual_kwargs': {'size': 10},
                 'population_size': 200,
                 'max_generations_number': 100,
                 'debug': False,
                 'log_metadata': False,
                }
    run_itarations(SphereIndividual, ge_config)
