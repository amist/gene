import random

class Individual:
    def __init__(self):
        self.fitness_value = None
        self.chromosome = []
        
        
    def get_random_chromosome(self):
        chromosome = []
        for _ in range(self.size):
            chromosome.append(random.uniform(self.lower_bound, self.upper_bound))
        return chromosome
        
        
    def get_crossover_list(self, parent2):
        return [0 if random.randint(0, 1) == 0 else 1 for _ in range(self.size)]
    
    
    def get_child(self, parent2, mutation_params=None):
        if mutation_params is None:
            mutation_params = {'mutation_prob_factor': 1, 'mutation_amp_factor': 1}
        # TODO: separate into two functions: crossover, mutation
        # TODO: get rid of mutation_factor parameter
        # TODO: define lower_bound, upper_bound, kwargs in __init__ or remove their usage in get_child
        # TODO: crossover between arbitrary number of parents
        # TODO: consider mutating the whole population at the end of each generation, decoupling mutation_factor
        # TODO: consider mutating more the unfit (possible when mutating in population level)
        
        child = self.__class__(**self.kwargs)
        
        # crossover
        crossover_list = self.get_crossover_list(parent2)
        both_chromosomes = [self.chromosome, parent2.chromosome]
        child.chromosome = [both_chromosomes[crossover_list[i]][i] for i in range(self.size)]
        
        for i in range(self.size):
            # mutate
            if random.randint(0, int(1 * self.size / (mutation_params['mutation_prob_factor'] + 1))) == 0:
                # print('before mutation: {}'.format(child.chromosome))
                # child.chromosome[i] = mutation_params['mutation_amp_factor'] * random.uniform(self.lower_bound, self.upper_bound)
                delta = (mutation_params['mutation_amp_factor']) * random.uniform(self.lower_bound, self.upper_bound)
                child.chromosome[i] += delta
                # print('delta was {}'.format(delta))
                if child.chromosome[i] > self.upper_bound:
                    child.chromosome[i] = self.upper_bound
                if child.chromosome[i] < self.lower_bound:
                    child.chromosome[i] = self.lower_bound
                # print('after mutation:  {}'.format(child.chromosome))
                # print('mutation factor was: {}'.format(mutation_params['mutation_amp_factor']))
        return child
        
        
    def calculate_fitness_value(self):
        raise NotImplementedError('You have to implemtent a calculate_fitness_value function')
        
        
    def get_fitness_value(self):
        if self.fitness_value is not None:
            return self.fitness_value
        self.fitness_value = self.calculate_fitness_value()
        return self.fitness_value
        
        
    def get_optimal_value(self):
        return None
        
        
    def print_chromosome(self):
        print(self.chromosome)
        
        
