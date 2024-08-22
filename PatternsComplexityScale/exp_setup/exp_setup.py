"""
Author: Oleksandr Kostin
"""

from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton, QVBoxLayout
from PyQt6.QtGui import QPixmap, QScreen, QFont
from PyQt6.QtCore import QTimer, Qt
import sys
import os

# Add the project root directory to the sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(project_root)

from PatternsComplexityScale.creating_masks.creating_masks import CreatingMasks
from constants import constants
import threading
import random
import sys
import os
import re

def apply_mask(visible, pieces, output_directory_path):
    try:


        input_directory_path = 'patterns_uncovered'

        files = [
            f for f in os.listdir(input_directory_path)
            if os.path.isfile(os.path.join(input_directory_path, f)) and
               any(char.isdigit() for char in f) and
               int(''.join(filter(str.isdigit, f))) % 2 == 0
        ]

        print(files)

        if not files:
            raise FileNotFoundError("No files found in the directory.")

        files_output = [f for f in os.listdir(output_directory_path) if
                        os.path.isfile(os.path.join(output_directory_path, f))]

        print(files_output)

        chosen_file = random.choice(files)
        pattern_path = os.path.join(input_directory_path, chosen_file)

        creating_masks = CreatingMasks(pattern_path, visible, pieces)
        creating_masks.create_visible_areas()
        creating_masks.cover_image()

        file_root, extention = os.path.splitext(chosen_file)
        output_path = output_directory_path + '/' + str(len(files_output) + 1) + '_' + file_root + '_covered_' + str(
            visible) + extention
        creating_masks.matrix_to_image(creating_masks.color_matrix, output_path)

        print(f'Mask generated and saved to {output_path}')
    except Exception as e:
        print('Error:', str(e))


