from ge.core.genetic_executor import GeneticExecutor
from ge.problems.sphere_problem import SphereIndividual
from ge.problems.sphere_aggregated_problem import SphereAggregatedIndividual
from ge.core.populations.basic_population import BasicPopulation
from ge.core.populations.medium_population import MediumPopulation
import random
import sys
import json

if __name__ == '__main__':
    # print(sys.argv)
    if len(sys.argv) < 3:
        print('Usage: python ' + sys.argv[0] + ' <output data filename> <runs config file>')
        sys.exit(1)
    data_filename = sys.argv[1]
    config_filename = sys.argv[2]
    
    all_data = []
        
    with open(config_filename) as config_file:
        all_runs = json.load(config_file)
    
    for run in all_runs:
        print(run['individual_class'], run['population_class'])
        
        ge_config = run
        ge_config['log_metadata'] = {'log_filename': 'temp_' + data_filename}
        ge_config['debug'] = False
        ge_config['individual_class'] = globals()[run['individual_class']]
        ge_config['population_class'] = globals()[run['population_class']]
        
        ge = GeneticExecutor(**ge_config)
        # solution = ge.get_solution()
        solution, cur_data = ge.get_full_data()
        all_data.append(cur_data)
        
        print(solution.chromosome)
        print(solution.get_fitness_value())
        
    with open(data_filename, 'w') as outfile:
        json.dump(all_data, outfile)
                
    
