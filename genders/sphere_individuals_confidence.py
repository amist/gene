# Each individual has two chromosomes:
# The first chromosome is the data itself - the solution.
# The second chromosome a confidence level (between 0 and 1): how confident this individual is that this particular value is in its maximum point

import random
from genetic_executor_2 import GeneticExecutor
from genetic_executor_2 import Individual

class SphereIndividual(Individual):
    def __init__(self, size=10, data_chromosome=None, confidence_chromosome=None):
        if (data_chromosome is None):
            self.data_chromosome = []
        else:
            self.data_chromosome = data_chromosome
            
        if (confidence_chromosome is None):
            self.confidence_chromosome = []
        else:
            self.confidence_chromosome = confidence_chromosome
            
        self.size = size
        self._fitness = None
        self._lower_bound = -5.12
        self._upper_bound = 5.12
        
        
    def _get_random_data_chromosome(self):
        chromosome = []
        for _ in range(self.size):
            chromosome.append(random.uniform(self._lower_bound, self._upper_bound))
        return chromosome
        
        
    def _get_random_confidence_chromosome(self):
        chromosome = []
        for _ in range(self.size):
            chromosome.append(random.uniform(0, 1))
        return chromosome    
        
    
    def set_to_random(self):
        self.data_chromosome = self._get_random_data_chromosome()
        self.confidence_chromosome = self._get_random_confidence_chromosome()
        
        
    def get_fitness_value(self):
        if self._fitness is not None:
            return self._fitness
        #self._fitness = -sum([x*x for x in self.data_chromosome])   # optimal at [0, 0, 0, ...]
        #self._fitness = -sum([(1-x)*(1-x) for x in self.data_chromosome])   # optimal at [1, 1, 1, ...]
        self._fitness = -sum([(2-x)*(2-x) for x in self.data_chromosome])   # optimal at [2, 2, 2, ...]
        return self._fitness
        
        
    def print_solution(self):
        print('{}\n{}'.format(self.data_chromosome, self.confidence_chromosome))
        
        
class SphereIndividualA(SphereIndividual):
    def __init__(self, size=10, data_chromosome=None, confidence_chromosome=None):
        super().__init__(size=10, data_chromosome=None, confidence_chromosome=None)
        
        
    def get_heuristic_value(self, candidate):
        estimated_data = []
        for i in range(self.size):
            new_gene = self.data_chromosome[i] * self.confidence_chromosome[i] + candidate.data_chromosome[i] * candidate.confidence_chromosome[i]
            estimated_data.append(new_gene)
        return -sum([(2-x)*(2-x) for x in estimated_data])   # optimal at [2, 2, 2, ...]


class SphereIndividualB(SphereIndividual):
    def __init__(self, size=10, data_chromosome=None, confidence_chromosome=None):
        super().__init__(size=10, data_chromosome=None, confidence_chromosome=None)
        
        
    def get_children(self, parent1):
        num_of_children = 5
        children = []
        for j in range(num_of_children):
            type = random.randint(0, 1)
            if type == 0:
                child = SphereIndividualA(self.size)
            else:
                child = SphereIndividualB(self.size)
            for i in range(self.size):
                # crossover data
                child.data_chromosome.append(parent1.data_chromosome[i] * parent1.confidence_chromosome[i] + self.data_chromosome[i] * self.confidence_chromosome[i])
                
                # crossover confidence
                child.confidence_chromosome.append(0.5 * parent1.confidence_chromosome[i] + 0.5 * self.confidence_chromosome[i])
                
                # mutate data
                if random.randint(1, 10 * self.size) == 1:
                    child.data_chromosome[i] = random.uniform(self._lower_bound, self._upper_bound)
                    
                # mutate confidence
                if random.randint(1, 10 * self.size) == 1:
                    child.confidence_chromosome[i] = random.uniform(0, 1)
                
        return children
        
        
if __name__ == '__main__':
    PROBLEM_SIZE = 10
    sia = SphereIndividualA(size=PROBLEM_SIZE)
    sib = SphereIndividualB(size=PROBLEM_SIZE)
    ge = GeneticExecutor(sia, sib, initial_population_size = 10, max_generations_number = 100)
    solution = ge.get_solution()
    solution.print_solution()
    print(solution.get_fitness_value())