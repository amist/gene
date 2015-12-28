import random
import statistics
import copy
from genetic_executor import Plan

class ArgsPlan(Plan):
    def __init__(self, ge, iterations_num=8):
        self.chromosome = []
        self.ge = copy.deepcopy(ge)
        self.iterations_num = iterations_num
        self._fitness_value = None
    
    
    def get_random_chromosome(self):
        # [mutation prbability, size dependant mutation probability, mutation step factor]
        return [random.randint(2, 100), True if random.randint(0,1) == 0 else False, random.uniform(0,1)]
        
        
    def get_child(self, parent2):
        child = ArgsPlan(copy.deepcopy(self.ge))
        for i in range(3):
            # crossover
            child.chromosome.append(self.chromosome[i] if random.randint(0, 1) == 0 else parent2.chromosome[i])
            
            # mutate
            if random.randint(1, 10 * 3) == 1:
                if i == 0:
                    rand_val = child.chromosome[i] + int(0.1 * (random.randint(2, 100) - 0.5 * (2 + 100)))
                if i == 1:
                    rand_val = True if random.randint(0,1) == 0 else False
                else:
                    rand_val = child.chromosome[i] + 0.1 * (random.uniform(0, 1) - 0.5)
                child.chromosome[i] = rand_val
        return child
        
        
    def get_fitness_value(self):
        if self._fitness_value is not None:
            return self._fitness_value
        
        results = []
        for _ in range(self.iterations_num):
            ge = copy.deepcopy(self.ge)
            solution = ge.get_solution()
            results.append(solution.get_fitness_value())
            
        print(results)
        return statistics.mean(results)
        
        
        
        