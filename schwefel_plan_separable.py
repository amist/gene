import random
from genetic_executor import GeneticExecutor
from genetic_executor import Plan

class SchwefelPlanSeparable(Plan):
    def __init__(self, size = 10, chromosome = None):
        if (chromosome is None):
            self.chromosome = []
        else:
            self.chromosome = chromosome
        self.size = size
        self._fitness = None
        self._lower_bound = -65.536
        self._upper_bound = 65.536
        
        
    def get_chromosome_size(self):
        return int(self.size * (self.size + 1) / 2)
        
        
    def get_random_chromosome(self):
        chromosome = []
        for _ in range(self.get_chromosome_size()):
            chromosome.append(random.uniform(self._lower_bound, self._upper_bound))
        return chromosome
            
            
    def get_child(self, parent2):
        child = SchwefelPlanSeparable(self.size)
        for i in range(self.get_chromosome_size()):
            # crossover
            child.chromosome.append(self.chromosome[i] if random.randint(0, 1) == 0 else parent2.chromosome[i])
            
            # mutate
            if random.randint(1, 10 * self.get_chromosome_size()) == 1:
                child.chromosome[i] = random.uniform(self._lower_bound, self._upper_bound)
        return child
        
        
    def get_solution(self):
        solution = self.size * [0]
        k = 0
        for i in range(self.size):
            for j in range(i+1):
                solution[j] += self.chromosome[k]
                k += 1
        return solution
        
        
    def get_fitness_value(self):
        if self._fitness is not None:
            return self._fitness
        solution = self.get_solution()
        self._fitness = -sum([(sum([solution[j] for j in range(i+1)]))**2 for i in range(len(solution))])
        return self._fitness
        
        
    def print_plan(self):
        print(self.chromosome)
        print(self.get_solution())
            
        
        
if __name__ == '__main__':
    sp = SchwefelPlanSeparable(10)
    ge = GeneticExecutor(sp, population_size = 200, max_generations_number = 100)
    solution = ge.get_solution()
    solution.print_plan()