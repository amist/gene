import random
import copy
import statistics
import sys
import math
import pickle

class Individual:
    def get_random_chromosome(self):
        chromosome = []
        for _ in range(self.size):
            chromosome.append(random.uniform(self._lower_bound, self._upper_bound))
        return chromosome
    
    
    def get_child(self, parent2, mutation_factor):
        raise NotImplementedError('You have to implemtent a get_child function')
        
        
    def get_fitness_value(self):
        raise NotImplementedError('You have to implemtent a get_fitness_value function')
        
        
    def get_optimal_value(self):
        return None
        
        
    def print_individual(self):
        return
        
        
