from random import randint
from genetic_executor import GeneticExecutor
from genetic_executor import Plan

class QueensPlan(Plan):
	def __init__(self, size = 8, gene = None):
		if (gene is None):
			self.gene = []
		self.size = size
		self._fitness = None
		
	def get_random_gene(self):
		gene = []
		for i in range(self.size):
			gene.append(randint(0, self.size - 1))
		return gene
		
	def get_child(self, parent2):
		child = QueensPlan(self.size)
		for i in range(self.size):
			# crossover
			child.gene.append(self.gene[i] if randint(0, 1) == 0 else parent2.gene[i])
			
			# mutate
			if randint(1, 10 * self.size) == 1:
				child.gene[i] = randint(0, self.size - 1)
		return child
		
	def get_fitness_value(self):
		if self._fitness is not None:
			return self._fitness
		cost = 0
		for i in range(self.size):
			for j in range(self.size):
				if i == j: continue
				cost += 1 if self.gene[i] == self.gene[j] else 0
				cost += 1 if self.gene[i] - i == self.gene[j] - j else 0
				cost += 1 if self.gene[i] + i == self.gene[j] + j else 0
		self._fitness = -cost
		return self._fitness
		
	def get_optimal_value(self):
		return 0
		
	def print_plan(self):
		print '-' + '----' * self.size
		for i in range(self.size):
			line = '|'.join([' X ' if self.gene[i] == j else '   ' for j in range(self.size)])
			print '|' + '   |' * self.size
			print '|' + line + '|'
			print '|' + '   |' * self.size
			print '-' + '----' * self.size			
		print self.gene
		print 'intersecting queens = %d' % -self.get_fitness_value()
				

if __name__ == '__main__':
	qp = QueensPlan(size = 8)
	ge = GeneticExecutor(qp, max_generations_number = 200)
	solution = ge.get_solution()
	solution.print_plan()
	