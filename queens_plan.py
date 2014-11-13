from random import randint
from genetic_executor import GeneticExecutor

class QueensPlan:
	def __init__(self, size = 8, gene = None):
		if (gene is None):
			self.gene = []
		self.size = size
		
	def get_random_gene(self):
		gene = []
		for i in range(self.size):
			gene.append(randint(1, self.size))
		return gene
		
	def get_child(self, parent2):
		child = QueensPlan(self.size)
		for i in range(self.size):
			child.gene.append(self.gene[i] if randint(0, 1) == 0 else parent2.gene[i])
			if randint(1, self.size) == 1:
				child.gene[i] = randint(1, self.size)
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

if __name__ == '__main__':
	qp = QueensPlan()
	ge = GeneticExecutor(qp)
	solution = ge.get_solution()
	print solution.gene
	