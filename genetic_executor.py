#from random import randint
import random
import copy
import multiprocessing

class Population:
    def __init__(self, size=200, expansion_factor=5, genders='no'):
        self.population = []
        self.size = size
        self.expansion_factor = expansion_factor
        self.genders = genders
        self.coindividuals_num = 100
        
    def _get_individual_with_uniform_choice(self):
        return self.population[random.randint(0, len(self.population) - 1)]
        
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
        
    def add_individual(self, individual):
        self.population.append(individual)
        
    def process_generation(self):
        self._expand_population()
#         self._calculate_fintesses()
        self._sort_population()
        #self._distinct_population()
        self._cut_population()
        #self.population[0].print_plan()
        
    def _expand_population(self):
        if self.genders == 'no':
            for _ in range(self.size * (self.expansion_factor - 1)):
                parent1 = self._get_individual_with_uniform_choice()
                parent2 = self._get_individual_with_uniform_choice()
                child = parent1.get_child(parent2)
                self.population.append(child)
                #self.population.append(self._get_individual_with_weighted_choice().get_child(self._get_individual_with_weighted_choice()))
        if self.genders == 'equals':
            for _ in range(self.size * (self.expansion_factor - 1)):
                parent1 = self._get_individual_with_uniform_choice()
                parent2 = self._get_coindividual_with_uniform_choice(parent1)
                child = parent1.get_child(parent2)
                self.population.append(child)
        
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

class GeneticExecutor:

    def __init__(self, individual_instance, initial_population_size=10, max_generations_number=100, genders='no'):
        self.individual_instance = copy.deepcopy(individual_instance)
        self.initial_population_size = initial_population_size
        self.max_generations_number = max_generations_number
        self.genders = genders
        
    def get_solution(self):
        population = Population(genders=self.genders)
        for i in range(self.initial_population_size):
            plan = copy.deepcopy(self.individual_instance)
            plan.chromosome = plan.get_random_chromosome()
            population.add_individual(plan)
        
        for i in range(self.max_generations_number):
            print('Processing generation %d' % i)
            population.process_generation()
            print('  Current maximum fitness value = %f' % population.population[0].get_fitness_value())
            if (population.population[0].get_fitness_value() == population.population[0].get_optimal_value()):
                break;
        return population.population[0]
