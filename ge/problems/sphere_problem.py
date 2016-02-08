import random
from ..core.individual import Individual

class SphereIndividual(Individual):
    def __init__(self, size=10, lower_bound=-5.12, upper_bound=5.12):
        super().__init__()
        
        self.size = size
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        
        self.kwargs = {'size': self.size,
                       'lower_bound': self.lower_bound,
                       'upper_bound': self.upper_bound}
        
        
    def calculate_fitness_value(self):
        return -sum([x*x for x in self.chromosome])
        