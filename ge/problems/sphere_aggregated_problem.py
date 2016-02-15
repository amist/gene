from ..core.individual import Individual

class SphereAggregatedIndividual(Individual):
    def __init__(self, size=10, lower_bound=-5.12, upper_bound=5.12):
        super().__init__()
        
        self.size = size
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        
        self.kwargs = {'size': self.size,
                       'lower_bound': self.lower_bound,
                       'upper_bound': self.upper_bound}
        
        self.aggregated_fitness = []
        
        
    def get_crossover_list(self, parent2):
        return [0 if self.aggregated_fitness[i] > parent2.aggregated_fitness[i] else 1 for i in range(self.size)]
        
        
    def calculate_fitness_value(self):
        self.aggregated_fitness = [-x*x for x in self.chromosome]
        return -sum([x*x for x in self.chromosome])
        