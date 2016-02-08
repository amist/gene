import random
from ..core.individual import Individual

class SphereIndividual(Individual):
    def __init__(self, size=10, chromosome=None):
        if chromosome is None:
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
            
            
    def get_child(self, parent2, mutation_factor=1):
        child = SphereIndividual(self.size)
        for i in range(self.size):
            # crossover
            child.chromosome.append(self.chromosome[i]
                                    if random.randint(0, 1) == 0
                                    else parent2.chromosome[i])
            
            # mutate
            if random.randint(1, int(10 * self.size / (mutation_factor + 1))) == 1:
                child.chromosome[i] = mutation_factor * \
                                      random.uniform(self._lower_bound, self._upper_bound)
        return child
        
        
    def get_fitness_value(self):
        if self._fitness is not None:
            return self._fitness
        self._fitness = -sum([x*x for x in self.chromosome])
        return self._fitness
        
        
    def print_plan(self):
        print(self.chromosome)
        