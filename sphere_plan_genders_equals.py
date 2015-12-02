import random
from genetic_executor import GeneticExecutor
from genetic_executor import Plan

class SpherePlan(Plan):
    def __init__(self, size = 10, chromosome = None):
        if (chromosome is None):
            self.chromosome = []
        else:
            self.chromosome = chromosome
        self.size = size
        self._fitness = None
        self._lower_bound = -5.12
        self._upper_bound = 5.12
        
        
    def get_random_chromosome(self):
        chromosome = []
        for _ in range(self.size):
            chromosome.append(random.uniform(self._lower_bound, self._upper_bound))
        return chromosome
            
            
    def get_child(self, parent2):
        child = SpherePlan(self.size)
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
        self._fitness = -sum([x*x for x in self.chromosome])
        return self._fitness
        
        
    def get_cofitness_value(self, other):
        return -sum([x*y for x,y in zip(self.chromosome, other.chromosome)])
        
        
    def print_plan(self):
        print(self.chromosome)
            
        
        
if __name__ == '__main__':
    sp = SpherePlan(10)
    ge = GeneticExecutor(sp, initial_population_size = 10, max_generations_number = 100, genders='equals')
    solution = ge.get_solution()
    solution.print_plan()