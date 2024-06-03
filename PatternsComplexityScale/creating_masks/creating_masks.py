from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QLineEdit, QPushButton, QFileDialog, QMessageBox
from PIL import Image
import numpy as np
import random
import math
import cv2
import sys



class CreatingMasks:
    def __init__(self, path_to_pattern, visible, pieces):
        image = cv2.imread(path_to_pattern, cv2.IMREAD_GRAYSCALE)

        if image is None:
            print("Error: Could not open or find the image.")
            exit()

        _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

        self.binary_matrix = np.where(binary_image == 255, 0, 1)

        self.visible_area = visible*(len(self.binary_matrix)*len(self.binary_matrix[0]))
        self.pieces = pieces
        self.piece_area = int(self.visible_area/pieces)

        self.visible_coord = []
        print('Visible coordinates: ' + str(self.visible_coord))

        self.boundaries = []

    def create_visible_areas(self):
        side_length = int(math.sqrt(self.piece_area))
        for i in range(self.pieces):
            available = False
            while not available:
                r_col = random.randint(0, len(self.binary_matrix[0]))
                r_row = random.randint(0, len(self.binary_matrix))

                print('RANDOM START COORDINATES: ' + str(r_row) + ' ' + str(r_col))

                available = self.check_region(r_row, r_col)

                if available:
                    self.boundaries.append([r_col, r_row, r_col + side_length-2, r_row + side_length-2])
        print(self.boundaries)

    def xy(self, row, column):
        if column < 0 or row < 0 or column >= len(self.binary_matrix[0]) or row >= len(self.binary_matrix) or ([row, column] in self.visible_coord):
            return [-1, -1]
        for bound in self.boundaries:
            if (column >= bound[0] and column <= bound[2]) and (row >= bound[1] and row <= bound[3]):
                return [-1, -1]
        return [row, column]

    def check_region(self, start_row, start_column):
        side_length = int(math.sqrt(self.piece_area))

        for i in range(0, side_length):
            for j in range(0, side_length):
                point = self.xy(start_row + i, start_column + j)
                #print(start_row + i, start_column + j)
                if point[0] == -1:
                    return False
        return True

    def cover_image(self):
        for i in range(len(self.binary_matrix)):
            for j in range(len(self.binary_matrix[0])):
                for bound in self.boundaries:
                    if (j >= bound[0] and j <= bound[2]) and (i >= bound[1] and i <= bound[3]):
                        break
                else:
                    self.binary_matrix[i, j] = 1


def matrix_to_image(matrix, filename):
    image = Image.new('1', (len(matrix[0]), len(matrix)))

    pixels = image.load()

    for i in range(image.size[1]):
        for j in range(image.size[0]):
            pixels[j, i] = 0 if matrix[i][j] == 1 else 1

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

            creating_masks = CreatingMasks(input_path, visible, pieces)
            creating_masks.create_visible_areas()
            creating_masks.cover_image()
            matrix_to_image(creating_masks.binary_matrix, output_path)

            QMessageBox.information(self, 'Success', f'Mask generated and saved to {output_path}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))




def main():
    app = QApplication(sys.argv)
    ex = MaskApp()
    ex.show()
    sys.exit(app.exec())
    #path = 'patterns/image1.png'     # Path to image
    #visible = 0.01       # Percentage value of the part of the image that will remain visible after applying masking
    #pieces = 100   # Amount of rectangles into which the visible part of the picture is divided

    #creating_masks = CreatingMasks(path, visible, pieces)
    #binary_matrix = creating_masks.binary_matrix

    #print(binary_matrix)
    #print()
    #print('Hight: ' + str(len(binary_matrix)))
    #print('Wigth: ' + str(len(binary_matrix[0])))
    #print()

    #creating_masks.create_visible_areas()
    #creating_masks.cover_image()

    #matrix_to_image(creating_masks.binary_matrix, 'patterns_covered/image6.png')



if __name__ == '__main__':
    main()