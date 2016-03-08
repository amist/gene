from ..core.individual import Individual
import math

class SchwefelSinNaiveIndividual(Individual):
    def __init__(self, size=10, lower_bound=-512.03, upper_bound=511.97):
        super().__init__()
        
        self.size = size
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        
        self.kwargs = {'size': self.size,
                       'lower_bound': self.lower_bound,
                       'upper_bound': self.upper_bound}
        
        
    def calculate_fitness_value(self):
        return -418.9829 * len(self.chromosome) -sum([(g * math.sin(math.sqrt(math.fabs(g)))) for g in self.chromosome])
        