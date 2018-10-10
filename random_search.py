__author__ = 'David T. Pocock'

import timeit
from operator import itemgetter
from genetic_algorithm import GeneticAlgorithm


class RandomSearch(GeneticAlgorithm):
    show_each_solution = None
    silent = None
    mean_time = None
    mean_rounds = None
    failed = False

    def __init__(self, target_string, solutions_size):
        self.target_string = target_string
        self.solutions_size = solutions_size

    def run(self, number_of_runs):
        times = []
        rounds = []
        for i in range(0, number_of_runs):
            self.failed = False
            start_time = timeit.default_timer()
            solutions = self.generate_population(self.solutions_size)
            best_solution = self.evaluate(solutions)
            round_number = 0
            if not self.silent:
                if self.show_each_solution is True:
                    print("\n     Fitness              Solution            Round\n")
                else:
                    print("\n               Fitness    Solution            Round\n")
            while self.target_string not in solutions:
                round_number += 1
                if best_solution[1] == 0:
                    break
                if round_number > 4999999:
                    self.failed = True
                    print("\nRandom Search failed, as the target string was not reached after 5000000 rounds\n")
                    break
                new_solutions = self.generate_population(self.solutions_size)
                new_best_solution = self.evaluate(new_solutions)
                if self.show_each_solution:
                    print("       {}                 {}            {}".
                          format(str(new_best_solution[1]).rjust(2), new_best_solution[0].rjust(2), str(round_number).rjust(2)))
                if new_best_solution[1] < best_solution[1]:
                    solutions = new_solutions
                    best_solution = new_best_solution
                    if not self.silent:
                        print("\nFitter Solution ({}):  ".format(best_solution[1]), "    ", best_solution[0],
                              "             ", str(round_number).rjust(2), "\n")
            exec_time = timeit.default_timer() - start_time
            times.append(exec_time)
            rounds.append(round_number)
            if not self.failed:
                print("\nRandom Search complete, Execution Time:     {0:.3f} seconds".format(exec_time),
                  "          Rounds:", round_number, "\n")
        self.set_stats(times, rounds, number_of_runs)

    def evaluate(self, solutions):
        solutions_evaluated = []
        for solution_str in solutions:
            solution_fitness = self.fitness(solution_str, self.target_string)
            solution = solution_str, solution_fitness
            solutions_evaluated.append(solution)
        best_solution = min(solutions_evaluated, key=itemgetter(1))
        return best_solution

    def set_show_each_solution(self, boolean):
        self.show_each_solution = boolean

    def set_silent(self, boolean):
        self.silent = boolean

    def set_stats(self, times, rounds, number_of_runs):
        self.mean_time = sum(times) / number_of_runs
        self.mean_rounds = sum(rounds) / number_of_runs

    def get_stats(self):
        if self.failed is False:
            print("\n\nRandom Search Run     Mean Execution Time:  {0:.3f} seconds".format(self.mean_time),
              "     Mean Rounds:", int(self.mean_rounds), "\n\n\n")
        else:
            print("\n\nRandom Search failed to reach the target string after a reasonable amount of time\n\n\n")
        return self.mean_time
