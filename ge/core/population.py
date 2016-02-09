import random
import statistics
import sys

class Population:
    def __init__(self, **kwargs):         
        prop_defaults = {
            'individual_class': None,
            'individual_kwargs': {'size': 10}, 
            'population_size': 200,
            'expansion_factor': 5,
            'log_metadata': False,
        }

        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))
            
        if self.individual_class is None:
            raise TypeError("You must pass an individual_class parameter to Population")
        
        self.population = []
        fitness_values = []
        
        self.individuals_id = 0
        self.generations_log = []
        
        for _ in range(self.population_size):
            individual = self.individual_class(**self.individual_kwargs)
            individual.chromosome = individual.get_random_chromosome()
            if self.log_metadata:
                individual.id = self.get_id()
                individual.parent1_id = -1
                individual.parent2_id = -1
            self.population.append(individual)
            fitness_values.append(individual.get_fitness_value())
        try:
            self.initial_population_std = statistics.stdev(fitness_values)
        except OverflowError:
            self.initial_population_std = int(sys.float_info.max / 10)
            
        if self.log_metadata:
            self.generations_log.append(self.get_population_log())
        
        
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
        
        
    def process_generation(self):
        self.expand_population()
        self.sort_population()
        if self.log_metadata:
            self.generations_log.append(self.get_population_log())
        self.cut_population()
        
        
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
            parent1 = self.get_individual_moving_window(window_percentage)
            parent2 = self.get_individual_moving_window(window_percentage)
            child = parent1.get_child(parent2)
            if self.log_metadata:
                child.id = self.get_id()
                child.parent1_id = parent1.id
                child.parent2_id = parent2.id
            self.population.append(child)
            
            child = parent1.get_child(parent2,
                                      cur_population_std / (self.initial_population_std + 1))
            #child = parent1.get_child(parent2, mean_genes, std_genes)
            if self.log_metadata:
                child.id = self.get_id()
                child.parent1_id = parent1.id
                child.parent2_id = parent2.id
            self.population.append(child)
        
        
    def sort_population(self):
        self.population.sort(key=lambda x: -x.get_fitness_value())
        
        
    def cut_population(self):
        self.population = self.population[0:self.population_size - 1]
            
            
