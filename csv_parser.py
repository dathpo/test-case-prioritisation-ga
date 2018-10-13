__author__ = 'David T. Pocock'


import csv
import os.path


class CSVParser:

    def __init__(self, file_name):
        self.file_name = file_name

    def parse(self):
        pwd = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(pwd, self.file_name)
        test_case_dict = {}
        counter = 0
        with open(path, newline='') as file:
            matrix_reader = csv.reader(file)
            for row in matrix_reader:
                faults_revealed = []
                for element in row[1:]:
                    booled = int(element)
                    faults_revealed.append(booled)
                print(counter, tuple(faults_revealed))
                test_case_dict[tuple(faults_revealed)] = row[0]
                counter += 1
            print(len(test_case_dict))
        return test_case_dict
