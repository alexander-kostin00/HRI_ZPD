"""
Author: Oleksandr Kostin
"""

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QFileDialog, QMessageBox
from PIL import Image
import random
import time
import math
import cv2
import sys


class CreatingMasks:
    def __init__(self, path_to_pattern, visible, pieces):
        image = cv2.imread(path_to_pattern)

        if image is None:
            print("Error: Could not open or find the image.")
            exit()

        self.color_matrix = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        self.visible_area = visible * (self.color_matrix.shape[0] * self.color_matrix.shape[1])
        self.pieces = pieces
        self.piece_area = int(self.visible_area / pieces)
        self.boundaries = []

    def create_visible_areas(self):
        side_length = int(math.sqrt(self.piece_area))
        time_limit = 2

        for i in range(self.pieces):
            start_time = time.time()
            available = False

            while not available:
                if time.time() - start_time > time_limit:
                    print("Timeout: Restarting the process.")
                    break

                r_col = random.randint(0, self.color_matrix.shape[1] - 1)
                r_row = random.randint(0, self.color_matrix.shape[0] - 1)

                print('RANDOM START COORDINATES: ' + str(r_row) + ' ' + str(r_col))

                available = self.check_region(r_row, r_col, side_length)

                if available:
                    self.boundaries.append([r_col, r_row, r_col + side_length - 1, r_row + side_length - 1])
                    print(self.boundaries)

    def xy(self, row, column):
        if column < 0 or row < 0 or column >= self.color_matrix.shape[1] or row >= self.color_matrix.shape[0]:
            return [-1, -1]
        for bound in self.boundaries:
            if (column >= bound[0] and column <= bound[2]) and (row >= bound[1] and row <= bound[3]):
                return [-1, -1]
        return [row, column]

    def check_region(self, start_row, start_column, side_length):
        for i in range(0, side_length):
            for j in range(0, side_length):
                point = self.xy(start_row + i, start_column + j)
                if point[0] == -1:
                    return False
        return True

    def cover_image(self):
        green_color = [0, 255, 0]  # RGB value for green
        for i in range(self.color_matrix.shape[0]):
            for j in range(self.color_matrix.shape[1]):
                for bound in self.boundaries:
                    if (j >= bound[0] and j <= bound[2]) and (i >= bound[1] and i <= bound[3]):
                        break
                else:
                    self.color_matrix[i, j] = random.choice([(255,255,255), (0,0,0)])

    def matrix_to_image(self, matrix, filename):
        image = Image.fromarray(matrix.astype('uint8'), 'RGB')
        image.save(filename)


class MaskApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Mask Generator')
        self.setGeometry(100, 100, 400, 350)

        layout = QVBoxLayout()

        self.visible_input = QLineEdit(self)
        self.visible_input.setPlaceholderText('Visible Area Percentage (e.g.  0.45)')
        layout.addWidget(self.visible_input)

        self.pieces_input = QLineEdit(self)
        self.pieces_input.setPlaceholderText('Number of Pieces (e.g.  5)')
        layout.addWidget(self.pieces_input)

        self.input_path_input = QLineEdit(self)
        self.input_path_input.setPlaceholderText('Input Path')
        layout.addWidget(self.input_path_input)

        self.browse_input_button = QPushButton('Browse Input', self)
        self.browse_input_button.clicked.connect(self.browse_input_file)
        layout.addWidget(self.browse_input_button)

        self.output_path_input = QLineEdit(self)
        self.output_path_input.setPlaceholderText('Output Path')
        layout.addWidget(self.output_path_input)

        self.browse_output_button = QPushButton('Browse Output', self)
        self.browse_output_button.clicked.connect(self.browse_output_file)
        layout.addWidget(self.browse_output_button)

        self.generate_button = QPushButton('Generate Mask', self)
        self.generate_button.clicked.connect(self.generate_mask)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)

    def browse_input_file(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'PNG Files (*.png);;All Files (*)')
        if file:
            self.input_path_input.setText(file)

    def browse_output_file(self):
        file, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'PNG Files (*.png);;All Files (*)')
        if file:
            self.output_path_input.setText(file)

    def generate_mask(self):
        try:
            visible = float(self.visible_input.text())
            pieces = int(self.pieces_input.text())
            input_path = self.input_path_input.text()
            output_path = self.output_path_input.text()
            retry_count = 0
            max_retries = 500

            while retry_count < max_retries:
                try:
                    creating_masks = CreatingMasks(input_path, visible, pieces)
                    creating_masks.create_visible_areas()
                    creating_masks.cover_image()
                    creating_masks.matrix_to_image(creating_masks.color_matrix, output_path)

                    QMessageBox.information(self, 'Success', f'Mask generated and saved to {output_path}')
                    break

                except Exception as e:
                    print(str(e))
                    retry_count += 1
                    if retry_count >= max_retries:
                        QMessageBox.critical(self, 'Error', 'Maximum retries exceeded. Could not generate mask.')

        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))


def main():
    app = QApplication(sys.argv)
    ex = MaskApp()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()