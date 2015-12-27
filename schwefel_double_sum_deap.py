import sys
import random
from deap import creator, base, tools, algorithms

def evalOneMin(individual):
    return sum([(sum([individual[j] for j in range(i+1)]))**2 for i in range(len(individual))]),
    
def run_one_iteration(debug=False):
    LOWER_BOUND = -65.536
    UPPER_BOUND = 65.536

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()

    toolbox.register("attr_bool", random.uniform, LOWER_BOUND, UPPER_BOUND)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=3)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)


        
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
        if debug == True:
            print('== Generation {} =='.format(gen))
        [best] = tools.selBest(population, k=1)
        if debug == True:
            print(best)
            print(toolbox.evaluate(best)[0])
    top10 = tools.selBest(population, k=10)
    return toolbox.evaluate(best)[0]

    
if __name__ == '__main__':
    iterations_num = 1
    debug = True
    if len(sys.argv) > 1:
        iterations_num = int(sys.argv[1])
        debug = False
        
    for _ in range(iterations_num):
        res = run_one_iteration(debug=debug)
        print(res)