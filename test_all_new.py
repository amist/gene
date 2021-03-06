import sys
from ge.core.genetic_executor import GeneticExecutor
from ge.problems.sphere_problem import SphereIndividual
from ge.problems.sphere_aggregated_problem import SphereAggregatedIndividual
import main

def test_problem(individual_class, individual_kwargs, target_value):
    print(individual_class.__name__, end=' ')
    sys.stdout.flush()
    TIMES_TO_FAIL = 5
    
    ge_config = {'individual_class': individual_class,
                 'individual_kwargs': individual_kwargs,
                 'population_size': 200,
                 'max_generations_number': 100,
                 'debug': False,
                 'log_metadata': None,
                }
    
    # Randomized algorithm, so it needs to fail TIMES_TO_FAIL times to be considered failure
    for _ in range(TIMES_TO_FAIL):
        ge = GeneticExecutor(**ge_config)    
        solution = ge.get_solution()
        print(solution.get_fitness_value(), end=' ')
        sys.stdout.flush()
        try:
            assert solution.get_fitness_value() >= -target_value
        except AssertionError:
            # Don't do anything. Will fail outside of the loop after TIMES_TO_FAIL times
            pass
        except Exception:
            break
        else:
            print('OK')
            return True
    print('FAIL')
    return False
    
    
def test_examples():
    print('main.py', end=' ')
    sys.stdout.flush()
    try:
        main.get_solution()
        print('OK')
        return True
    except Exception:
        print('FAIL')
        return False
    
    
def test_all():
    result = True
    result &= test_examples()
    result &= test_problem(SphereIndividual, {'size': 10}, 1e-100)
    result &= test_problem(SphereAggregatedIndividual, {'size': 10}, 0)
    #result &= test_problem(SchwefelDoubleSumPlanNaive(10), 1)
    #result &= test_problem(SchwefelDoubleSumPlanSeparable(10), 1e-4)
    #result &= test_problem(RosenbrockPlanNaive(10), 8)
    #result &= test_problem(RosenbrockPlanSeparable(10), 0.005)
    #result &= test_problem(SchwefelSinPlanNaive(10), 0.001)
    
    print('== Finished ==')
    if result:
        print('OK')
    else:
        print('FAIL')
        sys.exit(1)
        
        
if __name__ == '__main__':
    test_all()