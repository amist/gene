import random
import copy
import statistics
import sys
import math
import pickle

class Population:
    def __init__(self, individual, size=200, expansion_factor=5, log_metadata=False):
        self.population = []
        self.size = size
        self.expansion_factor = expansion_factor
        fitness_values = []
        
        self.log_metadata = log_metadata
        self.individuals_id = 0
        self.generations_log = []
        
        for _ in range(self.size):
            plan = copy.deepcopy(individual)
            plan.chromosome = plan.get_random_chromosome()
            if self.log_metadata:
                plan.id = self.get_id()
                plan.parent1_id = -1
                plan.parent2_id = -1
            self.population.append(plan)
            fitness_values.append(plan.get_fitness_value())
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
        
        
    def get_individual_with_uniform_choice(self):
        return self.population[random.randint(0, len(self.population) - 1)]
        
        
    def get_individual_with_moving_window(self, percentage):
        window_size = self.size / 10
        lower_bound = int(percentage * (self.size - window_size))
        upper_bound = int(window_size + percentage * (self.size - window_size - 1))
        if upper_bound - 1 > lower_bound:
            upper_bound = upper_bound - 1
        #print(percentage, lower_bound, upper_bound)
        return self.population[random.randint(lower_bound, upper_bound)]
        
        
    def get_individual_with_weighted_choice(self):
        choices = self.population
        f_values = [c.get_fitness_value() for c in choices]
        
        # factor - ensure the minimum value is 1 (especially to avoid negative values)
        factor = -min(f_values) + 1
        total = sum(f_values) + factor * len(f_values)
        #print 'total =', total
        rand_number = random.uniform(0, total)
        upto = 0
        for choice in choices:
            #print 'upto =', upto
            f = choice.get_fitness_value() + factor
            if upto + f > rand_number:
                return choice
            upto += f
        assert False, "In get_individual_with_weighted_choice. Shouldn't get here"
        
        
    def process_generation(self):
        self.expand_population()
        self.sort_population()
        if self.log_metadata:
            self.generations_log.append(self.get_population_log())
        #self._distinct_population()
        self.cut_population()
        #self.population[0].print_plan()
        
        
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
        for iter_num in range(self.size * (self.expansion_factor - 1)):
            #parent1 = self.get_individual_with_uniform_choice()
            #parent2 = self.get_individual_with_uniform_choice()
            parent1 = self.get_individual_with_moving_window(iter_num / (self.size * (self.expansion_factor - 1)))
            parent2 = self.get_individual_with_moving_window(iter_num / (self.size * (self.expansion_factor - 1)))
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
        self.population = self.population[0:self.size - 1]
            
            
class Plan:
    def get_random_chromosome(self):
        raise NotImplementedError('You have to implemtent a get_random_chromosome function')
    
    
    def get_child(self, parent2, mutation_factor):
        raise NotImplementedError('You have to implemtent a get_child function')
        
        
    def get_fitness_value(self):
        raise NotImplementedError('You have to implemtent a get_fitness_value function')
        
        
    def get_optimal_value(self):
        return None
        
        
    def print_plan(self):
        return
        
        
def FitnessDecorator(func):
    def inner(individual):
        try:
            #print('in inner ' + str(individual.chromosome) + ' ' + str(func(individual)))
            #a = func(individual)
            
            if math.isnan(func(individual)):
                return -int(sys.float_info.max / 10)
            return func(individual)
        except OverflowError:
            return -int(sys.float_info.max / 10)
    return inner

        
class GeneticExecutor:

    def __init__(self, individual_instance, population_size=200,
                 max_generations_number=100, debug=False, log_metadata=False):
        self.individual_instance = copy.deepcopy(individual_instance)
        self.population_size = population_size
        self.max_generations_number = max_generations_number
        self.debug = debug
        self.log_metadata = log_metadata
        
        
    def print_debug_info(self, population, i):
        print('Generation %d has been processed' % i)
        print('  Current maximum fitness value = %f' % population.population[0].get_fitness_value())
        print('  Current optimal solution: ' + str(population.population[0].chromosome))
        
    def get_solution(self):
        population = Population(individual=self.individual_instance,
                                size=self.population_size, log_metadata=self.log_metadata)
        
        for i in range(self.max_generations_number):
            population.process_generation()
            if self.debug:
                self.print_debug_info(population, i)
            if population.population[0].get_fitness_value() == population.population[0].get_optimal_value():
                if self.debug:
                    print('== Optimal value has been reached! ==')
                break
        if self.debug:
            population.population[0].print_plan()
        if self.log_metadata:
            pickle.dump(population.generations_log, open('generations_data.p', 'wb'))
        return population.population[0]
