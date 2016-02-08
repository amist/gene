from genetic_executor import Population
from sphere_plan import SpherePlan
from sphere_plan_aggregated_fitness import SphereAggregatedFitnessPlan
from schwefel_sin_plan_naive import SchwefelSinPlanNaive
from schwefel_sin_plan_naive_const_mutation_factor import SchwefelSinPlanNaiveConstMutationFactor
from schwefel_sin_plan_aggregated_fitness import SchwefelSinPlanAggregatedFitness
from rosenbrock_plan_naive import RosenbrockPlanNaive
from rosenbrock_plan_separable import RosenbrockPlanSeparable
from schwefel_double_sum_plan_naive import SchwefelDoubleSumPlanNaive
from schwefel_double_sum_plan_separable import SchwefelDoubleSumPlanSeparable
from schwefel_sin_plan_mutation_selection import SchwefelSinMutationSelection
from run_python_from_string import run_python_code

def create_one_graph(instances, serial=-1):
    population_size = 200
    max_generations_number = 150
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
    filename = '_'.join([instance.__class__.__name__ for instance in instances])
    filename += '_size_{}_population_{}_{:02d}.png'.format(instances[0].size, population_size, serial)
    run_python_code('''
import matplotlib.pyplot as plt
xs = {xs}
ys = {ys}
colors = ['r', 'b', 'g', 'c', 'y', 'm', 'k']
plt.clf()
plt.grid(True)
plt.yscale('log')
[plt.plot(xs, y, '{{}}-'.format(c)) for [y, c] in zip(ys, colors)]

if {serial}==-1:
    plt.show()
else:
    #filename = '_'.join([instance.__class__.__name__ for instance in instances])
    #filename += '_size_{{}}_population_{{}}_{{:02d}}.png'.format(instances[0].size, population_size, {serial})
    plt.savefig('images/' + {filename})
'''.format(xs=repr(xs), ys=repr(ys), serial=repr(serial), filename=repr(filename)))
#'''.format(xs='[1,2,3]', ys='[9,8,7]'))
        
        
def create_graphs():
    for i in range(1):
        #chromosome_size = 200
        #instances = [SchwefelSinPlanNaive(size=chromosome_size), SchwefelSinPlanAggregatedFitness(size=chromosome_size)]
        #create_one_graph(instances, i)
        #
        #chromosome_size = 50
        #instances = [RosenbrockPlanNaive(size=chromosome_size), RosenbrockPlanSeparable(size=chromosome_size)]
        #create_one_graph(instances, i)
        #
        #chromosome_size = 200
        #instances = [SchwefelDoubleSumPlanNaive(size=chromosome_size), SchwefelDoubleSumPlanSeparable(size=chromosome_size)]
        #create_one_graph(instances, i)
        #
        #chromosome_size = 1000
        #instances = [SpherePlan(size=chromosome_size), SphereAggregatedFitnessPlan(size=chromosome_size)]
        #create_one_graph(instances, i)
        #
        #chromosome_size = 100
        #instances = [SchwefelSinPlanNaive(size=chromosome_size), SchwefelSinMutationSelection(size=chromosome_size)]
        #create_one_graph(instances, i)
        
        chromosome_size = 10
        instances = [SchwefelSinPlanNaive(size=chromosome_size), SchwefelSinPlanNaiveConstMutationFactor(size=chromosome_size)]
        create_one_graph(instances, 4)
    
    
if __name__ == '__main__':
    create_graphs()
    
    
    
    