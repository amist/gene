from ge.core.genetic_executor import GeneticExecutor
from ge.problems.sphere_problem import SphereIndividual
import random
import sys
import json

if __name__ == '__main__':
    # print(sys.argv)
    if len(sys.argv) < 3:
        print('Usage: python ' + sys.argv[0] + ' <output data filename> <Individual class> [<more Individual classes>]')
        sys.exit(1)
    filename = sys.argv[1]
    classes = [globals()[sys.argv[i]] for i in range(2, len(sys.argv))]
    # print(classes)
    # exit(0)
    all_data = []
    
    for _class in classes:
        ge_config = {'individual_class': SphereIndividual,
                     'individual_kwargs': {'size': 10},
                     'population_size': 200,
                     'max_generations_number': 100,
                     'debug': False,
                     'log_metadata': {'log_filename': 'temp_' + filename},
                     # 'log_metadata': None,
                    }
        ge = GeneticExecutor(**ge_config)
        # solution = ge.get_solution()
        solution, cur_data = ge.get_full_data()
        all_data.append(cur_data)
        
    with open(filename, 'w') as outfile:
        json.dump(all_data, outfile)
                
    print(solution.chromosome)
    print(solution.get_fitness_value())
