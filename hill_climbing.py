__author__ = 'David T. Pocock'

import timeit, random
from operator import itemgetter
from genetic_algorithm import GeneticAlgorithm


class HillClimbing(GeneticAlgorithm):
    show_each_solution = None
    show_fitness_internals = None
    silent = None
    mean_time = None
    mean_rounds = None

    def __init__(self, test_case_suite, solution_size, solutions_pool_size, number_of_rounds):
        self.test_case_suite = test_case_suite
        self.solution_size = solution_size
        self.solutions_pool_size = solutions_pool_size
        self.number_of_rounds = number_of_rounds

    def run(self, number_of_runs):
        times = []
        rounds = []
        for i in range(0, number_of_runs):
            start_time = timeit.default_timer()
            solutions = self.generate_population(self.solutions_pool_size, self.solution_size)
            print("Solutions:", solutions)
            best_solution = self.evaluate(solutions)
            print("best solution", best_solution[1])
            round_number = 0
            if not self.silent:
                if self.show_each_solution is True:
                    print("\n     Fitness              Solution            Round\n")
                else:
                    print("\n               Fitness    Solution            Round\n")
            for i in range(0, self.number_of_rounds):
                round_number += 1
                if best_solution[1] == 1:
                    break
                new_solutions = self.generate_new_solutions(best_solution[0])
                new_best_solution = self.evaluate(new_solutions)
                if self.show_each_solution:
                    print("       {}              {}            {}".
                          format(str(new_best_solution[1]).rjust(2), new_best_solution[0].rjust(2), str(round_number).rjust(2)))
                if new_best_solution[1] < best_solution[1]:
                    solutions = new_solutions
                    best_solution = new_best_solution
                    if not self.silent:
                        print("\nFitter Solution ({}):  ".format(best_solution[1]), best_solution[0],
                              "          ", str(round_number).rjust(2), "\n")
            exec_time = timeit.default_timer() - start_time
            times.append(exec_time)
            rounds.append(round_number)
            print("\nHill Climbing complete, Execution Time:     {0:.3f} seconds".format(exec_time),
                  "          Rounds:", round_number, "\n")
        self.set_stats(times, rounds, number_of_runs)

    # def fitness(self, source, target):
    #     fit_chars = [None] * len(self.target_string)
    #     if len(source) == len(target):
    #         pairs = zip(source, target)
    #         hamming_distance = 0
    #         for i, (a, b) in enumerate(pairs):
    #             if a != b:
    #                 hamming_distance += 1
    #             else:
    #                 fit_chars[i] = [a]
    #         return hamming_distance, fit_chars
    #     else:
    #         raise ValueError('Source and target string must be of the same length!')

    def evaluate(self, solutions):
        solutions_evaluated = []
        for solution in solutions:
            solution_fitness = self.fitness(solution, self.solution_size)
            # solution_fitness = self.fitness(solution)
            # print("\nsolution fitness", solution_fitness)
            # fitness = solution_fitness[0]
            # fit_chars = solution_fitness[1]
            # solution = solution_str, fitness, fit_chars
            solution = solution, solution_fitness
            solutions_evaluated.append(solution)
        best_solution = max(solutions_evaluated, key=itemgetter(1))
        # print("Best:", best_solution)
        return best_solution

    def generate_new_solutions(self, best_solution):
        solutions = []
        for i in range(0, self.solutions_pool_size):
            solution = []
            str_length = len(self.target_string)
            for j, char in enumerate(range(0,str_length)):
                if best_solution[j] is None:
                    char = random.choice(self.available_chars())
                    solution.append(char)
                else:
                    solution.append(best_solution[j][0])
            solution_string = ''.join(solution)
            solutions.append(solution_string)
        return solutions

    def set_show_each_solution(self, boolean):
        self.show_each_solution = boolean

    def set_silent(self, boolean):
        self.silent = boolean

    def set_stats(self, times, rounds, number_of_runs):
        self.mean_time = sum(times) / number_of_runs
        self.mean_rounds = sum(rounds) / number_of_runs

    def get_stats(self):
        print("\n\nHill Climbing Run, Mean Execution Time:     {0:.3f} seconds".format(self.mean_time),
              "     Mean Rounds:", int(self.mean_rounds), "\n\n\n")
        return self.mean_time
