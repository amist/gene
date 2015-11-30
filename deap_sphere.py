import random
from deap import creator, base, tools, algorithms

LOWER_BOUND = -5.12
UPPER_BOUND = 5.12

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

toolbox.register("attr_bool", random.uniform, LOWER_BOUND, UPPER_BOUND)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=30)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalOneMin(individual):
    return sum([s*s for s in individual]),
    
toolbox.register("evaluate", evalOneMin)
toolbox.register("mate", tools.cxUniform, indpb=0.5)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
#toolbox.register("select", tools.selTournament, tournsize=3)

toolbox.register("select", tools.selBest)

population = toolbox.population(n=300)

NGEN=100
for gen in range(NGEN):
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)
    fits = toolbox.map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit
    population = toolbox.select(offspring, k=len(population))
    print('== Generation {} =='.format(gen))
    [best] = tools.selBest(population, k=1)
    print(best)
    print(toolbox.evaluate(best))
top10 = tools.selBest(population, k=10)
