import sys
from genetic_executor import GeneticExecutor
from sphere_plan import SpherePlan
from sphere_plan_aggregated_fitness import SphereAggregatedFitnessPlan
from schwefel_double_sum_plan_naive import SchwefelDoubleSumPlanNaive
from schwefel_double_sum_plan_separable import SchwefelDoubleSumPlanSeparable
from rosenbrock_plan_naive import RosenbrockPlanNaive
from rosenbrock_plan_separable import RosenbrockPlanSeparable
from schwefel_sin_plan_naive import SchwefelSinPlanNaive

def test_plan(plan, value):
    print(plan.__class__.__name__, end=' ')
    sys.stdout.flush()
    TIMES_TO_FAIL = 5
    
    # Randomized algorithm, so it needs to fail TIMES_TO_FAIL times to be considered failure
    for _ in range(TIMES_TO_FAIL):
        ge = GeneticExecutor(plan, population_size = 200, max_generations_number = 100)    
        solution = ge.get_solution()
        print(solution.get_fitness_value(), end=' ')
        sys.stdout.flush()
        try:
            assert solution.get_fitness_value() >= -value
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
    
    
def test_all():
    result = True
    result &= test_plan(SpherePlan(10), 1e-100)
    result &= test_plan(SphereAggregatedFitnessPlan(10), 0)
    result &= test_plan(SchwefelDoubleSumPlanNaive(10), 1)
    result &= test_plan(SchwefelDoubleSumPlanSeparable(10), 1e-4)
    result &= test_plan(RosenbrockPlanNaive(10), 8)
    result &= test_plan(RosenbrockPlanSeparable(10), 0.005)
    result &= test_plan(SchwefelSinPlanNaive(10), 0.001)
    
    print('== Finished ==')
    if result:
        print('OK')
    else:
        print('FAIL')
        sys.exit(1)
        
        
if __name__ == '__main__':
    test_all()