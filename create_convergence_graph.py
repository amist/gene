from genetic_executor import Population
from schwefel_sin_plan_naive import SchwefelSinPlanNaive
from schwefel_sin_plan_aggregated_fitness import SchwefelSinPlanAggregatedFitness
from rosenbrock_plan_naive import RosenbrockPlanNaive
from rosenbrock_plan_separable import RosenbrockPlanSeparable
from schwefel_double_sum_plan_naive import SchwefelDoubleSumPlanNaive
from schwefel_double_sum_plan_separable import SchwefelDoubleSumPlanSeparable
import matplotlib.pyplot as plt

def create_one_graph(instances, serial=None):
    population_size = 200
    max_generations_number = 1000
    debug = True
    populations = [Population(individual=instance, size=population_size) for instance in instances]
    
    xs = [x for x in range(max_generations_number)]
    ys = [[] for population in populations]
    colors = ['r', 'b', 'g', 'c', 'y', 'm', 'k']
    
    for i in range(max_generations_number):
        if debug == True:
            print('Processing generation %d' % i)
        for population in populations:
            population.process_generation()
            if debug == True:
                print('  Current maximum fitness value = %f' % population.population[0].get_fitness_value())
                #print('  Current optimal solution: ' + str(population.population[0].chromosome))
                #print('  Current aggregated fitness' + str(population.population[0].aggregated_fitness))
            #if (population.population[0].get_fitness_value() == population.population[0].get_optimal_value()):
                #break;
        [a.append(b) for a, b in zip(ys, [-population.population[0].get_fitness_value() for population in populations])]
    #print(ys)
    plt.yscale('log')
    [plt.plot(xs, y, '{}-'.format(c)) for [y, c] in zip(ys, colors)]
    
    if serial is None:
        plt.show()
    else:
        filename = '_'.join([instance.__class__.__name__ for instance in instances])
        filename += '_size_{}_population_{}_{:02d}.png'.format(instances[0].size, population_size, serial)
        plt.savefig('images/' + filename)
        
        
def create_graphs():
    for i in range(20):
        chromosome_size = 200
        instances = [SchwefelSinPlanNaive(size=chromosome_size), SchwefelSinPlanAggregatedFitness(size=chromosome_size)]
        create_one_graph(instances, i)
        
        chromosome_size = 50
        instances = [RosenbrockPlanNaive(size=chromosome_size), RosenbrockPlanSeparable(size=chromosome_size)]
        create_one_graph(instances, i)
        
        chromosome_size = 100
        instances = [SchwefelDoubleSumPlanNaive(size=chromosome_size), SchwefelDoubleSumPlanSeparable(size=chromosome_size)]
        create_one_graph(instances, i)
    
    
if __name__ == '__main__':
    create_graphs()
    
    
    
    