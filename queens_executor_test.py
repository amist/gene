#from population import Population
from queens_plan import QueensPlan
from queens_executor import QueensExecutor
from random import randint

if __name__ == '__main__':
	print 'Started...'
	#qe = QueensPlan(size = 8, gene = None)
	#qe = QueensExecutor(qe)
	qe = QueensExecutor(QueensPlan, size = 8, gene = None)
	
	solution = qe.get_solution()
	print solution.gene
	print 'cost = %d' % solution.get_fitness_value()
	#population.print_population()
	
	
	
	print 'Finished.'