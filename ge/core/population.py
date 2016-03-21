import random
import math
import statistics
import sys

class Population:
    def __init__(self, **kwargs):
        # TODO: set the members statically, then run on kwargs keys
        prop_defaults = {
            'individual_class': None,
            'individual_kwargs': {'size': 10}, 
            'population_size': 200,
            'expansion_factor': 5,
        }

        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))
            
        if self.individual_class is None:
            raise TypeError("You must pass an individual_class parameter to Population")
        
        self.population = []
        
        # TODO: rename generations_log
        self.generations_log = []
        
        for _ in range(self.population_size):
            individual = self.individual_class(**self.individual_kwargs)
            individual.chromosome = individual.get_random_chromosome()
            self.population.append(individual)
            
        self.generations_log.append(self.get_population_log())
        
        
    def get_population_log(self):
        return [(-1, -1, -1, individual.get_fitness_value()) for individual in self.population]
        
        
    def get_individual(self, iter_num):
        return self.get_individual_uniform_choice()
        
        
    def get_individual_uniform_choice(self):
        return self.population[random.randint(0, len(self.population) - 1)]
        
        
    def process_generation(self):
        self.expand_population()
        self.mutate_population()
        self.sort_population()
        self.generations_log.append(self.get_population_log())
        self.cut_population()
        
        
    def expand_population(self):
        for iter_num in range(self.population_size * (self.expansion_factor - 1)):
        
            window_percentage = iter_num / (self.population_size * (self.expansion_factor - 1))
            
            # parent1 = self.get_individual_moving_window(window_percentage)
            # parent2 = self.get_individual_moving_window(window_percentage)
            parent1 = self.get_individual(iter_num)
            parent2 = self.get_individual(iter_num)
            
            child = parent1.get_child(parent2)
            self.population.append(child)
            
            
    def mutate_population(self):
        # TODO: pythonize this
        
        mutation_params = {'mutation_prob_factor': self.individual_kwargs['size'], 'mutation_amp_factor': 0.01}
        # mutate only the new individuals
        for i in range(self.population_size, self.population_size * (self.expansion_factor - 1)):
            for j in range(self.individual_kwargs['size']):
                # mutate
                if random.randint(0, int(1 * self.individual_kwargs['size'] / (mutation_params['mutation_prob_factor'] + 1))) == 0:
                    delta = (mutation_params['mutation_amp_factor']) * random.uniform(self.population[i].lower_bound, self.population[i].upper_bound)
                    self.population[i].chromosome[j] += delta
                    # print('delta was {}'.format(delta))
                    if self.population[i].chromosome[j] > self.population[i].upper_bound:
                        self.population[i].chromosome[j] = self.population[i].upper_bound
                    if self.population[i].chromosome[j] < self.population[i].lower_bound:
                        self.population[i].chromosome[j] = self.population[i].lower_bound
        
    
    def sort_population(self):
        self.population.sort(key=lambda x: -x.get_fitness_value())
        
        
    def cut_population(self):
        self.population = self.population[0:self.population_size - 1]
            
            
