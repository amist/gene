#from random import randint
import random
import copy

class Population:
    def __init__(self, size=200, expansion_factor=5):
        self.population_a = []
        self.population_b = []
        self.size = size
        self.expansion_factor = expansion_factor
        self.candidates_num = 100
        
        
    def add_individual_to_a(self, individual):
        self.population_a.append(individual)
        
        
    def add_individual_to_b(self, individual):
        self.population_b.append(individual)
        
        
    def _get_individual_from_a(self):
        return self.population_a[random.randint(0, len(self.population_a) - 1)]
        
        
    def _get_individual_from_b(self, parent1):
        parent2 = None
        max_heuristic = None
        for _ in range(self.candidates_num):
            candidate = self.population_b[random.randint(0, len(self.population_b) - 1)]
            cur_heuristic = parent1.get_heuristic_value(candidate)
            if max_heuristic is None or max_heuristic < cur_heuristic:
                parent2 = candidate
                max_heuristic = cur_heuristic
        return parent2
        
        
    def process_generation(self):
        self._expand_population()
        self._sort_population()
        self._cut_population()
        #self.population[0].print_individual()
        
        
    def _expand_population(self):
        for _ in range(self.size * (self.expansion_factor - 1)):
            parent1 = self._get_individual_from_a()
            parent2 = self._get_individual_from_b(parent1)
            child1, child2 = parent2.get_children(parent1)
            self.population_a.append(child1)
            self.population_b.append(child2)
        
        
    def _sort_population(self):
        self.population_a.sort(key=lambda x: -x.get_fitness_value())
        self.population_b.sort(key=lambda x: -x.get_fitness_value())
        
        
    def _cut_population(self):
        self.population_a = self.population_a[0:self.size - 1]
        self.population_b = self.population_b[0:self.size - 1]
    
            
class Individual:
    def get_random_data_chromosome(self):
        raise NotImplementedError('You have to implement a get_random_data_chromosome function')
        
    def get_random_operator_chromosome(self):
        raise NotImplementedError('You have to implement a get_random_operator_chromosome function')
        
    def get_fitness_value(self):
        raise NotImplementedError('You have to implement a get_fitness_value function')
        
    def get_optimal_value(self):
        return None
        
    def print_individual(self):
        return
        
        
class IndividualA(Individual):
    def get_heuristic_value(self, candidate):
        raise NotImplementedError('You have to implement a get_heuristic_value function')
    
    
class IndividualB(Individual):
    def get_child(self, parent2):
        raise NotImplementedError('You have to implement a get_child function')
    

class GeneticExecutor:

    def __init__(self, individual_a_instance, individual_b_instance, initial_population_size=10, max_generations_number=100):
        self.individual_a_instance = copy.deepcopy(individual_a_instance)
        self.individual_b_instance = copy.deepcopy(individual_b_instance)
        self.initial_population_size = initial_population_size
        self.max_generations_number = max_generations_number
        
        
    def create_random_individual(self, type):
        if type == 'a':
            individual = copy.deepcopy(self.individual_a_instance)
        elif type == 'b':
            individual = copy.deepcopy(self.individual_b_instance)
        else:
            raise Exception('Unknown individual type \'{}\' in create_random_individual'.format(type))
        individual.data_chromosome = individual.get_random_data_chromosome()
        individual.operator_chromosome = individual.get_random_operator_chromosome()
        return individual
        
        
    def get_solution(self):
        population = Population()
        for i in range(self.initial_population_size):
            individual = self.create_random_individual('a')
            population.add_individual_to_a(individual)
            individual = self.create_random_individual('b')
            population.add_individual_to_b(individual)
        
        for i in range(self.max_generations_number):
            print('Processing generation {}'.format(i))
            population.process_generation()
            print('  Current maximum fitness value in population_a = {} with {} | {}'.format(population.population_a[0].get_fitness_value(), population.population_a[0].data_chromosome, population.population_a[0].operator_chromosome))
            print('  Current maximum fitness value in population_b = {} with {} | {}'.format(population.population_b[0].get_fitness_value(), population.population_b[0].data_chromosome, population.population_b[0].operator_chromosome))
            if (population.population_a[0].get_fitness_value() == population.population_a[0].get_optimal_value() or
                population.population_b[0].get_fitness_value() == population.population_b[0].get_optimal_value()):
                break;
                
        if population.population_a[0].get_fitness_value() > population.population_b[0].get_fitness_value():
            return population.population_a[0]
        else:
            return population.population_b[0]
