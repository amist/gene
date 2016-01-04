import sys
import random
import statistics
import math
from genetic_executor import GeneticExecutor
from genetic_executor import Plan
from args_plan import ArgsPlan

class RosenbrockPlanSeparable(Plan):
    def __init__(self, size=10, mutation_probability=10, size_dependant_mutation_probability=True, mutation_step_factor=0.01):
        self.chromosome = []
        self.size = size
        self._fitness = None
        self._lower_bound = -2.048
        self._upper_bound = 2.048
        
        self._mutation_probability = mutation_probability
        self._size_dependant_mutation_probability = size_dependant_mutation_probability
        self._actual_mutation_probability = self._mutation_probability
        if self._size_dependant_mutation_probability:
            self._actual_mutation_probability = self.size * self._mutation_probability
        self._mutation_step_factor = mutation_step_factor
        
        
    def get_random_chromosome(self):
        chromosome = []
        for _ in range(self.size):
            chromosome.append(random.uniform(self._lower_bound, self._upper_bound))
        return chromosome
            
            
    def get_child(self, parent2, mutation_factor=1):
        child = RosenbrockPlanSeparable(self.size)
        for i in range(self.size):
            # crossover
            child.chromosome.append(self.chromosome[i] if random.randint(0, 1) == 0 else parent2.chromosome[i])
            
            # mutate
            #print(self._actual_mutation_probability)
            if random.randint(0, int(self._actual_mutation_probability / (mutation_factor + 1))) == 0:
                rand_val = random.uniform(self._lower_bound, self._upper_bound)
                rand_val = child.chromosome[i] + mutation_factor * self._mutation_step_factor * (random.uniform(self._lower_bound, self._upper_bound) - 0.5 * (self._lower_bound + self._upper_bound))
                child.chromosome[i] = rand_val
        return child
        
        
    def get_solution_vector(self):
        solution = [self.chromosome[0]]
        for i in range(len(self.chromosome) - 1):
            #solution.append( self.chromosome[i+1] + ( 200*self.chromosome[i]**2 + 1 - self.chromosome[i] ) / 200 )
            temp = self.chromosome[i] - (solution[i-1] - self.chromosome[i-1])**2
            if temp < 0:
                temp = 0
            solution.append( solution[i-1]**2 + math.sqrt( temp ) / 200 )
        return solution
        
        
    def get_fitness_value(self):
        if self._fitness is not None:
            return self._fitness
        solution = self.get_solution_vector()
        self._fitness = -sum([( 100 * ( solution[i+1] - solution[i]**2 )**2 + ( solution[i] - 1 )**2 ) for i in range(len(solution)-1)])
        return self._fitness
        
        
    def print_plan(self):
        print(self.chromosome)
            
        
    
def run_iterations(genetic_executor, iterations_num, debug=True):
    results = []

    for _ in range(iterations_num):
        
        ge = genetic_executor
        solution = ge.get_solution()
        
        results.append(solution.get_fitness_value())
        if debug:
            print(solution.get_fitness_value())
        
    if len(results) == 1:
        return [results[0], 0]
    
    return [statistics.mean(results), statistics.stdev(results)]
    
        
def find_algorithm_parameters():
    sp = RosenbrockPlanSeparable()
    inner_ge = GeneticExecutor(sp, debug=False)
    
    ap = ArgsPlan(inner_ge)
    ge = GeneticExecutor(ap, population_size=3, max_generations_number=1000, debug=True)
    solution = ge.get_solution()
    print(solution)
    
    
def run_algorithm():
    iterations_num = 1
    debug = True
    if len(sys.argv) > 1:
        iterations_num = int(sys.argv[1])
        debug = False
        
    sp = RosenbrockPlanSeparable()
    ge = GeneticExecutor(sp, debug=debug)
    
    [mean, std] = run_iterations(genetic_executor=ge, iterations_num=iterations_num)
    
    print('==============================')
    print('Mean: ' + str(mean))
    print('STD:  ' + str(std))
    
    
if __name__ == '__main__':
    
    #find_algorithm_parameters()
    
    run_algorithm()
    
    
    
    
    
    
    
    
    
    