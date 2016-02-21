from ge.core.genetic_executor import GeneticExecutor
from ge.problems.sphere_problem import SphereIndividual
from ge.problems.sphere42_problem import Sphere42Individual
from ge.problems.sphere_aggregated_problem import SphereAggregatedIndividual
import random
import sys
import json

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python ' + sys.argv[0] + ' <output data filename>')
        sys.exit(1)
    filename = sys.argv[1]
    all_data = []
    
    # ge_configs = [{'individual_class': SphereIndividual,
                   # 'individual_kwargs': {'size': 10},
                   # 'population_size': 200,
                   # 'max_generations_number': 100,
                   # 'debug': False,
                   # 'log_metadata': {'log_filename': 'temp_' + filename},
                  # },
                  # {'individual_class': SphereAggregatedIndividual,
                   # 'individual_kwargs': {'size': 10},
                   # 'population_size': 200,
                   # 'max_generations_number': 100,
                   # 'debug': False,
                   # 'log_metadata': {'log_filename': 'temp_' + filename},
                  # }]
    
    ge_configs = [{'individual_class': SphereIndividual,
                   'individual_kwargs': {'size': 10},
                   'population_size': 200,
                   'max_generations_number': 100,
                   'debug': False,
                   'log_metadata': {'log_filename': 'temp_' + filename},
                  },
                  {'individual_class': Sphere42Individual,
                   'individual_kwargs': {'size': 10},
                   'population_size': 200,
                   'max_generations_number': 100,
                   'debug': False,
                   'log_metadata': {'log_filename': 'temp_' + filename},
                  }]
    
    
    for ge_config in ge_configs:
        print(ge_config['individual_class'].__name__)
        
        ge = GeneticExecutor(**ge_config)
        solution, cur_data = ge.get_full_data()
        all_data.append(cur_data)
        
        print(solution.chromosome)
        print(solution.get_fitness_value())
        
    with open(filename, 'w') as outfile:
        json.dump(all_data, outfile)
                
    
