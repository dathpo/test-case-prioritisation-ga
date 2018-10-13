__author__ = 'David T. Pocock'


import csv
import os.path


class CSVParser:

    def __init__(self, file_name):
        self.file_name = file_name

    def parse(self):
        pwd = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(pwd, self.file_name)
        test_cases = []
        with open(path, newline='') as file:
            matrix_reader = csv.reader(file)
            for row in matrix_reader:
                faults_revealed = []
                for element in row[1:]:
                    booled = bool(int(element))
                    faults_revealed.append(booled)
                test_cases.append((row[0], faults_revealed))
        return test_cases
