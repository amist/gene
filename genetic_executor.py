#from random import randint
import random
import copy
import multiprocessing
import statistics
import sys
import math
import pickle

class Population:
    def __init__(self, individual, size=200, expansion_factor=5, log_metadata=False):
        
        self.population = []
        self.size = size
        self.expansion_factor = expansion_factor
        self.coindividuals_num = 100
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
        return [(individual.id, individual.parent1_id, individual.parent2_id, individual.get_fitness_value()) for individual in self.population]
        
        
    def _get_individual_with_uniform_choice(self):
        return self.population[random.randint(0, len(self.population) - 1)]
        
        
    def _get_individual_with_moving_window(self, percentage):
        window_size = self.size / 10
        lb = int(percentage * (self.size - window_size))
        ub = int(window_size + percentage * (self.size - window_size - 1))
        if ub - 1 > lb:
            ub = ub - 1
        #print(percentage, lb, ub)
        return self.population[random.randint(lb, ub)]
        
        
    def _get_coindividual_with_uniform_choice(self, parent1):
        parent2 = None
        max_fitness = None
        for _ in range(self.coindividuals_num):
            other = self.population[random.randint(0, len(self.population) - 1)]
            if max_fitness is None or max_fitness < parent1.get_cofitness_value(other):
                parent2 = other
                max_fitness = parent1.get_cofitness_value(other)
        return parent2
        
        
    def _get_individual_with_weighted_choice(self):
        choices = self.population
        f_values = [c.get_fitness_value() for c in choices]
        
        # factor - ensure the minimum value is 1 (especially to avoid negative values)
        factor = -min(f_values) + 1
        total = sum(f_values) + factor * len(f_values)
        #print 'total =', total
        r = random.uniform(0, total)
        upto = 0
        for c in choices:
            #print 'upto =', upto
            f = c.get_fitness_value() + factor
            if upto + f > r:
                return c
            upto += f
        assert False, "In _get_individual_with_weighted_choice. Shouldn't get here"
        
        
    def _calculate_fitness_concurrently(self, individual, i, res_dict):
        res_dict[i] = individual.get_fitness_value()
        
        
    def _calculate_fintesses(self):
        manager = multiprocessing.Manager()
        res_dict = manager.dict()
        jobs = []
        for i in range(len(self.population)):
            p = multiprocessing.Process(target=self._calculate_fitness_concurrently(self.population[i], i, res_dict))
            jobs.append(p)
            p.start()
        for job in jobs:
            job.join()
        for i in range(len(self.population)):
            self.population[i]._fitness = res_dict[i]
        
        
    def process_generation(self):
        self._expand_population()
#         self._calculate_fintesses()
        self._sort_population()
        if self.log_metadata:
            self.generations_log.append(self.get_population_log())
        #self._distinct_population()
        self._cut_population()
        #self.population[0].print_plan()
        
        
    def _expand_population(self):
        #print("========================")
        try:
            cur_population_std = statistics.stdev([individual.get_fitness_value() for individual in self.population])
        except OverflowError:
            cur_population_std = int(sys.float_info.max / 10)
        for iter_num in range(self.size * (self.expansion_factor - 1)):
            #parent1 = self._get_individual_with_uniform_choice()
            #parent2 = self._get_individual_with_uniform_choice()
            parent1 = self._get_individual_with_moving_window(iter_num / (self.size * (self.expansion_factor - 1)))
            parent2 = self._get_individual_with_moving_window(iter_num / (self.size * (self.expansion_factor - 1)))
            child = parent1.get_child(parent2)
            if self.log_metadata:
                child.id = self.get_id()
                child.parent1_id = parent1.id
                child.parent2_id = parent2.id
            self.population.append(child)
            
            child = parent1.get_child(parent2, cur_population_std / (self.initial_population_std + 1))
            if self.log_metadata:
                child.id = self.get_id()
                child.parent1_id = parent1.id
                child.parent2_id = parent2.id
            self.population.append(child)
            #self.population.append(self._get_individual_with_weighted_choice().get_child(self._get_individual_with_weighted_choice()))
        
        
    def _sort_population(self):
        self.population.sort(key=lambda x: -x.get_fitness_value())
        
        
    def _distinct_population(self):
        raise NotImplementedError
        
        
    def _cut_population(self):
        self.population = self.population[0:self.size - 1]
            
            
class Plan:
    def get_random_chromosome(self):
        raise NotImplementedError('You have to implemtent a get_random_chromosome function')
    
    
    def get_child(self, parent2):
        raise NotImplementedError('You have to implemtent a get_child function')
        
        
    def get_fitness_value(self):
        raise NotImplementedError('You have to implemtent a get_fitness_value function')
        
        
    def get_optimal_value(self):
        return None
        
        
    def print_plan(self):
        return
        
        
def FitnessDecorator(f):
    def inner(individual):
        try:
            #print('in inner ' + str(individual.chromosome) + ' ' + str(f(individual)))
            #a = f(individual)
            
            if math.isnan(f(individual)):
                return -int(sys.float_info.max / 10)
            return f(individual)
        except OverflowError:
            return -int(sys.float_info.max / 10)
    return inner

        
class GeneticExecutor:

    def __init__(self, individual_instance, population_size=200, max_generations_number=100, debug=False, log_metadata=False):
        self.individual_instance = copy.deepcopy(individual_instance)
        self.population_size = population_size
        self.max_generations_number = max_generations_number
        self.debug = debug
        self.log_metadata = log_metadata
        
        
    def get_solution(self):
        population = Population(individual=self.individual_instance, size=self.population_size, log_metadata=self.log_metadata)
        
        for i in range(self.max_generations_number):
            if self.debug:
                print('Processing generation %d' % i)
            population.process_generation()
            if self.debug:
                print('  Current maximum fitness value = %f' % population.population[0].get_fitness_value())
                print('  Current optimal solution: ' + str(population.population[0].chromosome))
                #print('  Current aggregated fitness' + str(population.population[0].aggregated_fitness))
            if (population.population[0].get_fitness_value() == population.population[0].get_optimal_value()):
                break;
        if self.debug:
            population.population[0].print_plan()
        if self.log_metadata:
            pickle.dump(population.generations_log, open('generations_data.p', 'wb'))
        return population.population[0]
