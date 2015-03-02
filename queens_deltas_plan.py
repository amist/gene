import random
from genetic_executor import GeneticExecutor
from genetic_executor import Plan

class QueensDeltasPlan(Plan):
    def __init__(self, size = 8, gene = None):
        if (gene is None):
            self.gene = []
        self.size = size
        self._fitness = None
        
    def get_random_gene(self):
        gene = []
        for i in range(self.size):
            gene.append(random.randint(0, self.size - 1))
        return gene
        
    def get_child(self, parent2):
        child = QueensDeltasPlan(self.size)
        separator = random.uniform(0, self.size + 1)
        for i in range(self.size):
            # crossover
            child.gene.append(self.gene[i] if i < separator else parent2.gene[i])
            
            # mutate
            if random.randint(1, 10 * self.size) == 1:
                child.gene[i] = random.randint(0, self.size - 1)
        return child
        
    def get_fitness_value(self):
        if self._fitness is not None:
            return self._fitness
        cost = 0
        positions = self.gene
        for i in range(len(positions) - 1):
            positions[i + 1] = (int(positions[i + 1]) + int(positions[i])) % self.size
        for i in range(self.size):
            for j in range(self.size):
                if i == j: continue
                cost += 1 if positions[i] == positions[j] else 0
                cost += 1 if positions[i] - i == positions[j] - j else 0
                cost += 1 if positions[i] + i == positions[j] + j else 0
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
    qp = QueensDeltasPlan(size = 8)
    ge = GeneticExecutor(qp, max_generations_number = 200)
    solution = ge.get_solution()
    solution.print_plan()
    