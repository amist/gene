import sys
import statistics
import random
from ge.core.genetic_executor import GeneticExecutor
from ge.problems.sphere_problem import SphereIndividual
            
def main():
    iterations_num = 1
    debug = True
    results = []
    if len(sys.argv) > 1:
        iterations_num = int(sys.argv[1])
        debug = False
        
    for _ in range(iterations_num):
        genetic_executor = GeneticExecutor(SphereIndividual, {'size': 10}, population_size=200, max_generations_number=100)    
        solution = genetic_executor.get_solution()
        
        if debug:
            solution.print_chromosome()
        print(solution.get_fitness_value())
        results.append(solution.get_fitness_value())
        
    [mean, std] = [results[0], 0]
    if len(results) > 1:
        [mean, std] = [statistics.mean(results), statistics.stdev(results)]
        
    print('==============================')
    print('Mean: ' + str(mean))
    print('STD:  ' + str(std))
        
if __name__ == '__main__':
    main()
