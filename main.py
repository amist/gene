from ge.core.genetic_executor import GeneticExecutor
from ge.problems.sphere_problem import SphereIndividual

if __name__ == '__main__':
    sp = SphereIndividual(10)
    ge = GeneticExecutor(SphereIndividual)
    solution = ge.get_solution()
    print(solution.chromosome)
    print(solution.get_fitness_value())