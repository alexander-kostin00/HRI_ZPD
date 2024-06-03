"""
Author: Oleksandr Kostin
"""

from patterns import pattern_easy, pattern_complex, pattern_middle

def amount_lit(pattern):
    amount_lit = 0
    for i in pattern:
        for j in i:
            if j == 1:
                amount_lit += j
    return amount_lit


def amount_all(pattern):
    amount_all = len(pattern) * len(pattern[0])
    return amount_all


def find_largest_component(target):
    sum_of_numbers = 0
    n = 0

    while True:
        n += 1
        sum_of_numbers += n
        if sum_of_numbers > target:
            return n - 1
        elif sum_of_numbers == target:
            return n

def filter_list(original_list):
    filtered_list = [element for element in original_list if element != 0]
    return filtered_list

def unique_sizes(original_list):
    unique_sizes = list(set(original_list))
    return unique_sizes

class PatternComplexity:
    def __init__(self, pattern):
        self.pattern = pattern
        self.rows = len(pattern)
        self.columns = len(pattern[0])
        self.complexity = 0
        self.unlit_areas = []
        self.diff_sized_unlit_areas = []
        self.already_checked = [[False] * self.columns for _ in range(self.rows)]

    def xy(self, j, i):
        if j < 0 or i < 0 or j >= self.columns or i >= self.rows:
            return [-1, -1]
        return [j, i]

    def get_surrounding(self, j, i, iteration):
        if iteration == 0:
            surrounding = [
                #to write if conditions for at first 4 combinations
                self.xy(j, i - 1), self.xy(j + 1, i), self.xy(j, i + 1), self.xy(j - 1, i)
            ]
        elif iteration == 1:
            surrounding = [
                self.xy(j, i - 1),  self.xy(j, i + 1), self.xy(j + 1, i), self.xy(j - 1, i)
            ]
        elif iteration == 2:
            surrounding = [
                self.xy(j - 1, i), self.xy(j, i - 1), self.xy(j + 1, i), self.xy(j, i + 1)
            ]
        elif iteration == 3:
            surrounding = [
                 self.xy(j + 1, i), self.xy(j, i + 1), self.xy(j - 1, i), self.xy(j, i - 1)
            ]

        return [surr for surr in surrounding if surr[0] != -1]

    def discover_pattern(self, counter, i, j, iteration):
        if self.already_checked[i][j]:
            return 0
        self.already_checked[i][j] = True
        counter += 1

        surr = self.get_surrounding(j, i, iteration)
        for h in surr:
            if self.pattern[h[1]][h[0]] == 0:
                counter += self.discover_pattern(counter, h[1], h[0], iteration)
        return counter

    def define_complexity(self, scaling_factor):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.pattern[i][j] == 0:
                    counters = []
                    for iteration in range(4):
                        counter_overload = self.discover_pattern(0, i, j, iteration)
                        counter = find_largest_component(counter_overload)
                        counters.append(counter)

                    counter = max(counters)
                    self.unlit_areas.append(counter)
        self.unlit_areas = filter_list(self.unlit_areas)

        self.diff_sized_unlit_areas = unique_sizes(self.unlit_areas)

        amount_unlit_areas = len(self.unlit_areas)
        amount_diff_sized_unlit_areas = len(self.diff_sized_unlit_areas)

        self.complexity = amount_unlit_areas + scaling_factor * amount_diff_sized_unlit_areas

        return self.complexity


def main(pattern):
    pattern_complexity = PatternComplexity(pattern)

    scaling_factor = 1

    complexity_level = pattern_complexity.define_complexity(scaling_factor)

    print('All unlit areas: ' + str(pattern_complexity.unlit_areas))

    print('Only differently sized unlit areas: ' + str(pattern_complexity.diff_sized_unlit_areas))

    print('Pattern complexity level is : ' + str(complexity_level))



if __name__ == '__main__':
    main(pattern_complex)



