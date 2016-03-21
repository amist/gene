import random
import math
import statistics
import sys
from ..population import Population

class MediumPopulation(Population):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        
    def get_individual(self, iter_num):
        window_percentage = iter_num / (self.population_size * (self.expansion_factor - 1))
        return self.get_individual_moving_window(window_percentage)
        
        
    def get_individual_moving_window(self, percentage):
        window_size = self.population_size / 10
        lower_bound = int(percentage * (self.population_size - window_size))
        upper_bound = int(window_size + percentage * (self.population_size - window_size - 1))
        if upper_bound - 1 > lower_bound:
            upper_bound = upper_bound - 1
        #print(percentage, lower_bound, upper_bound)
        return self.population[random.randint(lower_bound, upper_bound)]
        