__author__ = 'David T. Pocock'


import random, string, timeit
from operator import itemgetter


class GeneticAlgorithm:
    show_each_chromosome = None
    show_fitness_internals = None
    show_crossover_internals = None
    show_mutation_internals = None
    show_duplicate_internals = None
    silent = None
    mean_time = None
    mean_generations = None
    failed = False

    def __init__(self, unique_fault_combinations, chromosome_size, population_size, number_of_generations, crossover_rate,
                 mutation_rate, tournament_size_percent, strongest_winner_probability):
        self.unique_fault_combinations = unique_fault_combinations
        self.chromosome_size = chromosome_size
        self.population_size = population_size
        self.number_of_generations = number_of_generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.tournament_size_percent = tournament_size_percent
        self.strongest_winner_probability = strongest_winner_probability

    def tournament_size(self):
        size = int(self.tournament_size_percent * self.population_size)
        return size

    def tournament_rounds(self):
        return self.population_size

    def strongest_winner_prob(self):
        return self.strongest_winner_probability

    def crossover_point(self):
        value = random.random()
        return value

    def run(self, number_of_runs):
        times = []
        generations = []
        for i in range(0, number_of_runs):
            self.failed = False
            start_time = timeit.default_timer()
            population = self.generate_population(self.population_size)
            if self.tournament_size() % 2 != 0:
                raise ValueError('Tournament Size must be an even number!')
            generation_number = 0
            fittest_chromosome = 0
            if self.show_each_chromosome: print("       Fitness (APFD)                          Chromosome        "
                                                "             Generation\n")
            for i in range(0, self.number_of_generations):
                generation_number += 1
                winners = self.selection(population)
                pre_mutation_generation = self.check_for_crossover(winners)
                new_generation = self.mutate(pre_mutation_generation)
                population = new_generation
                counter = 0
                for chromosome in population:
                    counter += 1
                    fitness_value = self.fitness(chromosome)
                    if counter == 1:
                        fittest_chromosome = chromosome, fitness_value
                    if self.show_each_chromosome:
                        print("       {0:.10f}".format(fitness_value),"            {}".format(chromosome),"            {}"
                                                 .format(generation_number))
                    if fitness_value >= fittest_chromosome[1]:
                        fittest_chromosome = chromosome, fitness_value
                        if fitness_value == 1:
                            break
                if not self.silent:
                    print("\nFittest Value:", fittest_chromosome[1], "    Chromosome:", fittest_chromosome[0],
                          "    Generation:", generation_number)
            exec_time = timeit.default_timer() - start_time
            times.append(exec_time)
            generations.append(generation_number)
            if not self.failed:
                print("\nGenetic Algorithm complete, Execution Time: {0:.3f} seconds".format(exec_time),
                      "          Generations:", generation_number, "\n")
        if not self.failed:
            self.set_stats(times, generations, number_of_runs)

    def generate_population(self, size):
        population = []
        for i in range(0, size):
            chromosome = []
            for j in range(0, self.chromosome_size):
                self.populate(j, chromosome)
            if self.show_duplicate_internals: print()
            population.append(chromosome)
        return population

    def populate(self, j, chromosome):
        random_index = random.randint(0, len(self.unique_fault_combinations) - 1)
        unique_test_cases = list(self.unique_fault_combinations.values())
        chromosome.append(unique_test_cases[random_index])
        if self.show_duplicate_internals: print("Chromosome:", chromosome)
        if j > 0:
            if self.check_for_duplicate(chromosome):
                if self.show_duplicate_internals: print("Duplicate found, popping it and picking again")
                chromosome.pop()
                self.populate(j, chromosome)

    def fitness(self, chromosome):
        fault_matrix_chromosome = self.from_test_case_to_fault_matrix(chromosome)
        weight = 0
        number_of_test_cases_in_set = self.chromosome_size
        number_of_faults = len(fault_matrix_chromosome[0])
        if self.show_fitness_internals: print("Calculating fitness (APFD) of Chromosome:", fault_matrix_chromosome)
        for i in range(0, number_of_faults):
            for j in range(0, number_of_test_cases_in_set):
                if fault_matrix_chromosome[j][i]:
                    weight += j+1
                    break
                if j == self.chromosome_size - 1:
                    weight += number_of_test_cases_in_set + 1
        apfd = 1 - (weight/(number_of_faults * number_of_test_cases_in_set)) + 1/(2 * number_of_test_cases_in_set)
        if self.show_fitness_internals:
            print("APFD:", apfd, "Weight:", weight, "Number of Faults:", number_of_faults,
              "Number of Test Cases:", number_of_test_cases_in_set, "\n")
        return apfd

    def selection(self, population):
        return self.tournament_selection(population)

    def decision(self, probability):
        rand_int = random.random()
        return rand_int < probability

    def tournament_selection(self, population):
        winners = []
        for t_round in range(0, self.tournament_rounds()):
            participants = []
            for participant in range(0, self.tournament_size()):
                random_index = random.randint(0, len(population) - 1)
                participant = population[random_index]
                participant_fitness = self.fitness(participant)
                participant_evaluated = participant, participant_fitness
                participants.append(participant_evaluated)
            if self.decision(self.strongest_winner_prob()):
                winner = max(participants, key=itemgetter(1))
                winners.append(winner)
            elif self.decision(self.strongest_winner_prob()):
                temp_participant = max(participants, key=itemgetter(1))
                participants.remove(temp_participant)
                winner = max(participants, key=itemgetter(1))
                winners.append(winner)
                participants.append(temp_participant)
            else:
                first_temp_participant = max(participants, key=itemgetter(1))
                participants.remove(first_temp_participant)
                second_temp_participant = max(participants, key=itemgetter(1))
                participants.remove(second_temp_participant)
                winner = max(participants, key=itemgetter(1))
                winners.append(winner)
                participants.append(first_temp_participant)
                participants.append(second_temp_participant)
        winners_test_combo = [test_combos[0] for test_combos in winners]
        paired_winners = list(zip(winners_test_combo[0::2], winners_test_combo[1::2]))
        return paired_winners

    def check_for_crossover(self, parents):
        new_generation = []
        for first_parent, second_parent in parents:
            if self.decision(self.crossover_rate):
                children_duo = self.crossover(first_parent, second_parent)
                for child in children_duo:
                    new_generation.append(child)
            else:
                new_generation.append(first_parent)
                new_generation.append(second_parent)
        return new_generation

    def crossover(self, first_parent, second_parent):
        if self.show_crossover_internals:
            print("\nParent #1:", first_parent)
            print("Parent #2:", second_parent)
        first_child_test_case_set = []
        second_child_test_case_set = []
        i = 0
        point = int(self.crossover_point() * (self.chromosome_size - 1)) + 1
        first_parent_copy = first_parent.copy()
        second_parent_copy = second_parent.copy()
        for test_case_a, test_case_b in zip(first_parent, second_parent):
            i += 1
            if i <= point:
                first_child_test_case_set.append(test_case_a)
                if test_case_b in first_parent_copy:
                    first_parent_copy.remove(test_case_b)
                else:
                    first_parent_copy.pop()
                second_child_test_case_set.append(test_case_b)
                if test_case_a in second_parent_copy:
                    second_parent_copy.remove(test_case_a)
                else:
                    second_parent_copy.pop()
            else:
                first_child_test_case_set.extend(second_parent_copy)
                second_child_test_case_set.extend(first_parent_copy)
                break
        if self.show_crossover_internals:
            print("Crossover Point after Test Case #{}".format(point))
            print("Child #1:", first_child_test_case_set)
            print("Child #2:", second_child_test_case_set)
        return first_child_test_case_set, second_child_test_case_set

    def mutate(self, generation):
        new_generation = []
        for chromosome in generation:
            if self.show_mutation_internals: print("\nChromosome being worked on:  ", chromosome, "\n")
            for test_case in chromosome:
                if self.decision(self.mutation_rate):
                    if self.show_mutation_internals: print("Chromosome pre-mutation:   ", chromosome)
                    current_index = chromosome.index(test_case)
                    random_index = self.swap_test_cases(current_index)
                    chromosome[current_index], chromosome[random_index] = chromosome[random_index], chromosome[current_index]
                    if self.show_mutation_internals:
                        print("Test Case", chromosome[current_index], "at index #{}".format(random_index),
                              "swapped with Test Case", chromosome[random_index], "at index #{}".format(current_index))
                        print("Chromosome post-mutation:   ", chromosome, "\n")
            new_generation.append(chromosome)
        return new_generation

    def swap_test_cases(self, test_case_index):
        random_index = random.randint(0, self.chromosome_size - 1)
        if random_index is not test_case_index:
            return random_index
        else:
            return self.swap_test_cases(test_case_index)

    def set_show_each_chromosome(self, boolean):
        self.show_each_chromosome = boolean

    def set_show_fitness_internals(self, boolean):
        self.show_fitness_internals = boolean

    def set_show_crossover_internals(self, boolean):
        self.show_crossover_internals = boolean

    def set_show_mutation_internals(self, boolean):
        self.show_mutation_internals = boolean

    def set_show_duplicate_internals(self, boolean):
        self.show_duplicate_internals = boolean

    def set_silent(self, boolean):
        self.silent = boolean

    def set_stats(self, times, generations, number_of_runs):
        self.mean_time = sum(times) / number_of_runs
        self.mean_generations = sum(generations) / number_of_runs

    def get_stats(self):
        print("\n\nGenetic Algorithm Run  Mean Execution Time: {0:.3f} seconds".format(self.mean_time),
              "     Mean Generations:", int(self.mean_generations), "\n\n\n")
        return self.mean_time

    def check_for_duplicate(self, chromosome):
        duplicate_checker = []
        for faults_combination in chromosome:
            duplicate_checker.append(faults_combination)
        return len(duplicate_checker) != len(set(duplicate_checker))

    def from_fault_matrix_to_test_case(self, chromosome):
        new_chromosome = []
        print("Fault Matrix Chromosome to convert:", chromosome)
        for fault_matrix in chromosome:
            test_case = self.unique_fault_combinations.get(fault_matrix)
            new_chromosome.append(test_case)
        print("Converted Test Case Chromosome:", new_chromosome)
        return new_chromosome

    def from_test_case_to_fault_matrix(self, chromosome):
        new_chromosome = []
        if self.show_fitness_internals: print("Test Case Chromosome to convert:", chromosome)
        for test_case in chromosome:
            fault_matrix = [key for key, value in self.unique_fault_combinations.items() if value == test_case][0]
            new_chromosome.append(fault_matrix)
        if self.show_fitness_internals: print("Converted Fault Matrix Chromosome:", new_chromosome)
        return new_chromosome
