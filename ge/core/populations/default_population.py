import random
import math
import statistics
import sys
from ..population import Population

class DefaultPopulation(Population):
    def __init__(self, **kwargs):
        # TODO: set the members statically, then run on kwargs keys
        prop_defaults = {
            'individual_class': None,
            'individual_kwargs': {'size': 10}, 
            'population_size': 200,
            'expansion_factor': 5,
            'log_metadata': {'log_filename': 'generations_data.p'},
            'mutation_a_b': True,
        }

        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))
            
        if self.individual_class is None:
            raise TypeError("You must pass an individual_class parameter to Population")
        
        self.population = []
        fitness_values = []
        
        self.individuals_id = 0
        # TODO: rename generations_log
        self.generations_log = []
        
        for _ in range(self.population_size):
            individual = self.individual_class(**self.individual_kwargs)
            individual.chromosome = individual.get_random_chromosome()
            if self.log_metadata is not None:
                # TODO: get unique id from Individual (maybe with id(self) - consider range limitation)
                individual.id = self.get_id()
                # TODO: set parents' ids into list (for variable number of parents)
                individual.parent1_id = -1
                individual.parent2_id = -1
            if self.mutation_a_b:
                individual.tag = 0
            self.population.append(individual)
            fitness_values.append(individual.get_fitness_value())
        # TODO: choose convergence checking method dynamically
        try:
            self.initial_population_std = statistics.stdev(fitness_values)
        except OverflowError:
            self.initial_population_std = int(sys.float_info.max / 10)
            
        if self.log_metadata is not None:
            self.generations_log.append(self.get_population_log())
            
        if self.mutation_a_b:
            init_mutation_prob = self.individual_kwargs['size']
            self.mutation_params_list = [{'mutation_prob_factor': init_mutation_prob, 'mutation_amp_factor': 1},
                                         {'mutation_prob_factor': 2 * init_mutation_prob, 'mutation_amp_factor': 1}]
                                         
        self.generation_number = 0
        
        
    def get_id(self):
        self.individuals_id += 1
        return self.individuals_id - 1
        
        
    def get_population_log(self):
        return [(individual.id, 
                 individual.parent1_id, 
                 individual.parent2_id, 
                 individual.get_fitness_value()) for individual in self.population]
        
        
    def get_individual_uniform_choice(self):
        return self.population[random.randint(0, len(self.population) - 1)]
        
        
    def get_individual_moving_window(self, percentage):
        window_size = self.population_size / 10
        lower_bound = int(percentage * (self.population_size - window_size))
        upper_bound = int(window_size + percentage * (self.population_size - window_size - 1))
        if upper_bound - 1 > lower_bound:
            upper_bound = upper_bound - 1
        #print(percentage, lower_bound, upper_bound)
        return self.population[random.randint(lower_bound, upper_bound)]
        
        
    # def get_individual_weighted_choice(self):
        # choices = self.population
        # f_values = [c.get_fitness_value() for c in choices]
        
        # # factor - ensure the minimum value is 1 (especially to avoid negative values)
        # factor = -min(f_values) + 1
        # total = sum(f_values) + factor * len(f_values)
        # #print 'total =', total
        # rand_number = random.uniform(0, total)
        # upto = 0
        # for choice in choices:
            # #print 'upto =', upto
            # f = choice.get_fitness_value() + factor
            # if upto + f > rand_number:
                # return choice
            # upto += f
        # assert False, "In get_individual_with_weighted_choice. Shouldn't get here"
        
        
    def assess_a_b(self):
        a_survivors = sum([1 for individual in self.population[:max(6, int(len(self.population)/10))] if individual.tag == 0])
        b_survivors = sum([1 for individual in self.population[:max(6, int(len(self.population)/10))] if individual.tag == 1])
        # print(self.population[0].get_fitness_value())
        # print('{} - {} ({} - {})'.format(a_survivors, b_survivors, self.mutation_params_list[0]['mutation_prob_factor'], self.mutation_params_list[1]['mutation_prob_factor']))
        # TODO: check difference in STD
        # TODO: handle integer/float overflow
        if self.mutation_params_list[0]['mutation_prob_factor'] > 1e-50 and self.mutation_params_list[1]['mutation_prob_factor'] > 1e-50:
            if a_survivors > 1.1 * b_survivors:
                self.mutation_params_list[1]['mutation_prob_factor'] *= (self.mutation_params_list[0]['mutation_prob_factor'] / (self.mutation_params_list[1]['mutation_prob_factor'])) ** (self.generation_number / 20)
            if b_survivors > 1.1 * a_survivors:
                self.mutation_params_list[0]['mutation_prob_factor'] *= (self.mutation_params_list[1]['mutation_prob_factor'] / (self.mutation_params_list[0]['mutation_prob_factor'])) ** (self.generation_number / 20)
        
        
    def process_generation(self):
        self.generation_number += 1
        self.expand_population()
        self.sort_population()
        if self.log_metadata is not None:
            self.generations_log.append(self.get_population_log())
        self.cut_population()
        if self.mutation_a_b:
            self.assess_a_b()
        
        
    def expand_population(self):
        #print("========================")
        try:
            cur_population_std = statistics.stdev([individual.get_fitness_value()
                                                   for individual in self.population])
        except OverflowError:
            cur_population_std = int(sys.float_info.max / 10)
        #mean_genes = [statistics.mean(individual.chromosome[i]
        #                              for individual in self.population)
        #              for i in range(self.population[0].size)]
        #std_genes = [statistics.stdev(individual.chromosome[i]
        #                              for individual in self.population)
        #             for i in range(self.population[0].size)]
        #print(std_genes)
        for iter_num in range(self.population_size * (self.expansion_factor - 1)):
            #parent1 = self.get_individual_with_uniform_choice()
            #parent2 = self.get_individual_with_uniform_choice()
            window_percentage = iter_num / (self.population_size * (self.expansion_factor - 1))
            # TODO: choose dynamically the parents choosing method
            parent1 = self.get_individual_moving_window(window_percentage)
            parent2 = self.get_individual_moving_window(window_percentage)
            mutation_params = {'mutation_prob_factor': self.mutation_params_list[0]['mutation_prob_factor'],
                               'mutation_amp_factor': math.sqrt(cur_population_std / (self.initial_population_std + 1))}
            child = parent1.get_child(parent2, mutation_params)
            # TODO: extract into tag_child function
            if self.log_metadata is not None:
                child.id = self.get_id()
                child.parent1_id = parent1.id
                child.parent2_id = parent2.id
            if self.mutation_a_b:
                child.tag = 0
            self.population.append(child)
            
            # mutation_params = {'mutation_prob_factor': cur_population_std / (self.initial_population_std + 1),
                               # 'mutation_amp_factor': cur_population_std / (self.initial_population_std + 1)}
            mutation_params = {'mutation_prob_factor': self.mutation_params_list[1]['mutation_prob_factor'],
                               'mutation_amp_factor': cur_population_std / (self.initial_population_std + 1)}
            # mutation_params = self.mutation_params_list[1]
            child = parent1.get_child(parent2, mutation_params)
            #child = parent1.get_child(parent2, mean_genes, std_genes)
            if self.log_metadata is not None:
                child.id = self.get_id()
                child.parent1_id = parent1.id
                child.parent2_id = parent2.id
            if self.mutation_a_b:
                child.tag = 1
            self.population.append(child)
            
            
