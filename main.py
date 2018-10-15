__author__ = 'David T. Pocock'


from hill_climbing import HillClimbing
from random_search import RandomSearch
from genetic_algorithm import GeneticAlgorithm
from csv_parser import CSVParser
import numpy as np
import matplotlib as mpl
# mpl.use('agg')
import matplotlib.pyplot as plt


def main():
    runs = 100
    rounds = 20
    chromosome_size = 5
    population_size = 120

    parser = CSVParser('smallfaultmatrix.txt')
    test_case_fault_matrix = parser.parse_unique()

    ga = GeneticAlgorithm(test_case_fault_matrix, chromosome_size, population_size, rounds, 0.8, 0.08, 0.05, 0.75)
    ga.set_show_each_chromosome(False)
    ga.set_show_fitness_internals(False)
    ga.set_show_crossover_internals(False)
    ga.set_show_mutation_internals(False)
    ga.set_show_duplicate_internals(False)
    ga.set_silent(True)
    ga.run(runs)
    ga_fitness = ga.get_stats()

    hc = HillClimbing(test_case_fault_matrix, chromosome_size, population_size, rounds, False)
    hc.set_show_each_solution(False)
    hc.set_show_fitness_internals(False)
    hc.set_show_swapping_internals(False)
    hc.set_silent(True)
    hc.run(runs)
    hc_internal_fitness = hc.get_stats()

    hc = HillClimbing(test_case_fault_matrix, chromosome_size, population_size, rounds, True)
    hc.set_show_each_solution(False)
    hc.set_show_fitness_internals(False)
    hc.set_show_swapping_internals(False)
    hc.set_silent(True)
    hc.run(runs)
    hc_external_fitness = hc.get_stats()

    rs = RandomSearch(test_case_fault_matrix, chromosome_size, population_size, rounds)
    rs.set_show_each_solution(False)
    rs.set_silent(True)
    rs.run(runs)
    rs_fitness = rs.get_stats()

    # np.random.seed(10)
    # collectn_1 = np.random.normal(100, 10, 200)
    # collectn_2 = np.random.normal(80, 30, 200)
    # collectn_3 = np.random.normal(90, 20, 200)
    # collectn_4 = np.random.normal(70, 25, 200)

    rs_data = np.array(rs_fitness)
    hs_internal = np.array(hc_internal_fitness)
    hs_external = np.array(hc_external_fitness)
    ga_data = np.array(ga_fitness)

    ## combine these different collections into a list
    # data_to_plot = [collectn_1, collectn_2, collectn_3, collectn_4]
    data_to_plot = [rs_data, hs_internal, hs_external, ga_data]


    # Create a figure instance
    fig = plt.figure(1, figsize=(9, 6))

    # Create an axes instance
    ax = fig.add_subplot(111)

    ## add patch_artist=True option to ax.boxplot()
    ## to get fill color
    bp = ax.boxplot(data_to_plot, patch_artist=True)

    ## change outline color, fill color and linewidth of the boxes
    for box in bp['boxes']:
        # change outline color
        box.set(color='#7570b3', linewidth=2)
        # change fill color
        box.set(facecolor='#1b9e77')

    ## change color and linewidth of the whiskers
    for whisker in bp['whiskers']:
        whisker.set(color='#7570b3', linewidth=2)

    ## change color and linewidth of the caps
    for cap in bp['caps']:
        cap.set(color='#7570b3', linewidth=2)

    ## change color and linewidth of the medians
    for median in bp['medians']:
        median.set(color='#b2df8a', linewidth=2)

    ## change the style of fliers and their fill
    for flier in bp['fliers']:
        flier.set(marker='o', color='#e7298a', alpha=0.5)

    ## Custom x-axis labels
    ax.set_xticklabels(['Random Search', 'HC Internal Swap', 'HC External Swap', 'Genetic Algorithm'])

    ## Remove top axes and right axes ticks
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    # Save the figure
    fig.savefig('fig1.png', bbox_inches='tight')

    plt.show()


if __name__ == "__main__":
    main()
