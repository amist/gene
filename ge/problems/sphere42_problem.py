from ..core.individual import Individual
import random

class Sphere42Individual(Individual):
    average_gene = []
    
    def __init__(self, size=10, lower_bound=42-5.12, upper_bound=42+5.12):
        super().__init__()
        
        self.size = size
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        
        self.kwargs = {'size': self.size,
                       'lower_bound': self.lower_bound,
                       'upper_bound': self.upper_bound}
        
        
    def calculate_fitness_value(self):
        # TODO: update bounds.
        # need to decide how the gene will represent the distance from the average and yet somehow to remember that the goal is to reach 42
        
        # quick and ugly
        # if len(Sphere42Individual.average_gene) < self.size:
            # return -sum([(42-x)*(42-x) for x in self.chromosome])
        vals = []
        for i in range(self.size):
            vals.append(float(Sphere42Individual.average_gene[i]) + float(self.chromosome[i]))
        return -sum([(42-x)*(42-x) for x in vals])
        # return -sum([(42-x)*(42-x) for x in self.chromosome])
        
        
    def get_child(self, parent2, mutation_factor=1):
        child = self.__class__(**self.kwargs)
        
        # crossover
        crossover_list = self.get_crossover_list(parent2)
        both_chromosomes = [self.chromosome, parent2.chromosome]
        child.chromosome = [both_chromosomes[crossover_list[i]][i] for i in range(self.size)]
        for i in range(self.size):
            child.chromosome[i] -= Sphere42Individual.average_gene[i]
        
        for i in range(self.size):
            # mutate
            if random.randint(1, int(10 * self.size / (mutation_factor + 1))) == 1:
                child.chromosome[i] = mutation_factor * \
                                      random.uniform(self.lower_bound, self.upper_bound)
        return child
        