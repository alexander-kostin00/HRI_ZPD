"""
Author: Oleksandr Kostin
"""

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QFileDialog, QMessageBox, QCheckBox
from PIL import Image
import itertools
import random
import time
import math
import sys
sys.setrecursionlimit(50000)  # Increase the recursion limit to handle deep recursion

class CreatingPatterns:
    def __init__(self, rows, columns, complexity_level, scaling_factor, merge):
        # Initialize class attributes
        self.merge = merge
        self.rows = rows
        self.columns = columns
        self.complexity_level = complexity_level
        self.scaling_factor = scaling_factor
        self.boundaries = []
        self.merge_boundaries = []

    # Create a matrix filled with 1s (lit image)
    def create_lit_image(self, columns, rows):
        matrix = []
        for i in range(rows):
            row = []
            for j in range(columns):
                row.append(1)
            matrix.append(row)

        return matrix

    def find_valid_combinations(self, complexity_level, scaling_factor, precise):
        valid_combinations = []

        for amount_unlit_areas in range(0, 10):
            for amount_diff_sized_areas in range(1, amount_unlit_areas + 1):
                if not precise:
                    if round(amount_unlit_areas + scaling_factor * amount_diff_sized_areas) == complexity_level:
                        valid_combinations.append([amount_unlit_areas, amount_diff_sized_areas])
                else:
                    if (amount_unlit_areas + scaling_factor * amount_diff_sized_areas) == complexity_level:
                        valid_combinations.append([amount_unlit_areas, amount_diff_sized_areas])

        print("Valid combinations:")
        for combination in valid_combinations:
            print(combination)

        print("Pseudo random chosen combination:")
        if len(valid_combinations) == 0:
            print("No available combinations...")
        else:
            rand_comb = random.choice(valid_combinations)
            print(rand_comb)

        return rand_comb

    def generate_unlit_regions(self, amount_unlit_areas, amount_diff_sized_areas, lit_image, target_sum):
        ATTEMPTS = 0
        while True:
            random_values = []
            current_sum = 0
            limit = int((min(len(lit_image), len(lit_image[0])) / 3) ** 2)
            # Generate unique values
            attempts = 0
            if amount_unlit_areas == amount_diff_sized_areas:
                while len(random_values) < amount_unlit_areas and attempts < 1000:
                    random_integer = random.randint(1, limit + 1)

                    if random_integer not in random_values:
                        random_values.append(random_integer)
                        current_sum += random_integer
                    if (target_sum - current_sum) <= limit:
                        final = target_sum - current_sum
                        random_values.append(final)
                        current_sum += final
                        return random_values
                    if current_sum == target_sum and len(random_values) == amount_unlit_areas:
                        return random_values
                    attempts += 1
                return random_values
            else:
                attempts = 0
                while len(random_values) < amount_diff_sized_areas and attempts < 500:
                    random_integer = random.randint(1, limit + 1)

                    if random_integer not in random_values:
                        random_values.append(random_integer)
                        current_sum += random_integer
                    if (int(2 / 3 * target_sum) - current_sum) <= limit:
                        final = int(2 / 3 * target_sum) - current_sum
                        random_values.append(final)
                        current_sum += final
                        break
                    if (current_sum == int(2 / 3 * target_sum)) and len(random_values) == amount_diff_sized_areas:
                        break
                    attempts += 1

                attempts = 0
                random_integer = random.choice(random_values)
                while len(random_values) < amount_unlit_areas and attempts < 500:
                    random_values.append(random_integer)
                    current_sum += random_integer

                    if (current_sum <= target_sum + 1 and current_sum >= target_sum - 1) and len(random_values) == amount_unlit_areas:
                        print("Unlit regions:")
                        print(random_values)
                        return random_values
                    attempts += 1
                return random_values
            ATTEMPTS += 1
            print("ATTEMPT:" + str(ATTEMPTS))

    def random_coordinates(self, lit_image):
        r_col = random.randint(0, len(lit_image[0]) - 1)
        r_row = random.randint(0, len(lit_image) - 1)
        return [r_row, r_col]

    def xy(self, row, column, image):
        if column < 0 or row < 0 or column >= len(image[0]) or row >= len(image):
            return [-1, -1]
        for bound in self.boundaries:
            if (column >= bound[0] and column <= bound[2]) and (row >= bound[1] and row <= bound[3]):
                return [-1, -1]
        return [row, column]

    def check_region(self, start_row, start_column, area, image):
        side_length = int(math.sqrt(area))

        for i in range(side_length):
            for j in range(side_length):
                point = self.xy(start_row + i, start_column + j, image)
                if point[0] == -1:
                    return False

        return True

    def make_unlit_region(self, start_row, start_column, area, image):
        side_length = int(math.sqrt(area))

        for i in range(side_length):
            for j in range(side_length):
                image[start_row + i][start_column + j] = 0
        return image

    def make_unlit_region_merge(self, merge_boundaries, image):
        for rect in merge_boundaries:
            left, top, right, bottom = rect
            for row in range(top, bottom + 1):
                for col in range(left, right + 1):
                    image[row][col] = 0

        return image

    def print_matrix(self, matrix):
        for row in matrix:
            print(" ".join(map(str, row)))

    def fill_image(self, image, unlit_areas, time_limit=2):
        for area in unlit_areas:
            side_length = int(math.sqrt(area))
            available = False
            start_time = time.time()

            while not available:
                if time.time() - start_time > time_limit:
                    raise TimeoutError(f"Time limit of {time_limit} seconds exceeded while finding available region.")

                r_coordinates = self.random_coordinates(image)

                available = self.check_region(r_coordinates[0], r_coordinates[1], area, image)

                if available:
                    image = self.make_unlit_region(r_coordinates[0], r_coordinates[1], area, image)
                    self.boundaries.append([r_coordinates[1], r_coordinates[0], r_coordinates[1] + side_length - 1, r_coordinates[0] + side_length - 1])
                    print(self.boundaries)

        if self.merge:
            self.make_merge_boundaries()
            image = self.make_unlit_region_merge(self.merge_boundaries, image)

        return image

    def make_merge_boundaries(self):
        comb = list(itertools.product(range(len(self.boundaries)), repeat=2))
        unique_comb = [pair for pair in comb if pair[0] < pair[1]]
        print(unique_comb)
        combinations = [[self.boundaries[i], self.boundaries[j]] for i, j in unique_comb]
        print(combinations)

        for pair in combinations:
            vec1, vec2 = pair
            differences = [abs(vec1[i] - vec2[(i + 2) % 4]) for i in range(4)]
            print(differences)

            # Check if any differences are less than the threshold
            for i, diff in enumerate(differences):
                if diff < 50:
                    if i % 2 == 0:  # Even indices (0 and 2)
                        # Assign values to b and d
                        b = max(vec1[1], vec2[1])
                        d = min(vec1[3], vec2[3])
                        if b >= d:
                            continue
                        # Assign values to a and c
                        a = min(vec1[0], vec2[0])
                        c = max(vec1[2], vec2[2])
                        if a >= c:
                            continue
                    else:  # Odd indices (1 and 3)
                        # Assign values to a and c
                        a = min(vec1[2], vec2[2])
                        c = max(vec1[0], vec2[0])
                        if a >= c:
                            continue
                        # Assign values to b and d
                        b = max(vec1[1], vec2[1])
                        d = min(vec1[3], vec2[3])
                        if b >= d:
                            continue

                    self.merge_boundaries.append([a, b, c, d])
                    # break
        print('MERGE boundaries: ' + str(self.merge_boundaries))

    def count_zeros_in_matrix(self, matrix):
        zero_count = 0  # Initialize a counter for zeros
        for row in matrix:  # Iterate over each row in the matrix
            for element in row:  # Iterate over each element in the row
                if element == 0:  # Check if the element is zero
                    zero_count += 1  # Increment the counter if it's zero
        return zero_count

    def matrix_to_image(self, matrix, filename):
        image = Image.new('1', (len(matrix[0]), len(matrix)))

        pixels = image.load()

        for i in range(image.size[1]):
            for j in range(image.size[0]):
                pixels[j, i] = 0 if matrix[i][j] == 1 else 1

        image.save(filename)


class PatternApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Pattern Generator')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.complexity_input = QLineEdit(self)
        self.complexity_input.setPlaceholderText('Complexity Level (e.g. 10)')
        layout.addWidget(self.complexity_input)

        self.scaling_factor_input = QLineEdit(self)
        self.scaling_factor_input.setPlaceholderText('Scaling Factor (e.g. 0.2)')
        layout.addWidget(self.scaling_factor_input)

        self.columns_input = QLineEdit(self)
        self.columns_input.setPlaceholderText('Columns (e.g. 3000)')
        layout.addWidget(self.columns_input)

        self.rows_input = QLineEdit(self)
        self.rows_input.setPlaceholderText('Rows (e.g. 3000)')
        layout.addWidget(self.rows_input)

        self.output_path_input = QLineEdit(self)
        self.output_path_input.setPlaceholderText('Output Path')
        layout.addWidget(self.output_path_input)

        self.browse_button = QPushButton('Browse', self)
        self.browse_button.clicked.connect(self.browse_file)
        layout.addWidget(self.browse_button)

        self.merge_checkbox = QCheckBox("merging", self)
        self.merge_checkbox.setChecked(False)
        layout.addWidget(self.merge_checkbox)

        self.generate_button = QPushButton('Generate Pattern', self)
        self.generate_button.clicked.connect(self.generate_pattern)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)

    def browse_file(self):
        file, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'PNG Files (*.png);;All Files (*)')
        if file:
            self.output_path_input.setText(file)

    def generate_pattern(self):
        try:
            complexity_level = int(self.complexity_input.text())
            scaling_factor = float(self.scaling_factor_input.text())
            columns = int(self.columns_input.text())
            rows = int(self.rows_input.text())
            output_path = self.output_path_input.text()
            merge = self.merge_checkbox.isChecked()
            retry_count = 0
            max_retries = 500

            while retry_count < max_retries:
                try:
                    creating_patterns = CreatingPatterns(rows, columns, complexity_level, scaling_factor, merge)
                    rand_comb = creating_patterns.find_valid_combinations(complexity_level, scaling_factor, False)

                    if not rand_comb:
                        QMessageBox.critical(self, 'Error', 'No valid combinations found.')
                        return

                    lit_image = creating_patterns.create_lit_image(columns, rows)
                    target_sum = round((len(lit_image) * len(lit_image[0])) / 3)
                    unlit_areas = creating_patterns.generate_unlit_regions(rand_comb[0], rand_comb[1], lit_image, target_sum)

                    filled_image = creating_patterns.fill_image(lit_image, unlit_areas)
                    print("Filled Image:")
                    creating_patterns.print_matrix(filled_image)

                    creating_patterns.matrix_to_image(filled_image, output_path)

                    QMessageBox.information(self, 'Success', f'Pattern generated and saved to {output_path}')
                    break

                except Exception as e:
                    print(str(e))
                    retry_count += 1
                    if retry_count >= max_retries:
                        QMessageBox.critical(self, 'Error', 'Maximum retries exceeded. Could not generate pattern.')

        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))


def main():
    app = QApplication(sys.argv)
    ex = PatternApp()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
