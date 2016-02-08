import sys
import random
import statistics
import math
from genetic_executor import GeneticExecutor
from genetic_executor import Plan
from args_plan import ArgsPlan

class SchwefelSinMutationSelection(Plan):
    def __init__(self, size=10, mutation_probability=10, size_dependant_mutation_probability=True, mutation_step_factor=0.01):
        self.chromosome = []
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
        
        self.mutated_genes = []
        self.pre_mutation_fitness = 0
        
        
    def get_random_chromosome(self):
        chromosome = []
        for _ in range(self.size):
            chromosome.append(random.uniform(self._lower_bound, self._upper_bound))
        return chromosome
            
            
    def get_child(self, parent2, mutation_factor=1):
        child = SchwefelSinMutationSelection(self.size)
        # crossover
        for i in range(self.size):
            if i in self.mutated_genes and i not in parent2.mutated_genes:
                if self.get_fitness_value() > self.pre_mutation_fitness:
                    child.chromosome.append(self.chromosome[i])
                else:
                    child.chromosome.append(parent2.chromosome[i])
            elif i not in self.mutated_genes and i in parent2.mutated_genes:
                if parent2.get_fitness_value() > parent2.pre_mutation_fitness:
                    child.chromosome.append(parent2.chromosome[i])
                else:
                    child.chromosome.append(self.chromosome[i])
            elif i in self.mutated_genes and i in parent2.mutated_genes:
                if self.get_fitness_value() - self.pre_mutation_fitness > parent2.get_fitness_value() - parent2.pre_mutation_fitness:
                    child.chromosome.append(self.chromosome[i])
                else:
                    child.chromosome.append(parent2.chromosome[i])
            else:
                child.chromosome.append(self.chromosome[i] if random.randint(0, 1) == 0 else parent2.chromosome[i])
            
        # mutate
        child.pre_mutation_fitness = child.get_fitness_value()
        child._fitness = None
        child.mutated_genes = []
        for i in range(self.size):
            if random.randint(0, int(self._actual_mutation_probability / (mutation_factor + 1))) == 0:
                child.mutated_genes.append(i)
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
        self._fitness = -418.9829 * len(solution) -sum([(g * math.sin(math.sqrt(math.fabs(g)))) for g in solution])
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
    
    sp = SchwefelSinMutationSelection()
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
        
    sp = SchwefelSinMutationSelection(50)
    ge = GeneticExecutor(sp, population_size = 200, max_generations_number=100, debug=debug)
    
    [mean, std] = run_iterations(genetic_executor=ge, iterations_num=iterations_num)
    
    print('==============================')
    print('Mean: ' + str(mean))
    print('STD:  ' + str(std))
    
    
if __name__ == '__main__':
    
    #find_algorithm_parameters()
    
    run_algorithm()
    
    
    
    
    
    
    
    
    
    