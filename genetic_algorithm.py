__author__ = 'David T. Pocock'


import random, string, timeit
from operator import itemgetter


class GeneticAlgorithm:
    show_each_chromosome = None
    show_crossover_internals = None
    show_mutation_internals = None
    silent = None
    mean_time = None
    mean_generations = None
    failed = False

    def __init__(self, test_cases, chromosome_size, population_size, number_of_generations, crossover_rate, mutation_rate,
                 is_k_point_crossover, tournament_size_percent, strongest_winner_probability):
        self.test_cases = test_cases
        self.chromosome_size = chromosome_size
        self.population_size = population_size
        self.number_of_generations = number_of_generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.is_k_point_crossover = is_k_point_crossover
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
            if self.show_each_chromosome: print("Fitness (APFD)      Chromosome          Generation\n")
            for i in range(0, self.number_of_generations):
                generation_number += 1
                # if generation_number > 499:
                #     self.failed = True
                #     print("\nThe Genetic Algorithm failed, as the target string was not reached after 500 generations\n")
                #     break
                winners = self.selection(population)
                pre_mutation_generation = self.check_for_crossover(winners)
                new_generation = self.mutate(pre_mutation_generation)
                population = new_generation
                counter = 0
                for chromosome in population:
                    counter += 1
                    fitness_value = self.fitness(chromosome, "TARGET STRING, NEEDS TO CHANGE")
                    if counter == 1:
                        fittest_chromosome = chromosome, fitness_value
                    if self.show_each_chromosome:
                        print("       {}            {}            {}"
                              .format(str(fitness_value).rjust(2), chromosome.rjust(2), str(generation_number).rjust(2)))
                    if fitness_value <= fittest_chromosome[1]:
                        fittest_chromosome = chromosome, fitness_value
                        if fitness_value == 0:
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
        # for i in range(0, size):
        #     chromosome = []
        #     for j in range(0, self.chromosome_size):
        #         self.populate(j, chromosome)
        #     population.append(chromosome)
        chromosome = []
        chromosome.append(('t1', [True, False, False, False, False]))
        chromosome.append(('t5', [False, False, False, False, False]))
        chromosome.append(('t2', [False, False, True, False, True]))
        chromosome.append(('t4', [True, False, False, True, False]))
        # chromosome.append(('t3', [False, True, False, False, False]))
        # chromosome.append(('t6', [False, False, False, False, True]))
        population.append(chromosome)
        return population

    def populate(self, j, chromosome):
        random_index = random.randint(0, len(self.test_cases) - 1)
        chromosome.append(self.test_cases[random_index])
        if j > 0:
            if self.check_for_duplicate(chromosome):
                chromosome.pop()
                self.populate(j, chromosome)

    def fitness(self, chromosome):
        weight = 0
        number_of_test_cases = self.chromosome_size
        number_of_faults = len(chromosome[0][1])
        # print(chromosome)
        for i in range(0, number_of_faults):
            for j in range(0, number_of_test_cases):
                # print(chromosome[j][1][i], j )
                if chromosome[j][1][i]:
                    weight += j+1
                    break
                if j == self.chromosome_size - 1:
                    weight += number_of_test_cases + 1
        apfd = 1 - (weight/(number_of_faults * number_of_test_cases)) + 1/(2 * number_of_test_cases)
        # print("weight:", weight, "APFD:", apfd, "no faults:", number_of_faults, "no test cases:", number_of_test_cases)
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
            for participant_str in range(0, self.tournament_size()):
                random_index = random.randint(0, len(population) - 1)
                participant = population[random_index]
                participant_fitness = self.fitness(participant)
                participant_evaluated = participant, participant_fitness
                participants.append(participant_evaluated)
            if self.decision(self.strongest_winner_prob()):
                winner = min(participants, key=itemgetter(1))
                winners.append(winner)
            elif self.decision(self.strongest_winner_prob()):
                temp_participant = min(participants, key=itemgetter(1))
                participants.remove(temp_participant)
                winner = min(participants, key=itemgetter(1))
                winners.append(winner)
                participants.append(temp_participant)
            else:
                first_temp_participant = min(participants, key=itemgetter(1))
                participants.remove(first_temp_participant)
                second_temp_participant = min(participants, key=itemgetter(1))
                participants.remove(second_temp_participant)
                winner = min(participants, key=itemgetter(1))
                winners.append(winner)
                participants.append(first_temp_participant)
                participants.append(second_temp_participant)
        winners_strings = [str[0] for str in winners]
        paired_winners = list(zip(winners_strings[0::2], winners_strings[1::2]))
        return paired_winners

    def check_for_crossover(self, parents):
        new_generation = []
        for first_parent, second_parent in parents:
            if self.decision(self.crossover_rate):
                children_duo = self.crossover(first_parent, second_parent, self.is_k_point_crossover)
                for child in children_duo:
                    new_generation.append(child)
            else:
                new_generation.append(first_parent)
                new_generation.append(second_parent)
        return new_generation

    def crossover(self, first_parent, second_parent, is_k_point_crossover):
        if is_k_point_crossover: crossover_method = "k-Point Crossover"
        else: crossover_method = "One-Point Crossover"
        if self.show_crossover_internals:
            print("\nParent #1:", first_parent, "      Parent #2:", second_parent, "      Crossover Method:", crossover_method)
        first_child_char_array = []
        second_child_char_array = []
        i = 0
        point = int(self.crossover_point() * (len("TARGET STRING, NEEDS TO CHANGE") - 1)) + 1
        points = []
        for char_a, char_b in zip(first_parent, second_parent):
            i += 1
            if is_k_point_crossover:
                point = int(self.crossover_point() * (len("TARGET STRING, NEEDS TO CHANGE") - 1)) + 1
                points.append(point)
            if i <= point:
                first_child_char_array.append(char_a)
                second_child_char_array.append(char_b)
            else:
                first_child_char_array.append(char_b)
                second_child_char_array.append(char_a)
        first_child = ''.join(first_child_char_array)
        second_child = ''.join(second_child_char_array)
        if self.show_crossover_internals:
            if is_k_point_crossover:
                print("Child #1: ", first_child, "      Parent #2:", second_child,
                      "      Crossover Point at multiple points")
            else:
                print("Child #1: ", first_child, "      Parent #2:", second_child,
                      "      Crossover Point after character #{}".format(point))
        return first_child, second_child

    def mutate(self, generation):
        """I left the print statements in to allow seeing how the bit-flipping works in the mutation process"""
        new_generation = []
        for chromosome in generation:
            if self.show_mutation_internals: print("\nChromosome being worked on:  ", chromosome, "\n")
            chromosome_bit_array = []
            for char in chromosome:
                binary_char = bin(ord(char))
                if self.show_mutation_internals: print("Char:    ", char, "   ASCII #:", ord(char), "   Binary Char:", binary_char)
                new_binary_char_array = ['0', 'b', '1']
                for bit in binary_char[3:]:
                    if self.decision(self.mutation_rate):
                        flipped_bit = int(bit) ^ 1
                        if self.show_mutation_internals: print("Bit:     ", str(bit), "   Flipped Bit:", str(flipped_bit))
                        new_binary_char_array.append(str(flipped_bit))
                    else:
                        if self.show_mutation_internals: print("Bit:     ", str(bit))
                        new_binary_char_array.append(str(bit))
                new_binary_char = ''.join(new_binary_char_array)
                if self.show_mutation_internals:
                    print("New Char:", chr(int(new_binary_char, 2)), "   ASCII #:",
                          int(new_binary_char, 2), "   Binary Char:", new_binary_char, "\n")
                chromosome_bit_array.append(new_binary_char)
            new_chromosome = self.bit_array_to_string(chromosome_bit_array)
            if self.show_mutation_internals:
                print("Chromosome pre-mutation:   ", chromosome)
                print("Chromosome post-mutation:  ", new_chromosome, "\n")
            new_generation.append(new_chromosome)
        return new_generation

    def bit_array_to_string(self, array):
        char_array = []
        for bit in array:
            char = chr(int(bit, 2))
            char_array.append(char)
        str = ''.join(char_array)
        return str

    def set_show_each_chromosome(self, boolean):
        self.show_each_chromosome = boolean

    def set_show_crossover_internals(self, boolean):
        self.show_crossover_internals = boolean

    def set_show_mutation_internals(self, boolean):
        self.show_mutation_internals = boolean

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
        for test_case, faults in chromosome:
            duplicate_checker.append(test_case)
        return len(duplicate_checker) != len(set(duplicate_checker))

        # if len(chromosome) != len(set(chromosome))

    #     return
    #print(chromosome[0])