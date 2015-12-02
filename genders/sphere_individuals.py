import random
from genetic_executor import GeneticExecutor
from genetic_executor import Individual

class SphereIndividual(Individual):
    def __init__(self, size=10, data_chromosome=None, operator_chromosome=None):
        if (data_chromosome is None):
            self.data_chromosome = []
        else:
            self.data_chromosome = data_chromosome
            
        if (operator_chromosome is None):
            self.operator_chromosome = []
        else:
            self.operator_chromosome = operator_chromosome
            
        self.size = size
        self._fitness = None
        self._lower_bound = -5.12
        self._upper_bound = 5.12
        self._operators = [ lambda a,b:a+b,
                            lambda a,b:a-b,
                            lambda a,b:a*b,
                            lambda a,b:a/b if b!=0 else a/(b+1)]
        
        
    def get_random_data_chromosome(self):
        chromosome = []
        for _ in range(self.size):
            chromosome.append(random.uniform(self._lower_bound, self._upper_bound))
        return chromosome
        
        
    def get_random_operator_chromosome(self):
        chromosome = []
        for _ in range(self.size):
            chromosome.append(random.randint(0, len(self._operators)-1))
        return chromosome    
        
        
    def get_fitness_value(self):
        if self._fitness is not None:
            return self._fitness
        self._fitness = -sum([x*x for x in self.data_chromosome])
        return self._fitness
        
        
    def print_solution(self):
        print('{}\n{}'.format(self.data_chromosome, self.operator_chromosome))
        
        
class SphereIndividualA(SphereIndividual):
    def __init__(self, size=10, data_chromosome=None, operator_chromosome=None):
        super().__init__(size=10, data_chromosome=None, operator_chromosome=None)
        
        
    def get_heuristic_value(self, candidate):
        return 0


class SphereIndividualB(SphereIndividual):
    def __init__(self, size=10, data_chromosome=None, operator_chromosome=None):
        super().__init__(size=10, data_chromosome=None, operator_chromosome=None)
        
        
    def get_children(self, parent1):
        child1 = SphereIndividualA(self.size)
        child2 = SphereIndividualB(self.size)
        for i in range(self.size):
            # crossover data
            f = self._operators[self.operator_chromosome[i]]
            child1.data_chromosome.append(f(parent1.data_chromosome[i], self.data_chromosome[i]))
            
            f = self._operators[self.operator_chromosome[i]]
            child2.data_chromosome.append(f(parent1.data_chromosome[i], self.data_chromosome[i]))
            
            # crossover operator - higher probability to be like the same gender parent
            if random.randint(1, 5) == 1:
                child1.operator_chromosome.append(self.operator_chromosome[i])
            else:
                child1.operator_chromosome.append(parent1.operator_chromosome[i])
                
            if random.randint(1, 5) == 1:
                child2.operator_chromosome.append(parent1.operator_chromosome[i])
            else:
                child2.operator_chromosome.append(self.operator_chromosome[i])
            
            # mutate data
            if random.randint(1, 10 * self.size) == 1:
                child1.data_chromosome[i] = random.uniform(self._lower_bound, self._upper_bound)
            if random.randint(1, 10 * self.size) == 1:
                child2.data_chromosome[i] = random.uniform(self._lower_bound, self._upper_bound)    
                
            # mutate operator
            if random.randint(1, 10 * self.size) == 1:
                child1.operator_chromosome[i] = random.randint(0, len(self._operators)-1)
            if random.randint(1, 10 * self.size) == 1:
                child2.operator_chromosome[i] = random.randint(0, len(self._operators)-1)
                
        return child1, child2
        
        
if __name__ == '__main__':
    PROBLEM_SIZE = 10
    sia = SphereIndividualA(size=PROBLEM_SIZE)
    sib = SphereIndividualB(size=PROBLEM_SIZE)
    ge = GeneticExecutor(sia, sib, initial_population_size = 10, max_generations_number = 100)
    solution = ge.get_solution()
    solution.print_solution()