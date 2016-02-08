import pickle
from .population import Population

class GeneticExecutor:

    def __init__(self, individual_class, individual_kwargs=None, population_size=200,
                 max_generations_number=100, debug=False, log_metadata=False):
        #self.individual_instance = copy.deepcopy(individual_instance)
        self.individual_kwargs = individual_kwargs
        self.individual_class = individual_class
        self.population_size = population_size
        self.max_generations_number = max_generations_number
        self.debug = debug
        self.log_metadata = log_metadata
        
        
    def print_debug_info(self, population, i):
        print('Generation %d has been processed' % i)
        print('  Current maximum fitness value = %f' % population.population[0].get_fitness_value())
        print('  Current optimal solution: ' + str(population.population[0].chromosome))
        
    def get_solution(self):
        population = Population(individual_class=self.individual_class,
                                individual_kwargs=self.individual_kwargs,
                                size=self.population_size,
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
        if self.log_metadata:
            pickle.dump(population.generations_log, open('generations_data.p', 'wb'))
        return population.population[0]
