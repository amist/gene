import random

class Individual:
    def __init__(self):
        self.fitness_value = None
        self.chromosome = []
        
        
    def get_random_chromosome(self):
        chromosome = []
        for _ in range(self.size):
            chromosome.append(random.uniform(self.lower_bound, self.upper_bound))
        return chromosome
    
    
    def get_child(self, parent2, mutation_factor=1):
        # TODO: separate into two functions: crossover, mutation
        # TODO: get rid of mutation_factor parameter
        # TODO: define lower_bound, upper_bound, kwargs in __init__ or remove their usage in get_child
        
        child = self.__class__(**self.kwargs)
        for i in range(self.size):
            # crossover
            child.chromosome.append(self.chromosome[i]
                                    if random.randint(0, 1) == 0
                                    else parent2.chromosome[i])
            
            # mutate
            if random.randint(1, int(10 * self.size / (mutation_factor + 1))) == 1:
                child.chromosome[i] = mutation_factor * \
                                      random.uniform(self.lower_bound, self.upper_bound)
        return child
        
        
    def calculate_fitness_value(self):
        raise NotImplementedError('You have to implemtent a calculate_fitness_value function')
        
        
    def get_fitness_value(self):
        if self.fitness_value is not None:
            return self.fitness_value
        self.fitness_value = self.calculate_fitness_value()
        return self.fitness_value
        
        
    def get_optimal_value(self):
        return None
        
        
    def print_chromosome(self):
        print(self.chromosome)
        
        