class ImageSlideshow(QWidget):
    def __init__(self, image_dir, masked_image_dir):
        super().__init__()

        self.image_dir = image_dir
        self.masked_image_dir = masked_image_dir
        self.image_files = self.get_image_files()
        self.current_index = 0
        self.cleanup_done = False

        self.initUI()
        self.start_slideshow()

    def initUI(self):
        self.setWindowTitle('PATTERNS PRE-SHOW')

        # Get the screen size
        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        self.screen_width = screen.width()
        self.screen_height = screen.height() - 100

        self.main_layout = QVBoxLayout()

        self.feedback_label = QLabel(self)
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.feedback_label.setFont(QFont('Arial', 48))
        self.feedback_label.setStyleSheet("color: red;")
        self.feedback_label.hide()

        self.image_layout = QHBoxLayout()
        self.image_layout.addItem(QSpacerItem(300, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))

        # Add spacer to push the image to the right side
        self.image_layout.addItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.label = QLabel(self)
        self.image_layout.addWidget(self.label)

        # Add spacer to push the image slightly towards the middle
        self.image_layout.addItem(QSpacerItem(450, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))

        self.main_layout.addLayout(self.image_layout)
        self.setLayout(self.main_layout)

    def get_image_files(self):
        # Get a list of image files in the specified directory
        image_files = [f for f in os.listdir(self.image_dir) if
                       f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not image_files:
            raise FileNotFoundError("No image files found in the specified directory.")

        # Sort the list of files
        image_files.sort(key=lambda f: int(''.join(filter(str.isdigit, f)) or -1))

        return image_files

    def start_slideshow(self):
        self.show_image()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_next_image)
        self.update_timer()

    def show_image(self):
        # Display the current image
        image_path = os.path.join(self.image_dir, self.image_files[self.current_index])
        pixmap = QPixmap(image_path)

        # Scale the pixmap to fit the screen size while maintaining the aspect ratio
        scaled_pixmap = pixmap.scaled(self.screen_width, self.screen_height, Qt.AspectRatioMode.KeepAspectRatio)

        self.label.setPixmap(scaled_pixmap)

        # Resize the window to match the screen size
        self.resize(self.screen_width, self.screen_height)

    def show_next_image(self):
        # Increment the index after showing the image
        self.current_index += 1
        if self.current_index >= len(self.image_files):
            self.show_masked_image()
        else:
            self.show_image()
            self.update_timer()

    def update_timer(self):
        # Determine the display duration based on the file number
        file_name = self.image_files[self.current_index]
        number = int(''.join(filter(str.isdigit, file_name)) or 0)
        duration = constants['number_image_display_duration'] if number % 2 == 1 else constants['pattern_image_display_duration']
        self.timer.start(duration)

    def show_masked_image(self):
        if not self.cleanup_done:
            self.cleanup_masked_image_dir()
            self.cleanup_done = True

        masked_image_path = self.get_last_masked_image()
        pixmap = QPixmap(masked_image_path)

        # Scale the pixmap to fit the screen size while maintaining the aspect ratio
        scaled_pixmap = pixmap.scaled(self.screen_width, self.screen_height - 100, Qt.AspectRatioMode.KeepAspectRatio)

        # Update the label's pixmap
        self.label.setPixmap(scaled_pixmap)
        self.label.repaint()  # Force the label to repaint

        # Clear existing layout items except the label
        self.clear_layout(self.image_layout)

        self.setWindowTitle('MASKED PATTERN')

        self.image_layout.addItem(QSpacerItem(1, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        self.image_layout.addItem(QSpacerItem(100, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))
        self.image_layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.image_layout.addItem(QSpacerItem(1, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        button_count = len(self.image_files) // 2

        button_layout = QHBoxLayout()
        button_layout.addItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        for i in range(button_count):
            button = QPushButton(str(i + 1), self)
            button.setFixedSize(50, 50)
            button.setStyleSheet("color: black;") #anna: changed color to black
            button.setFont(QFont('Arial', 16))
            button.clicked.connect(self.check_button)
            button_layout.addWidget(button)

        button_layout.addItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.image_layout.addLayout(button_layout)

        # Stop the timer since we are done with the slideshow
        self.timer.stop()

    def cleanup_masked_image_dir(self):
        if os.path.exists(self.masked_image_dir):
            for f in os.listdir(self.masked_image_dir):
                file_path = os.path.join(self.masked_image_dir, f)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f'Error: {e}')

        apply_mask(constants['mask_visibility_initial'], random.randint(constants['mask_pieces_min'], constants['mask_pieces_max']), self.masked_image_dir)

    def handle_button(self, result):
        masked_image_path = self.get_last_masked_image()
        # Extract the visibility value from the last masked image filename
        last_masked_image_filename = os.path.basename(masked_image_path)
        visibility_value = float(last_masked_image_filename.split('_')[-1].replace('.png', ''))

        if result:
            new_visibility_value = round(visibility_value - constants['decreasing_step'], 2) # anna: made increase and decrease consistent
            print('New visibility value is ' + str(new_visibility_value))
        else:
            new_visibility_value = round(visibility_value + constants['increasing_step'], 2)
            print('New visibility value is ' + str(new_visibility_value))

        # Check the visibility limits
        if new_visibility_value <= constants['visibility_minimum']:
            self.display_message("YOU WON")
        #elif new_visibility_value >= constants['visibility_maximum']:

        else:
            # Apply the mask with new visibility value
            thread = threading.Thread(target=self.apply_mask_and_show, args=(new_visibility_value,))
            thread.start()

    def apply_mask_and_show(self, new_visibility_value):
        apply_mask(new_visibility_value, random.randint(constants['mask_pieces_min'], constants['mask_pieces_max']), self.masked_image_dir)
        QTimer.singleShot(0, self.show_masked_image)  # Ensure UI update on main thread

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None and widget != self.label:
                widget.deleteLater()
            elif widget is None and item.layout() is not None:
                self.clear_layout(item.layout())

    def clear_layout_last(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            elif widget is None and item.layout() is not None:
                self.clear_layout(item.layout())

    def get_last_masked_image(self):
        masked_image_files = [f for f in os.listdir(self.masked_image_dir) if
                              f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not masked_image_files:
            raise FileNotFoundError("No masked image files found in the specified directory.")

        # Extract the integer prefix and sort the files based on this prefix
        masked_image_files.sort(key=lambda f: int(re.match(r'(\d+)_', f).group(1)), reverse=True)

        masked_image_path = os.path.join(self.masked_image_dir, masked_image_files[0])

        print(f"Latest masked image: {masked_image_path}")

        return masked_image_path

    def check_button(self):
        sender = self.sender()
        if sender:
            button_number = int(sender.text())
            print(f"Button {button_number} pressed")

            masked_image_path = self.get_last_masked_image()

            # Extract the second integer from the last masked image filename
            last_masked_image_filename = os.path.basename(masked_image_path)
            numbers_in_filename = [int(s) for s in last_masked_image_filename.split('_') if s.isdigit()]
            print(last_masked_image_filename, numbers_in_filename)
            if len(numbers_in_filename) >= 2:
                correct_value = numbers_in_filename[1] // 2
                if button_number == correct_value:
                    print("CORRECT")
                    self.display_feedback(True)
                    QTimer.singleShot(constants['feedback_message_duration'], lambda: self.handle_button(True))
                else:
                    print("WRONG")
                    self.display_feedback(False, correct_value)
                    QTimer.singleShot(constants['feedback_message_duration'], lambda: self.handle_button(False))
            else:
                print("Error: Unable to parse the filename for the second integer")

    def display_feedback(self, is_correct, correct_value=None):
        if is_correct:
            message = "CORRECT"
            self.feedback_label.setStyleSheet("color: green;")
        else:
            message = f"WRONG.<br>IT WAS {correct_value}"
            self.feedback_label.setStyleSheet("color: red;")

        self.feedback_label.setText(f"<p align='center'>{message}</p>")
        self.feedback_label.adjustSize()  # Adjust the size to fit the content

        # Calculate the position for the feedback label
        x = self.screen_width // 2 + (self.screen_width // 4) - (self.feedback_label.width() // 2) -25
        y = self.screen_height // 8

        self.feedback_label.setGeometry(x, y, self.feedback_label.width(),
                                        self.feedback_label.height())  # Set the size and position
        self.feedback_label.show()

        QTimer.singleShot(constants['feedback_message_duration'], self.hide_feedback)  # Hide feedback label after 3 seconds

    def hide_feedback(self):
        self.feedback_label.hide()

    def display_message(self, message):
        # Clear existing layout items
        self.clear_layout_last(self.image_layout)

        # Create a label to display the message
        message_label = QLabel(message, self)
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message_label.setFont(QFont('Arial', 48))
        message_label.setStyleSheet("color: white;")

        # Add the label to the layout
        self.image_layout.addWidget(message_label)

        # Resize the window to fit the screen size
        self.resize(self.screen_width, self.screen_height)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    image_dir = 'patterns_uncovered'
    masked_image_dir = 'masked'
    window = ImageSlideshow(image_dir, masked_image_dir)
    window.show()

    sys.exit(app.exec())
