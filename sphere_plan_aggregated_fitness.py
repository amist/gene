import sys
import statistics
import random
from genetic_executor import GeneticExecutor
from genetic_executor import Plan

class SphereAggregatedFitnessPlan(Plan):
    def __init__(self, size = 10, chromosome = None):
        if (chromosome is None):
            self.chromosome = []
        else:
            self.chromosome = chromosome
        self.aggregated_fitness = []
        self.size = size
        self._fitness = None
        self._lower_bound = -5.12
        self._upper_bound = 5.12
        
        
    def get_random_chromosome(self):
        chromosome = []
        for _ in range(self.size):
            chromosome.append(random.uniform(self._lower_bound, self._upper_bound))
        return chromosome
            
            
    def get_child(self, parent2, mutation_factor=1):
        child = SphereAggregatedFitnessPlan(self.size)
        for i in range(self.size):
            # crossover
            if self.aggregated_fitness[i] > parent2.aggregated_fitness[i]:
                child.chromosome.append(self.chromosome[i])
            elif self.aggregated_fitness[i] < parent2.aggregated_fitness[i]:
                child.chromosome.append(parent2.chromosome[i])
            else:
                child.chromosome.append(self.chromosome[i] if random.randint(0, 1) == 0 else parent2.chromosome[i])
            
            # mutate
            if random.randint(1, int(10 * self.size / (mutation_factor + 1))) == 1:
                child.chromosome[i] = mutation_factor * random.uniform(self._lower_bound, self._upper_bound)
        return child
        
        
    def get_fitness_value(self):
        if self._fitness is not None:
            return self._fitness
        self.aggregated_fitness = [-x*x for x in self.chromosome]
        self._fitness = sum(self.aggregated_fitness)
        return self._fitness
        
        
    def print_plan(self):
        print(self.chromosome)
            
def main():
    iterations_num = 1
    debug = True
    results = []
    if len(sys.argv) > 1:
        iterations_num = int(sys.argv[1])
        debug = False
        
    for _ in range(iterations_num):
        sp = SphereAggregatedFitnessPlan(10)
        ge = GeneticExecutor(sp, population_size = 200, max_generations_number = 100, debug=debug, log_metadata=True)
        solution = ge.get_solution()
        
        if debug:
            solution.print_plan()
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