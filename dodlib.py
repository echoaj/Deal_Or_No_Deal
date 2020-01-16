
import random
class DealNoDeal:
    def __init__(self):
        self.cases = {'case 1': None, 'case 2': None, 'case 3': None, 'case 4': None, 'case 5': None, 'case 6': None,
                      'case 7': None, 'case 8': None, 'case 9': None, 'case 10': None, 'case 11': None, 'case 12': None,
                      'case 13': None, 'case 14': None, 'case 15': None, 'case 16': None, 'case 17': None, 'case 18': None,
                      'case 19': None, 'case 20': None, 'case 21': None, 'case 22': None, 'case 23': None, 'case 24': None,
                      'case 25': None, 'case 26': None}

        self.values = [0.01, 1, 5, 10, 25, 50, 75, 100, 200, 300, 400, 500, 750, 1000, 5000, 10000, 25000, 50000, 75000, 100000,
                  200000, 300000, 400000, 500000, 750000, 1000000]
        self.values2 = self.values.copy()
        random.shuffle(self.values)
        self.setCases(self.values)
        self.playersCase = 0
        self.offer = 0


    def setCases(self, values):
        count = 0
        for case in self.cases:
            self.cases[case] = values[count]
            count += 1


    def bankOffer(self):
        total = 0
        for case in self.cases:
            total = total + self.cases[case]
        total = total + self.playersCase
        average = round((total / len(self.cases)) * 0.9)
        self.offer = average
        return self.offer                   # Newly added


    def players_choosen_case(self, case_selected):
        self.playersCase = self.cases[case_selected]
        del self.cases[case_selected]


    def remove_cases(self, case_selected):
        del self.cases[case_selected]


    def switch_case(self):
        temp = self.playersCase
        last_case = list(self.cases.keys())[0]          #must convert to list() after
        self.playersCase = self.cases[last_case]
        self.cases[last_case] = temp
        return self.cases[last_case]