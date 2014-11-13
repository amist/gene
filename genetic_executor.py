#from population import Population
#from queens_plan import QueensPlan
from random import randint
import copy

class Population:
	def __init__(self, size = 200, expansion_factor = 5):
		self.population = []
		self.size = size
		self.expansion_factor = expansion_factor
		
	def add_individual(self, individual):
		self.population.append(individual)
		
	def process_generation(self):
		self.expand_population()
		self.sort_population()
		#self.distinct_population()
		self.cut_population()
		
	def expand_population(self):
		for i in range(self.size * (self.expansion_factor - 1)):
			self.population.append(self.population[randint(0, len(self.population) - 1)].get_child(self.population[randint(0, len(self.population) - 1)]))
		
	def sort_population(self):
		self.population.sort(key=lambda x: -x.get_fitness_value())
		
	def distinct_population(self):
		raise NotImplementedError
		
	def cut_population(self):
		self.population = self.population[0:self.size - 1]
		
	def print_population(self):
		print 'Printing population...'
		for i in range(len(self.population)):
			print 'printing plan number %d' % i
			print self.population[i].gene
			
class Plan:
	def get_random_gene(self):
		raise NotImplementedError('You have to implemtent a get_random_gene function')
	
	def get_child(self, parent2):
		raise NotImplementedError('You have to implemtent a get_child function')
		
	def get_fitness_value(self):
		raise NotImplementedError('You have to implemtent a get_fitness_value function')
		
	def get_optimal_value(self):
		return None
		
	def print_plan(self):
		return

class GeneticExecutor:

	def __init__(self, individual_instance, initial_population_size = 10, max_generations_number = 100):
		self.individual_instance = copy.deepcopy(individual_instance)
		self.initial_population_size = initial_population_size
		self.max_generations_number = max_generations_number
		
	def get_solution(self):
		population = Population()
		for i in range(self.initial_population_size):
			plan = copy.deepcopy(self.individual_instance)
			plan.gene = plan.get_random_gene()
			population.add_individual(plan)
		
		for i in range(self.max_generations_number):
			print 'Processing generation %d' % i
			population.process_generation()
			if (population.population[0].get_fitness_value() == population.population[0].get_optimal_value()):
				break;
		return population.population[0]
