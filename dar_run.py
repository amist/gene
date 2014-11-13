from population import Population
from dar_plan import DarPlan
from random import randint

class DarRun:
	def __init__(self):
		self.population = Population()
		
if __name__ == '__main__':
	print 'Starting...'
	population = Population()
	run = DarRun()
	for i in range(10):
		print randint(0, 10)
		plan = DarPlan()
		plan.gene = plan.get_random_gene()
		population.add_individual(plan)
	population.print_population()
	print 'Finished.'