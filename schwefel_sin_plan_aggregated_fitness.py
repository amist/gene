import sys
import random
import statistics
import math
from genetic_executor import GeneticExecutor
from genetic_executor import Plan
from args_plan import ArgsPlan

'''
This class implements auto separation of variables, in case it's possible.
Each individual keeps a list of aggregated fitness - how much each variable
has contributed to the final fitness value.
The crossover chooses the value which contributed the least to the final
fitness value, between the two parents. This is beneficial only in case
the variables are independent.
This method helps in achieving faster convergence of the population.
'''
class SchwefelSinPlanAggregatedFitness(Plan):
    def __init__(self, size=10, mutation_probability=10, size_dependant_mutation_probability=True, mutation_step_factor=0.01):
        self.chromosome = []
        self.aggregated_fitness = []
        self.size = size
        self._fitness = None
        self._lower_bound = -512.03
        self._upper_bound = 511.97
        
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
        child = SchwefelSinPlanAggregatedFitness(self.size)
        for i in range(self.size):
            # crossover
            if self.aggregated_fitness[i] > parent2.aggregated_fitness[i]:
                child.chromosome.append(self.chromosome[i])
            elif self.aggregated_fitness[i] < parent2.aggregated_fitness[i]:
                child.chromosome.append(parent2.chromosome[i])
            else:
                child.chromosome.append(self.chromosome[i] if random.randint(0, 1) == 0 else parent2.chromosome[i])
            
            # mutate
            #print(self._actual_mutation_probability)
            if random.randint(0, int(self._actual_mutation_probability / (mutation_factor + 1))) == 0:
                rand_val = random.uniform(self._lower_bound, self._upper_bound)
                rand_val = child.chromosome[i] + mutation_factor * self._mutation_step_factor * (random.uniform(self._lower_bound, self._upper_bound) - 0.5 * (self._lower_bound + self._upper_bound))
                if rand_val > self._upper_bound:
                    rand_val = self._upper_bound
                if rand_val < self._lower_bound:
                    rand_val = self._lower_bound
                child.chromosome[i] = rand_val
        return child
        
        
    def get_fitness_value(self):
        if self._fitness is not None:
            return self._fitness
        solution = self.chromosome
        #self._fitness = -418.9829 * len(solution) -sum([(g * math.sin(math.sqrt(math.fabs(g)))) for g in solution])
        self.aggregated_fitness = [(-418.9829 - g * math.sin(math.sqrt(math.fabs(g)))) for g in solution]
        self._fitness = sum(self.aggregated_fitness)
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
    
    sp = SchwefelSinPlanAggregatedFitness()
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
        
    sp = SchwefelSinPlanAggregatedFitness(10)
    ge = GeneticExecutor(sp, population_size = 200, max_generations_number=100, debug=debug)
    
    [mean, std] = run_iterations(genetic_executor=ge, iterations_num=iterations_num)
    
    print('==============================')
    print('Mean: ' + str(mean))
    print('STD:  ' + str(std))
    
    
if __name__ == '__main__':
    
    #find_algorithm_parameters()
    
    run_algorithm()
    
    
    
    
    
    
    
    
    
    