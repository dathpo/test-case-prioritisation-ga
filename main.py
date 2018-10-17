__author__ = 'David T. Pocock'


from hill_climbing import HillClimbing
from random_search import RandomSearch
from genetic_algorithm import GeneticAlgorithm
from csv_parser import CSVParser
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os.path


def main():
    runs = 10
    rounds = 5
    chromosome_size = 23
    population_size = 1000
    data_set_name = 'bigfaultmatrix.txt'

    pwd = os.path.abspath(os.path.dirname(__file__))
    data_set_path = os.path.join(pwd, data_set_name)
    parser = CSVParser(data_set_path)
    test_case_fault_matrix = parser.parse_data(True)

    ga = GeneticAlgorithm(test_case_fault_matrix, chromosome_size, population_size, rounds, 0.8, 0.08, 0.05, 0.75)
    ga.set_show_each_chromosome(False)
    ga.set_show_fitness_internals(False)
    ga.set_show_crossover_internals(False)
    ga.set_show_mutation_internals(False)
    ga.set_show_duplicate_internals(False)
    ga.set_silent(True)
    ga.run(runs)
    ga_fitness = ga.get_stats()

    for i in range(0, 2):
        if i == 0:
            hc = HillClimbing(test_case_fault_matrix, chromosome_size, population_size, rounds, False)
        else:
            hc = HillClimbing(test_case_fault_matrix, chromosome_size, population_size, rounds, True)
        hc.set_show_each_solution(False)
        hc.set_show_fitness_internals(False)
        hc.set_show_swapping_internals(False)
        hc.set_silent(True)
        hc.run(runs)
        if i == 0: hc_internal_fitness = hc.get_stats()
        else: hc_external_fitness = hc.get_stats()

    rs = RandomSearch(test_case_fault_matrix, chromosome_size, population_size, rounds)
    rs.set_show_each_solution(False)
    rs.set_silent(True)
    rs.run(runs)
    rs_fitness = rs.get_stats()

    rs_data = np.array(rs_fitness)
    hs_internal = np.array(hc_internal_fitness)
    hs_external = np.array(hc_external_fitness)
    ga_data = np.array(ga_fitness)

    # test_cases_per_test_suite = np.array([5, 10, 20, 23, 30, 50, 100])
    # unique_large_apfd = np.array([0.4594736842105263, 0.6063157894736844, 0.6867105263157895, 0.6978260869565216, 0.7128947368421051, 0.7326842105263159, 0.7480263157894737])
    # full_large_apfd = np.array([0.44631578947368417, 0.6023684210526316, 0.6846052631578947, 0.6958810068649884, 0.7122807017543858, 0.7320526315789474, 0.7476578947368421])

    # plt.plot(test_cases_per_test_suite, unique_large_apfd, '-gD')
    # plt.xlabel("Test Cases per Test Suite")
    # plt.ylabel("Mean Fitness (APFD)")
    # plt.xticks(np.arange(min(test_cases_per_test_suite), max(test_cases_per_test_suite) + 1, 5.0))

    ## combine these different collections into a list
    data_to_plot = [rs_data, hs_internal, hs_external, ga_data]

    # Create a figure instance
    fig = plt.figure(1, figsize=(9, 6))

    # Create an axes instance
    ax = fig.add_subplot(111)

    ## add patch_artist=True option to ax.boxplot()
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
    graph_path = os.path.join(pwd, 'graph.pdf')
    pdf = PdfPages(graph_path)
    plt.savefig(pdf, format='pdf', bbox_inches='tight')
    plt.show()
    pdf.close()
    pdf = None

if __name__ == "__main__":
    main()
