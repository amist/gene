import sys
import statistics
import random
from deap import creator, base, tools, algorithms

LOWER_BOUND = -5.12
UPPER_BOUND = 5.12

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

toolbox.register("attr_bool", random.uniform, LOWER_BOUND, UPPER_BOUND)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=10)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalOneMin(individual):
    return sum([s*s for s in individual]),
    
toolbox.register("evaluate", evalOneMin)
toolbox.register("mate", tools.cxUniform, indpb=0.5)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
#toolbox.register("select", tools.selTournament, tournsize=3)

toolbox.register("select", tools.selBest)

NGEN=100

iterations_num = 1
debug = True
solutions = []
if len(sys.argv) > 1:
    iterations_num = int(sys.argv[1])
    debug = False

for _ in range(iterations_num):
    population = toolbox.population(n=300)
    for gen in range(NGEN):
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)
        fits = toolbox.map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        population = toolbox.select(offspring, k=len(population))
        if debug:
            print('== Generation {} =='.format(gen))
        [best] = tools.selBest(population, k=1)
        if debug:
            print(best)
            print(toolbox.evaluate(best))
    solutions.append(toolbox.evaluate(best)[0])
    print(toolbox.evaluate(best)[0])
        
[mean, std] = [solutions[0], 0]
if len(solutions) > 1:
    [mean, std] = [statistics.mean(solutions), statistics.stdev(solutions)]
    
print('==============================')
print('Mean: ' + str(mean))
print('STD:  ' + str(std))
