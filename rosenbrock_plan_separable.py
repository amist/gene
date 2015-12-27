import sys
import random
import statistics
from genetic_executor import GeneticExecutor
from genetic_executor import Plan

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
            
            
    def get_child(self, parent2):
        child = RosenbrockPlanSeparable(self.size)
        for i in range(self.size):
            # crossover
            child.chromosome.append(self.chromosome[i] if random.randint(0, 1) == 0 else parent2.chromosome[i])
            
            # mutate
            #print(self._actual_mutation_probability)
            if random.randint(0, int(self._actual_mutation_probability)) == 0:
                rand_val = random.uniform(self._lower_bound, self._upper_bound)
                rand_val = child.chromosome[i] + self._mutation_step_factor * (random.uniform(self._lower_bound, self._upper_bound) - 0.5 * (self._lower_bound + self._upper_bound))
                child.chromosome[i] = rand_val
        return child
        
        
    def get_solution_vector(self):
        solution = [self.chromosome[0]]
        for i in range(len(self.chromosome) - 1):
            #solution.append(self.chromosome[i+1] - self.chromosome[i]**2)
            #solution.append(self.chromosome[i+1] - self.chromosome[i])
            solution.append( self.chromosome[i+1] + ( 200*self.chromosome[i]**2 + self.chromosome[i] - 1 ) / 200 )
        return solution
        
        
    def get_fitness_value(self):
        if self._fitness is not None:
            return self._fitness
        solution = self.get_solution_vector()
        self._fitness = -sum([( 100 * ( solution[i+1] - solution[i]**2 )**2 + ( solution[i] - 1 )**2 ) for i in range(len(solution)-1)])
        return self._fitness
        
        
    def print_plan(self):
        print(self.chromosome)
            
        
    
def run_iterations(population_size=200, max_generations_number=100, mutation_probability=10, size_dependant_mutation_probability=True, mutation_step_factor=0.01, log=True):
    iterations_num = 1
    debug = True
    if len(sys.argv) > 1:
        iterations_num = int(sys.argv[1])
        debug = False
        
    solutions = []

    for _ in range(iterations_num):
        sp = RosenbrockPlanSeparable(size=10, mutation_probability=mutation_probability, size_dependant_mutation_probability=size_dependant_mutation_probability, mutation_step_factor=mutation_step_factor)
        ge = GeneticExecutor(sp, population_size=population_size, max_generations_number=max_generations_number, debug=debug)
        solution = ge.get_solution()
        
        solutions.append(solution.get_fitness_value())
        if log:
            print(solution.get_fitness_value())
        
    if len(solutions) == 1:
        return [solutions[0], 0]
    
    return [statistics.mean(solutions), statistics.stdev(solutions)]
    
    
class ArgsPlan(Plan):
    def __init__(self):
        self.chromosome = []
    
    
    def get_random_chromosome(self):
        # [mutation prbability, size dependant mutation probability, mutation step factor]
        return [random.randint(2, 100), True if random.randint(0,1) == 0 else False, random.uniform(0,1)]
        
        
    def get_child(self, parent2):
        child = ArgsPlan()
        for i in range(3):
            # crossover
            child.chromosome.append(self.chromosome[i] if random.randint(0, 1) == 0 else parent2.chromosome[i])
            
            # mutate
            if random.randint(1, 10 * 3) == 1:
                if i == 0:
                    rand_val = child.chromosome[i] + int(0.1 * (random.randint(2, 100) - 0.5 * (2 + 100)))
                if i == 1:
                    rand_val = True if random.randint(0,1) == 0 else False
                else:
                    rand_val = child.chromosome[i] + 0.1 * (random.uniform(0, 1) - 0.5)
                child.chromosome[i] = rand_val
        return child
        
        
    def get_fitness_value(self):
        [mean, std] = run_iterations(population_size=200, max_generations_number=100, mutation_probability=self.chromosome[0], size_dependant_mutation_probability=self.chromosome[1], mutation_step_factor=self.chromosome[2], log=False)
        return mean
        
        
def find_algorithm_parameters():
    ap = ArgsPlan()
    ge = GeneticExecutor(ap, population_size=10, max_generations_number=1000, debug=True)
    solution = ge.get_solution()
    
    
def run_algorithm():

    #[mean, std] = run_iterations(population_size=200, max_generations_number=100, mutation_probability=10, size_dependant_mutation_probability=True, mutation_step_factor=0.01, log=True)      # original values
    [mean, std] = run_iterations(population_size=200, max_generations_number=100, mutation_probability=61, size_dependant_mutation_probability=True, mutation_step_factor=0.8386711947606522, log=True)      # after 157 iterations of find_algorithm_parameters
    #[mean, std] = run_iterations(population_size=200, max_generations_number=100, mutation_probability=62, size_dependant_mutation_probability=False, mutation_step_factor=0.84, log=True)
    
    print('==============================')
    print('Mean: ' + str(mean))
    print('STD:  ' + str(std))
    
    
if __name__ == '__main__':
    
    #find_algorithm_parameters()
    
    run_algorithm()
    
    
    
    
    
    
    
    
    
    