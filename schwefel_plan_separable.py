import sys
import random
import statistics
from genetic_executor import GeneticExecutor
from genetic_executor import Plan

class SchwefelPlanSeparable(Plan):
    def __init__(self, size = 10, chromosome = None):
        if (chromosome is None):
            self.chromosome = []
        else:
            self.chromosome = chromosome
        self.size = size
        self._fitness = None
        self._lower_bound = -65.536
        self._upper_bound = 65.536
        
        
    def get_chromosome_size(self):
        return self.size
        
        
    def get_random_chromosome(self):
        chromosome = []
        for _ in range(self.get_chromosome_size()):
            chromosome.append(random.uniform(self._lower_bound, self._upper_bound))
        return chromosome
            
            
    def get_child(self, parent2):
        child = SchwefelPlanSeparable(self.size)
        for i in range(self.get_chromosome_size()):
            # crossover
            child.chromosome.append(self.chromosome[i] if random.randint(0, 1) == 0 else parent2.chromosome[i])
            
            # mutate
            if random.randint(1, 10 * self.get_chromosome_size()) == 1:
                rand_val = random.uniform(self._lower_bound, self._upper_bound)
                rand_val = child.chromosome[i] + 0.01 * (rand_val - 0.5 * (self._lower_bound + self._upper_bound))
                child.chromosome[i] = rand_val
        return child
        
        
    def get_solution_vector(self):
        # the solution vector is:   x_1, x_2, x_3, ...
        # the chromosome is:        y_1, y_2, y_3, ...
        # where:                    y_1 = x_1
        #                           y_2 = x_1 + x_2
        #                           y_3 = x_1 + x_2 + x_3
        # so:                       x_1 = y_1
        #                           x_2 = y_2 - y_1
        #                           x_3 = y_3 - y_2
        # the inseparable Schwefel's double sum transform into a separable isomorphic problem
        solution = [self.chromosome[0]]
        for i in range(self.get_chromosome_size() - 1):
            solution.append(self.chromosome[i+1] - self.chromosome[i])
        return solution
        
        
    def get_fitness_value(self):
        if self._fitness is not None:
            return self._fitness
        solution = self.get_solution_vector()
        self._fitness = -sum([(sum([solution[j] for j in range(i+1)]))**2 for i in range(len(solution))])
        return self._fitness
        
        
    def print_plan(self):
        print(self.chromosome)
        print(self.get_solution_vector())
            
        
def run_iterations(iterations_num):
    solutions = []

    for _ in range(iterations_num):
        sp = SchwefelPlanSeparable(10)
        ge = GeneticExecutor(sp, population_size=200, max_generations_number=100, debug=debug)
        solution = ge.get_solution()
        
        solutions.append(solution.get_fitness_value())
        print(solution.get_fitness_value())
        
    print('==============================')
    print('Mean: ' + str(statistics.mean(solutions)))
    print('STD:  ' + str(statistics.stdev(solutions)))
        
        
if __name__ == '__main__':
    iterations_num = 1
    debug = True
    if len(sys.argv) > 1:
        iterations_num = int(sys.argv[1])
        debug = False
        
    run_iterations(iterations_num)
        