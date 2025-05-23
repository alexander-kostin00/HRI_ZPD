"""
Author: Oleksandr Kostin
"""

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QFileDialog, QMessageBox, QCheckBox
from PatternsComplexityScale.creating_patterns.creating_patterns import CreatingPatterns
from PIL import Image, ImageDraw, ImageFont
import shutil
import os
import re
import sys
sys.setrecursionlimit(50000)  # Increase the recursion limit to handle deep recursion

def get_largest_image_number(directory):
    # This function finds the largest image number in the directory
    image_files = [
        f
        for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f)) and f.startswith("image_")
    ]
    numbers = [
        int(re.search(r"image_(\d+)", f).group(1)) for f in image_files if re.search(r"image_(\d+)", f)
    ]
    return max(numbers, default=0)

def write_report(output_directory, amount, complexity_level, scaling_factor):
    report_path = os.path.join(output_directory, "report.txt")
    with open(report_path, "a") as report_file:
        report_file.write(
            f"{amount} images: complexity level - {complexity_level}, scaling factor - {scaling_factor}\n"
        )

def create_patterns(amount=5, complexity_level=6, scaling_factor=0.1, rows=500, columns=500, merge=True, output_directory_path='patterns_uncovered', with_numbers = True):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory_path):
        os.makedirs(output_directory_path)

    # Get the current largest image number in the directory
    largest_number = get_largest_image_number(output_directory_path)
    print(f"Continuing from image number: {largest_number}")

    counter_numbers = largest_number
    counter = largest_number
    if with_numbers:
        for i in range(1, 2 * amount + 1):
            if i % 2 != 0:
                try:
                    # Create the number image
                    number_image = Image.new('RGB', (columns, rows), color='black')
                    draw = ImageDraw.Draw(number_image)
                    number_font_size = min(columns, rows) // 2

                    try:
                        # Try to use a truetype font if available
                        font = ImageFont.truetype("DejaVuSans.ttf", number_font_size)
                    except IOError as e:
                        print('Error:', str(e))
                        break

                    text = str(counter_numbers + 1)
                    text_width, text_height = draw.textsize(text, font=font)
                    text_x = (columns - text_width) // 2
                    text_y = (rows - text_height) // 2
                    draw.text((text_x, text_y), text, fill='white', font=font)
                    number_output_path = f'{output_directory_path}/image_{counter + 1}.png'
                    number_image.save(number_output_path)
                    print(f'Success: Number image generated and saved to {number_output_path}.')

                    counter += 1
                    counter_numbers += 1

                except Exception as e:
                    print('Error:', str(e))
                    break
            else:
                try:
                    retry_count = 0
                    max_retries = 500

                    while retry_count < max_retries:
                        try:
                            creating_patterns = CreatingPatterns(rows, columns, complexity_level, scaling_factor, merge)
                            rand_comb = creating_patterns.find_valid_combinations(complexity_level, scaling_factor, False)

                            if not rand_comb:
                                print('Error', 'No valid combinations found.')
                                print(str(counter_numbers) + ' images have been generated for now.')
                                return

                            # Create the pattern image
                            lit_image = creating_patterns.create_lit_image(columns, rows)
                            target_sum = round((len(lit_image) * len(lit_image[0])) / 3)
                            unlit_areas = creating_patterns.generate_unlit_regions(rand_comb[0], rand_comb[1], lit_image, target_sum)
                            filled_image = creating_patterns.fill_image(lit_image, unlit_areas)
                            creating_patterns.print_matrix(filled_image)
                            pattern_output_path = f'{output_directory_path}/image_{counter + 1}.png'
                            creating_patterns.matrix_to_image(filled_image, pattern_output_path)
                            print(f'Success: Pattern generated and saved to {pattern_output_path}.')

                            counter += 1

                            break

                        except Exception as e:
                            print(str(e))
                            retry_count += 1
                            if retry_count >= max_retries:
                                print(f"Maximum retries exceeded for pattern {counter_numbers + 1}. Skipping this pattern.")

                except Exception as e:
                    print('Error:', str(e))
                    break

        print(f'{int(counter / 2)} patterns have been generated.')
    else:
        for i in range(1, amount + 1):
            try:
                retry_count = 0
                max_retries = 500

                while retry_count < max_retries:
                    try:
                        creating_patterns = CreatingPatterns(rows, columns, complexity_level, scaling_factor, merge)
                        rand_comb = creating_patterns.find_valid_combinations(complexity_level, scaling_factor, False)

                        if not rand_comb:
                            print('Error', 'No valid combinations found.')
                            print(str(counter + 1) + ' images have been generated for now.')
                            return

                        # Create the pattern image
                        lit_image = creating_patterns.create_lit_image(columns, rows)
                        target_sum = round((len(lit_image) * len(lit_image[0])) / 3)
                        unlit_areas = creating_patterns.generate_unlit_regions(rand_comb[0], rand_comb[1], lit_image,
                                                                               target_sum)
                        filled_image = creating_patterns.fill_image(lit_image, unlit_areas)
                        creating_patterns.print_matrix(filled_image)
                        pattern_output_path = f'{output_directory_path}/image_{counter + 1}.png'
                        creating_patterns.matrix_to_image(filled_image, pattern_output_path)
                        print(f'Success: Pattern generated and saved to {pattern_output_path}.')

                        counter += 1

                        break

                    except Exception as e:
                        print(str(e))
                        retry_count += 1
                        if retry_count >= max_retries:
                            print(f"Maximum retries exceeded for pattern {counter + 1}. Skipping this pattern.")

            except Exception as e:
                print('Error:', str(e))
                break

            print(f'{counter} patterns have been generated.')

    write_report(output_directory_path, amount, complexity_level, scaling_factor)


class PatternApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Pattern Generator')
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        self.amount_input = QLineEdit(self)
        self.amount_input.setPlaceholderText('Amount (e.g. 10)')
        layout.addWidget(self.amount_input)

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
        self.output_path_input.setPlaceholderText('Output Directory Path')
        layout.addWidget(self.output_path_input)

        self.browse_button = QPushButton('Browse', self)
        self.browse_button.clicked.connect(self.browse_directory)
        layout.addWidget(self.browse_button)

        self.merge_checkbox = QCheckBox("Merge", self)
        self.merge_checkbox.setChecked(True)
        layout.addWidget(self.merge_checkbox)

        self.with_numbers_checkbox = QCheckBox("Include Number Images", self)
        self.with_numbers_checkbox.setChecked(False)  # Default to including numbers
        layout.addWidget(self.with_numbers_checkbox)

        self.generate_button = QPushButton('Generate Pattern', self)
        self.generate_button.clicked.connect(self.generate_pattern)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if directory:
            self.output_path_input.setText(directory)

    def generate_pattern(self):
        try:
            amount = int(self.amount_input.text())
            complexity_level = int(self.complexity_input.text())
            scaling_factor = float(self.scaling_factor_input.text())
            columns = int(self.columns_input.text())
            rows = int(self.rows_input.text())
            output_directory = self.output_path_input.text()
            merge = self.merge_checkbox.isChecked()
            with_numbers = self.with_numbers_checkbox.isChecked()

            create_patterns(
                amount=amount,
                complexity_level=complexity_level,
                scaling_factor=scaling_factor,
                rows=rows,
                columns=columns,
                merge=merge,
                output_directory_path=output_directory,
                with_numbers=with_numbers
            )

            QMessageBox.information(self, 'Success', f'Patterns generated and saved to {output_directory}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))


def main():
    app = QApplication(sys.argv)
    ex = PatternApp()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()