import pickle
from .population import Population

class GeneticExecutor:
    # TODO: add get_run_history (or something similar) alongside get_solution
    # TODO: modularize get_solution for use with get_run_history
    def __init__(self, **kwargs):
        # TODO: set the members statically, then run on kwargs keys
        prop_defaults = {
            'individual_class': None,
            'individual_kwargs': {'size': 10}, 
            'population_size': 200,
            'max_generations_number': 100,
            'debug': False,
            'log_metadata': None,
        }

        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))
            
        if self.individual_class is None:
            raise TypeError("You must pass an individual_class parameter to GeneticExecutor")
            
        # #self.individual_instance = copy.deepcopy(individual_instance)
        # self.individual_kwargs = individual_kwargs
        # self.individual_class = kwargs.get('individual_class')
        # self.population_size = population_size
        # self.max_generations_number = max_generations_number
        # self.debug = debug
        # self.log_metadata = log_metadata
        
        
    def print_debug_info(self, population, i):
        print('Generation %d has been processed' % i)
        print('  Current maximum fitness value = %f' % population.population[0].get_fitness_value())
        print('  Current optimal solution: ' + str(population.population[0].chromosome))
        
    def get_solution(self):
        # TODO: initialize population with config object
        population = Population(individual_class=self.individual_class,
                                individual_kwargs=self.individual_kwargs,
                                population_size=self.population_size,
                                log_metadata=self.log_metadata)
        
        for i in range(self.max_generations_number):
            population.process_generation()
            if self.debug:
                self.print_debug_info(population, i)
            if population.population[0].get_fitness_value() == population.population[0].get_optimal_value():
                if self.debug:
                    print('== Optimal value has been reached! ==')
                break
        if self.debug:
            population.population[0].print_chromosome()
        if self.log_metadata is not None:
            pickle.dump(population.generations_log, open(self.log_metadata.get('log_filename'), 'wb'))
        return population.population[0]
