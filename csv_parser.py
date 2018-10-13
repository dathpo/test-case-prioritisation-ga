__author__ = 'David T. Pocock'

import csv
import os.path


class CSVParser:

    def __init__(self, file_name):
        self.file_name = file_name

    def parse(self):
        pwd = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(pwd, self.file_name)
        unique_fault_combinations = {}
        test_cases = []
        with open(path, newline='') as file:
            matrix_reader = csv.reader(file)
            for row in reversed(list(matrix_reader)):
                faults_revealed = []
                for element in row[1:]:
                    inted = int(element)
                    faults_revealed.append(inted)
                unique_fault_combinations[tuple(faults_revealed)] = row[0]
            for key in unique_fault_combinations.keys():
                test_case = (unique_fault_combinations.get(key), list(key))
                test_cases.append(test_case)
        return test_cases
