from random import randint
from genetic_executor import GeneticExecutor
from genetic_executor import Plan

class QueensPlan(Plan):
    def __init__(self, size = 8, chromosome = None):
        if (chromosome is None):
            self.chromosome = []
        self.size = size
        self._fitness = None
        
    def get_random_chromosome(self):
        chromosome = []
        for _ in range(self.size):
            chromosome.append(randint(0, self.size - 1))
        return chromosome
        
    def get_child(self, parent2):
        child = QueensPlan(self.size)
        for i in range(self.size):
            # crossover
            child.chromosome.append(self.chromosome[i] if randint(0, 1) == 0 else parent2.chromosome[i])
            
            # mutate
            if randint(1, 10 * self.size) == 1:
                child.chromosome[i] = randint(0, self.size - 1)
        return child
        
    def get_fitness_value(self):
        if self._fitness is not None:
            return self._fitness
        cost = 0
        for i in range(self.size):
            for j in range(self.size):
                if i == j: continue
                cost += 1 if self.chromosome[i] == self.chromosome[j] else 0
                cost += 1 if self.chromosome[i] - i == self.chromosome[j] - j else 0
                cost += 1 if self.chromosome[i] + i == self.chromosome[j] + j else 0
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
    qp = QueensPlan(size = 8)
    ge = GeneticExecutor(qp, max_generations_number = 200)
    solution = ge.get_solution()
    solution.print_plan()
    
