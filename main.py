__author__ = 'David T. Pocock'


from hill_climbing import HillClimbing
from random_search import RandomSearch
from genetic_algorithm import GeneticAlgorithm
from csv_parser import CSVParser


def main():
    parser = CSVParser('bigfaultmatrix.txt')
    test_case_fault_matrix = parser.parse_unique()

    """ga = GeneticAlgorithm(test_case_fault_matrix, 111, 400, 50, 0.8, 0.08, 0.05, 0.75)
    ga.set_show_each_chromosome(False)
    ga.set_show_fitness_internals(False)
    ga.set_show_crossover_internals(False)
    ga.set_show_mutation_internals(False)
    ga.set_show_duplicate_internals(False)
    ga.set_silent(True) # If False it shows the fittest chromosome of each generation
    ga.run(10)
    ga.get_stats()"""

    hc = HillClimbing(test_case_fault_matrix, 5, 50, 5000)
    hc.set_show_each_solution(False)
    hc.set_show_fitness_internals(False)
    hc.set_show_swapping_internals(False)
    hc.set_silent(False)
    hc.run(10)
    hc.get_stats()

    """rs = RandomSearch(test_case_fault_matrix, 111, 400, 20)
    rs.set_show_each_solution(False)
    rs.set_silent(True)
    rs.run(10)
    rs.get_stats()"""


if __name__ == "__main__":
    main()
