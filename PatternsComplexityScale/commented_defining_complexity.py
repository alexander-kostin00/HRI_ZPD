from patterns import pattern_complex
import random
import math


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


# Define a class to handle the complexity analysis of patterns based on white regions within a grid.
class PatternComplexity:
    def __init__(self, pattern):
        """Initialize the PatternComplexity object with the given pattern.

        Args:
            pattern (list of list of int): A 2D list where each element represents a cell in a grid,
                                           typically 0 for unlit and 1 for lit.

        Attributes:
            pattern (list): The grid pattern being analyzed.
            rows (int): The number of rows in the grid.
            columns (int): The number of columns in the grid.
            complexity (float): A numeric value representing the calculated complexity of the pattern.
            unlit_areas (list): A collection of areas (in terms of number of cells) identified as unlit.
            diff_sized_unlit_areas (list): A list of unique sizes of unlit areas.
            already_checked (list of list of bool): A grid to keep track of cells that have been checked.
        """
        self.pattern = pattern
        self.rows = len(pattern)
        self.columns = len(pattern[0])
        self.complexity = 0
        self.unlit_areas = []
        self.diff_sized_unlit_areas = []
        self.already_checked = [[False] * self.columns for _ in range(self.rows)]

    def xy(self, j, i):
        """Check if the coordinates (j, i) are within the grid bounds.

        Args:
            j (int): The column index.
            i (int): The row index.

        Returns:
            list: A two-element list [j, i] if within bounds, otherwise [-1, -1].
        """
        if j < 0 or i < 0 or j >= self.columns or i >= self.rows:
            return [-1, -1]
        return [j, i]

    def get_surrounding(self, j, i, iteration):
        """Retrieve valid surrounding cells for the cell at (j, i) based on the current iteration.

        Args:
            j (int): The column index of the current cell.
            i (int): The row index of the current cell.
            iteration (int): The current iteration number (used to vary the search pattern if necessary).

        Returns:
            list: A list of valid surrounding cell coordinates.
        """
        # Define potential surrounding cells (neighbors)
        surrounding = [
            self.xy(j, i - 1),  # Left
            self.xy(j + 1, i),  # Below
            self.xy(j, i + 1),  # Right
            self.xy(j - 1, i)  # Above
        ]
        # Filter and return only valid coordinates
        return [surr for surr in surrounding if surr[0] != -1]

    def discover_pattern(self, counter, i, j, iteration):
        """Recursively discover the size of an unlit area starting from cell (i, j).

        Args:
            counter (int): The current count of contiguous unlit cells.
            i (int): The row index.
            j (int): The column index.
            iteration (int): The iteration number for varying the search pattern.

        Returns:
            int: The total count of contiguous unlit cells connected to the starting cell.
        """
        if self.already_checked[i][j]:
            return 0  # If already checked, return 0 to prevent double counting
        self.already_checked[i][j] = True  # Mark this cell as checked
        counter += 1  # Increment the counter for each unlit cell found

        # Get valid surrounding cells and continue the search
        surr = self.get_surrounding(j, i, iteration)
        for h in surr:
            if self.pattern[h[1]][h[0]] == 0:
                counter += self.discover_pattern(counter, h[1], h[0], iteration)
        return counter

    def define_complexity(self):
        """Calculate the complexity of the pattern based on unlit areas.

        Returns:
            float: The complexity level calculated from unlit areas and their distribution.
        """
        # Iterate over all cells in the grid
        for i in range(self.rows):
            for j in range(self.columns):
                if self.pattern[i][j] == 0:
                    # Explore each unlit area from each direction if needed
                    for iteration in range(4):
                        counter_overload = self.discover_pattern(0, i, j, iteration)
                        counter = find_largest_component(counter_overload)
                        self.unlit_areas.append(counter)
        # Filter and identify unique unlit area sizes
        self.unlit_areas = filter_list(self.unlit_areas)
        self.diff_sized_unlit_areas = unique_sizes(self.unlit_areas)

        # Calculate complexity based on the number of unique unlit area sizes and their frequency
        amount_unlit_areas = len(self.unlit_areas)
        amount_diff_sized_unlit_areas = len(self.diff_sized_unlit_areas)
        scaling_factor = 0.5  # Adjust this factor to scale the impact of diverse area sizes on complexity

        # Define complexity as a combination of total unlit areas and differentiated sizes
        self.complexity = amount_unlit_areas + scaling_factor * amount_diff_sized_unlit_areas
        return self.complexity


# Main function to initialize pattern complexity calculation and display results
def main(pattern):
    pattern_complexity = PatternComplexity(pattern)
    complexity_level = pattern_complexity.define_complexity()

    print('All unlit areas: ' + str(pattern_complexity.unlit_areas))
    print('Only differently sized unlit areas: ' + str(pattern_complexity.diff_sized_unlit_areas))
    print('Pattern complexity level is : ' + str(complexity_level))


if __name__ == '__main__':
    main(pattern_complex)
