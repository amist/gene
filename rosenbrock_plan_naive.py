import sys
import random
import statistics
from genetic_executor import GeneticExecutor
from genetic_executor import Plan
from genetic_executor import FitnessDecorator
from args_plan import ArgsPlan

class RosenbrockPlanNaive(Plan):
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
        child = RosenbrockPlanNaive(self.size)
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
        
        
    @FitnessDecorator
    def get_fitness_value(self):
        if self._fitness is not None:
            return self._fitness
        solution = self.chromosome
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
    # usage: pypy schwefel_double_sum_plan_naive.py 2
    # After 157 iterations:
    # mutation_probability=61, size_dependant_mutation_probability=True, mutation_step_factor=0.8386711947606522
    
    sp = RosenbrockPlanNaive()
    inner_ge = GeneticExecutor(sp, debug=False)
    
    ap = ArgsPlan(inner_ge)
    ge = GeneticExecutor(ap, population_size=10, max_generations_number=1000, debug=True)
    solution = ge.get_solution()
    print(solution)
    
    
def run_algorithm():
    iterations_num = 1
    debug = True
    if len(sys.argv) > 1:
        iterations_num = int(sys.argv[1])
        debug = False
        
    sp = RosenbrockPlanNaive()
    ge = GeneticExecutor(sp, debug=debug)
    
    [mean, std] = run_iterations(genetic_executor=ge, iterations_num=iterations_num)
    
    print('==============================')
    print('Mean: ' + str(mean))
    print('STD:  ' + str(std))
    
    
if __name__ == '__main__':
    
    #find_algorithm_parameters()
    
    run_algorithm()
    
    
    
    
    
    
    
    
    
    