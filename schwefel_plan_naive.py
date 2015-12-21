import sys
import random
from genetic_executor import GeneticExecutor
from genetic_executor import Plan

class SchwefelPlanNaive(Plan):
    def __init__(self, size = 10, chromosome = None):
        if (chromosome is None):
            self.chromosome = []
        else:
            self.chromosome = chromosome
        self.size = size
        self._fitness = None
        self._lower_bound = -65.536
        self._upper_bound = 65.536
        
        
    def get_random_chromosome(self):
        chromosome = []
        for _ in range(self.size):
            chromosome.append(random.uniform(self._lower_bound, self._upper_bound))
        return chromosome
            
            
    def get_child(self, parent2):
        child = SchwefelPlanNaive(self.size)
        for i in range(self.size):
            # crossover
            child.chromosome.append(self.chromosome[i] if random.randint(0, 1) == 0 else parent2.chromosome[i])
            
            # mutate
            if random.randint(1, 10 * self.size) == 1:
                child.chromosome[i] = random.uniform(self._lower_bound, self._upper_bound)
        return child
        
        
    def get_fitness_value(self):
        if self._fitness is not None:
            return self._fitness
        solution = self.chromosome
        self._fitness = -sum([(sum([solution[j] for j in range(i+1)]))**2 for i in range(len(solution))])
        return self._fitness
        
        
    def print_plan(self):
        print(self.chromosome)
            
        
        
if __name__ == '__main__':
    iterations_num = 1
    debug = True
    if len(sys.argv) > 1:
        iterations_num = int(sys.argv[1])
        debug = False
        
    for _ in range(iterations_num):
        sp = SchwefelPlanNaive(10)
        ge = GeneticExecutor(sp, population_size = 200, max_generations_number = 100, debug=debug)
        solution = ge.get_solution()
        print(solution.get_fitness_value())
        