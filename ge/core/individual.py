import random
import copy
import statistics
import sys
import math
import pickle

class Individual:
    def __init__(self):
        self._fitness = None
        self.chromosome = []
        
        
    def get_random_chromosome(self):
        chromosome = []
        for _ in range(self.size):
            chromosome.append(random.uniform(self.lower_bound, self.upper_bound))
        return chromosome
    
    
    def get_child(self, parent2, mutation_factor=1):
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
        if self._fitness is not None:
            return self._fitness
        self._fitness = self.calculate_fitness_value()
        return self._fitness
        
        
    def get_optimal_value(self):
        return None
        
        
    def print_chromosome(self):
        print(self.chromosome)
        
        
