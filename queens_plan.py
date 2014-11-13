from random import randint
from genetic_executor import GeneticExecutor
from genetic_executor import Plan

class QueensPlan(Plan):
	def __init__(self, size = 8, gene = None):
		if (gene is None):
			self.gene = []
		self.size = size
		
	def get_random_gene(self):
		gene = []
		for i in range(self.size):
			gene.append(randint(0, self.size - 1))
		return gene
		
	def get_child(self, parent2):
		child = QueensPlan(self.size)
		for i in range(self.size):
			child.gene.append(self.gene[i] if randint(0, 1) == 0 else parent2.gene[i])
			if randint(1, self.size) == 1:
				child.gene[i] = randint(0, self.size - 1)
		return child
		
	def get_fitness_value(self):
		cost = 0
		for i in range(self.size):
			for j in range(self.size):
				if i == j: continue
				cost += 1 if self.gene[i] == self.gene[j] else 0
				cost += 1 if self.gene[i] - i == self.gene[j] - j else 0
				cost += 1 if self.gene[i] + i == self.gene[j] + j else 0
		return -cost
		
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
				

if __name__ == '__main__':
	qp = QueensPlan(size = 15)
	ge = GeneticExecutor(qp)
	solution = ge.get_solution()
	solution.print_plan()
	print solution.gene
	print 'intersecting queens = %d' % -solution.get_fitness_value()