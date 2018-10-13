__author__ = 'David T. Pocock'


from hill_climbing import HillClimbing
from random_search import RandomSearch
from genetic_algorithm import GeneticAlgorithm
from csv_parser import CSVParser


def main():
    parser = CSVParser('smallfaultmatrix.txt')
    test_case_suite = parser.parse()

    """
    The main method for the application. The Genetic Algorithm uses tournament
    selection as selection method and k-point or one-point crossover as
    crossover methods. The Genetic Algorithm constructor takes in the following parameters:
    @param: target_string The target string
    @param: population_size Amount of randomly generated strings
    @param: crossover_rate Crossover Rate in percentage (i.e. 1 = 100%)
    @param: mutation_rate Mutation Rate in percentage
    @param: is_k_point_crossover Choose whether to choose k-point crossover as
            crossover method. If false, one-point crossover is performed
    @param: tournament_size_percent Percentage of population to participate in
            tournaments for selection
    @param: strongest_winner_probability Probability of strongest participant
            in tournament to win, as well as the second strongest's probability
    """
    """ga = GeneticAlgorithm(test_case_suite, 9, 400, 50, 0.8, 0.08, 0.05, 0.75)
    ga.set_show_each_chromosome(False)
    ga.set_show_fitness_internals(False)
    ga.set_show_crossover_internals(False)
    ga.set_show_mutation_internals(False)
    ga.set_show_duplicate_internals(False)
    ga.set_silent(True) # If False it shows the fittest chromosome of each generation
    ga.run(10)
    ga.get_stats()"""

    """
    The Hill Climbing constructor takes in the following parameters:
    @param: target_string The target string
    @param: solutions_size Amount of solutions (strings) to search for a
            better solution in
    """
    hc = HillClimbing(test_case_suite, 5, 100, 50)
    hc.set_show_each_solution(False)
    # hc.set_show_fitness_internals(True)
    hc.set_silent(False)
    hc.run(10)
    hc.get_stats()

    """
    The Random Search constructor takes in the following parameters:
    @param: target_string The target string
    @param: solutions_size Amount of solutions (strings) generated randomly
            each round in which the solution is searched for
    """
    """rs = RandomSearch(target_string, 1)
    rs.set_show_each_solution(False)
    rs.set_silent(True)
    rs.run(10)
    rs.get_stats()"""


if __name__ == "__main__":
    main()
