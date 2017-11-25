import urllib.request
import csv


class DataProcessing():
    def __init__(self):
        self.main_url = 'https://docs.google.com/spreadsheets/d/1xCedCs_0njtJ5QJSmSFJ8JJdg8IPh3fDeTZTAsxc93w/gviz/tq?tqx=out:csv&sheet='
        self.index = ['A', 'B', 'C', 'D', 'E', 'F']
        # self.index = ['A']
        self.grade = ['1', '1', '2', '2', '3', '3']
        # self.grade = ['1']
        self.color_data = {}
        self.general_data = {}
        self.get_all_data()

    def get_all_data(self):
        res = {}
        for (a, no) in zip(self.index, self.grade):
            url = self.main_url + a + '_NO_' + no
            res = urllib.request.urlretrieve(url, "log.csv")
            csvf = open('./log.csv', newline='')
            reader = csv.reader(csvf)
            self.general_data[a] = []
            for row in reader:
                if row[17] == '':
                    continue
                res = [row[0]] + row[17:20]
                self.general_data[a].append(res)
            self.general_data[a].pop(0)
            csvf = open('./log.csv', newline='')
            reader = csv.reader(csvf)
            for row in reader:
                if row[2] == '':
                    continue
                for (i, j) in zip(range(2, 15, 3), range(1, 6)):
                    if not a + str(j) in self.color_data:
                        self.color_data[a + str(j)] = []
                    if row[i][0] == 'C':
                        continue
                    res = row[i:i + 3]
                    self.color_data[a + str(j)].append(res)

    def get_general_data(self):
        return self.general_data

    def get_color_data(self):
        return self.color_data


def main():
    DP = DataProcessing()
    DP.get_all_data()


if __name__ == '__main__':
    main()
