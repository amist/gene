from population import Population
from queens_plan import QueensPlan, StopQueensPlan
from random import randint

class QueensRun:
	def __init__(self):
		self.population = Population()
		
if __name__ == '__main__':
	print 'Started...'
	SIZE = 9
	population = Population()
	run = QueensRun()
	for i in range(10):
		print i
		plan = QueensPlan(SIZE)
		plan.gene = plan.get_random_gene()
		population.add_individual(plan)
	#population.print_population()
	
	for i in range(100):
		print i
		population.process_generation()
		if (population.population[0].get_fitness_value() == population.population[0].get_optimal_value()):
			break;
	print population.population[0].gene
	print 'cost = %d' % population.population[0].get_fitness_value()
	#population.print_population()
	
	
	
	print 'Finished.'