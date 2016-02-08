import random
from genetic_executor import GeneticExecutor
from genetic_executor import Plan

class QueensDeltasPlan(Plan):
    def __init__(self, size = 8, chromosome = None):
        if (chromosome is None):
            self.chromosome = []
        self.size = size
        self._fitness = None
        
    def get_random_chromosome(self):
        chromosome = []
        for i in range(self.size):
            chromosome.append(random.randint(0, self.size - 1))
        return chromosome
        
    def get_child(self, parent2):
        child = QueensDeltasPlan(self.size)
        separator = random.uniform(0, self.size + 1)
        for i in range(self.size):
            # crossover
            child.chromosome.append(self.chromosome[i] if i < separator else parent2.chromosome[i])
            
            # mutate
            if random.randint(1, 10 * self.size) == 1:
                child.chromosome[i] = random.randint(0, self.size - 1)
        return child
        
    def get_fitness_value(self):
        if self._fitness is not None:
            return self._fitness
        cost = 0
        positions = self.chromosome
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
            line = '|'.join([' X ' if self.chromosome[i] == j else '   ' for j in range(self.size)])
            print '|' + '   |' * self.size
            print '|' + line + '|'
            print '|' + '   |' * self.size
            print '-' + '----' * self.size          
        print self.chromosome
        print 'intersecting queens = %d' % -self.get_fitness_value()
                

if __name__ == '__main__':
    qp = QueensDeltasPlan(size = 8)
    ge = GeneticExecutor(qp, max_generations_number = 200)
    solution = ge.get_solution()
    solution.print_plan()
    