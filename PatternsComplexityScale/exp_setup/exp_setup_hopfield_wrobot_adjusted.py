"""
Author: Oleksandr Kostin/Anna Lange
"""

from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton, QVBoxLayout
from PyQt6.QtGui import QPixmap, QScreen, QFont
from PyQt6.QtCore import QTimer, Qt
import sys
import os
import shutil


# Add the project root directory to the sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(project_root)

#from PatternsComplexityScale.creating_masks.creating_masks import CreatingMasks
from constants import constants
import threading
import random
import re
import qi
import numpy as np
from PIL import Image
import glob
import cv2
import matplotlib.pyplot as plt
from collections import deque
import time
import json


def collect_mask(level, output_directory_path):

    '''
    Parameters:
        level: relates to a range of flipped bits as calculated by the Hopfield Network
    '''

    print('entered collect mask')

    try:


        input_directory_path = 'masks_hopfield'

        level_str = str(level)

        # choose a random image number

        patter_no = random.randint(0, 4)
        patter_no_str = str(patter_no)


        pattern_path = os.path.join(input_directory_path, patter_no_str)
        subfolder_path = os.path.join(pattern_path, level_str)

        print(subfolder_path)

        files = [
            f for f in os.listdir(subfolder_path)
            if os.path.isfile(os.path.join(subfolder_path, f))
        ]

        print(files)

        if not files:
            raise FileNotFoundError("No files found in the directory.")

        files_output = [f for f in os.listdir(output_directory_path) if
                        os.path.isfile(os.path.join(output_directory_path, f))]

        print(files_output)

        chosen_file = random.choice(files)
        pattern_path = os.path.join(subfolder_path, chosen_file)

        file_root, extention = os.path.splitext(chosen_file)
        output_path = output_directory_path + '/' + str(len(files_output) + 1) + '_' + file_root + '_covered_' + str(
            level) + extention

        shutil.copy(pattern_path, output_path)

        print(f'Mask generated and saved to {output_path}')

    except Exception as e:
        print('Error:', str(e))


class ImageSlideshow(QWidget):
    def __init__(self, image_dir, masked_image_dir, train_dir, mask_capture_dir):
        super().__init__()

        self.image_dir = image_dir
        self.masked_image_dir = masked_image_dir
        self.train_dir = train_dir
        self.mask_capture_dir = mask_capture_dir
        self.image_files = self.get_image_files()
        self.current_index = 0
        self.cleanup_done = False
        self.button_press_number = 0
        self.closing = False
        self.pattern_underlying = None
        self.flipped_bits_save = None
        self.pattern_identified = None
        self.accuracy_pattern = None
        self.human_choice = None

        # Initialize the save data later we might want to add more
        self.summary_data = {
            "iterations": []
        }
        self.current_iteration_data = {
            "iteration_number": None,
            "mask_shown": None,
            "pattern_underlying": None,
            "level": None,
            "visibility": None,
            "flipped_bits": None,
            "accuracy": None,
            "pattern_identified": None,
            "human_button": None
        }
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
        print(image_path)

        # Scale the pixmap to fit the screen size while maintaining the aspect ratio
        scaled_pixmap = pixmap.scaled(self.screen_width, self.screen_height - 100, Qt.AspectRatioMode.KeepAspectRatio)

        self.label.setPixmap(scaled_pixmap)

        self.clear_layout(self.image_layout)

        # Resize the window to match the screen size
        self.resize(self.screen_width, self.screen_height)
        print(self.current_index)

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
            button.setStyleSheet("color: black;")  # anna: changed color to black
            button.setFont(QFont('Arial', 16))
            button.clicked.connect(self.check_button)
            button.setVisible(False)
            button_layout.addWidget(button)

        button_layout.addItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.image_layout.addLayout(button_layout)

        # Capture the patterns with the robot helper camera to train its Hopfield
        if self.current_index % 2 == 1: #only save the odd images as those are the patterns

            pattern_no = str(self.current_index - 1)
            filename_pattern = f'{pattern_no}.png'
            QTimer.singleShot(150, lambda: self.capture_and_save_image(filename_pattern, 'train')) #150 ms delay

    def show_next_image(self):
        if self.closing:
            return
        # Increment the index after showing the image
        self.current_index += 1
        if len(self.image_files) + 1 > self.current_index >= len(self.image_files) and not self.closing:
            self.show_masked_image() # only call once after the patterns have been called, the show_masked_image is self contained after this
        elif self.current_index < len(self.image_files) and not self.closing:
            self.show_image()
            self.update_timer()

    def update_timer(self):
        # Determine the display duration based on the file number
        file_name = self.image_files[self.current_index]
        number = int(''.join(filter(str.isdigit, file_name)) or 0)
        duration = constants['number_image_display_duration'] if number % 2 == 1 else constants['pattern_image_display_duration']
        self.timer.start(duration)

    def show_masked_image(self):
        if self.closing:
            return
        if not self.cleanup_done:
            self.cleanup_masked_image_dir()
            self.cleanup_done = True

        masked_image_path = self.get_last_masked_image() #getting the path, change to get the respective mask from a path

        pixmap = QPixmap(masked_image_path)

        # Scale the pixmap to fit the screen size while maintaining the aspect ratio
        scaled_pixmap = pixmap.scaled(self.screen_width, self.screen_height - 100, Qt.AspectRatioMode.KeepAspectRatio)

        # Update the label's pixmap
        self.label.setPixmap(scaled_pixmap)
        self.label.repaint()  # Force the label to repaint

        # Call the function to capture the image with the robot camera

        mask_files = len([f for f in os.listdir(self.masked_image_dir) if
                       f.lower().endswith(('.png', '.jpg', '.jpeg'))])

        filename_mask = f'mask_{mask_files}.png'

        QTimer.singleShot(100, lambda: self.capture_and_save_image(filename_mask, 'mask')) # Delay of 100 milliseconds

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

        # Additional processing after UI update
        # Optionally, delay further processing to ensure capture is complete
        QTimer.singleShot(250, self.after_capture_processing)

    def after_capture_processing(self):
        # Calculate cognitive load for the robot
        flipped_bits, flattened_image = self.calculate_flipped_bits()

        # Check most similar pattern
        pattern_choice = self.check_similarity(flattened_image)

        self.flipped_bits_save = int(flipped_bits)
        self.pattern_identified = int(pattern_choice)


    def cleanup_masked_image_dir(self):
        if os.path.exists(self.masked_image_dir):
            for f in os.listdir(self.masked_image_dir):
                file_path = os.path.join(self.masked_image_dir, f)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f'Error: {e}')
        if os.path.exists(self.mask_capture_dir):
            for f in os.listdir(self.mask_capture_dir):
                file_path = os.path.join(self.mask_capture_dir, f)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f'Error: {e}')

        collect_mask(constants['mask_level_initial'], self.masked_image_dir)
        print('Collected the initial mask')

    def handle_button(self, result):

        self.summary_data["iterations"].append(self.current_iteration_data)

        self.current_iteration_data = {
            "iteration_number": None,
            "mask_shown": None,
            "pattern_underlying": None,
            "level": None,
            "visibility": None,
            "flipped_bits": None,
            "pattern_identified": None
        }

        self.current_iteration_data["pattern_underlying"] = self.pattern_underlying
        self.current_iteration_data["flipped_bits"] = self.flipped_bits_save
        self.current_iteration_data["pattern_identified"] = self.pattern_identified
        self.current_iteration_data["accuracy"] = self.accuracy_pattern
        self.current_iteration_data["human_button"] = self.human_choice

        #start the next iteration
        self.button_press_number += 1

        self.current_iteration_data["iteration_number"] = self.button_press_number

        masked_image_path = self.get_last_masked_image()
        # Extract the level value from the last masked image filename
        last_masked_image_dir = os.path.dirname(masked_image_path)
        print(last_masked_image_dir)
        last_masked_image_filename = os.path.basename(masked_image_path)
        self.current_iteration_data["mask_shown"] = last_masked_image_filename
        level_value = int(last_masked_image_filename.split('_')[-1].replace('.png', ''))
        self.current_iteration_data["level"] = level_value


            #(float(last_masked_image_filename.split('_')[-1].replace('.png', '')))

        if not result and level_value > 1:
            new_level_value = level_value - 1  # anna: made increase and decrease consistent
            print('New level value is ' + str(new_level_value))
        elif result and level_value < 17:
            new_level_value = level_value + 1
            print('New level value is ' + str(new_level_value))
        else:
            new_level_value = level_value

        # Check the visibility

        last_masked_image_filename = os.path.basename(masked_image_path)


        match = re.search(r'\d+\.\d+', last_masked_image_filename)
        if match:
            visibility_value = float(match.group())
            print(f"The extracted floating-point value is: {visibility_value}")
            self.current_iteration_data["visibility"] = visibility_value

            if visibility_value <= constants['visibility_minimum'] and result:
                self.display_message("YOU WON")
                self.summary_data["iterations"].append(self.current_iteration_data)
                QTimer.singleShot(2000, self.display_completed_message)


            #elif visibility_value >= constants['visibility_maximum']:
                #self.display_message("YOU LOST")
            else:
                #
                print('Apply the mask with new visibility value')
                thread = threading.Thread(target=self.collect_mask_and_show, args=(new_level_value,))
                thread.start()
        else:
            print("No floating-point number found in the file name.")

    def display_completed_message(self):
        # Display the second message
        self.display_message("THE EXPERIMENT IS COMPLETED")

        # Wait for another 2 seconds, then close the window
        QTimer.singleShot(2000, self.save_data_and_close)

    def save_data_and_close(self):
        self.closing = True
        # Save data to a JSON file
        # converting int64 to int
        self.summary_data = {k: int(v) if isinstance(v, np.int64) else v for k, v in self.summary_data.items()}

        with open("slideshow_summary.json", "w") as f:
            json.dump(self.summary_data, f, indent=4)

        # Now close the window
        self.close()
        QApplication.quit()

    def collect_mask_and_show(self, new_level_value):
        collect_mask(new_level_value, self.masked_image_dir)
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
        print(self.masked_image_dir)
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
            self.human_choice = button_number
            masked_image_path = self.get_last_masked_image()

            # Extract the second integer from the last masked image filename
            last_masked_image_filename = os.path.basename(masked_image_path)
            numbers_in_filename = [int(s) for s in last_masked_image_filename.split('_') if s.isdigit()]
            print(last_masked_image_filename, numbers_in_filename)
            if len(numbers_in_filename) >= 2:
                correct_value = numbers_in_filename[2] + 1
                self.pattern_underlying = correct_value
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
        message_label.setStyleSheet("color: black;") #anna:changed color to black

        # Add the label to the layout
        self.image_layout.addWidget(message_label)

        # Resize the window to fit the screen size
        self.resize(self.screen_width, self.screen_height)

    def capture_and_save_image(self, filename, train_or_mask):
        # Capture the image with the robot camera
        result, image = self.capture_robot_camera()


        # Convert the image to a PIL Image
        img = Image.fromarray(image)


        if train_or_mask == 'train':
            # crop the image
            img_res = img.crop((constants['left_t'], constants['top_t'], constants['right_t'], constants['bottom_t']))

            # Save the image with to the trainimgs location
            filename_train = os.path.join(self.train_dir, filename)
            print('trying to save to', filename_train)
            img_res.save(filename_train)
            print('training image saved to', filename_train)
        else:
            # crop the image
            img_res = img.crop((constants['left_m'], constants['top_m'], constants['right_m'], constants['bottom_m']))
            # Save the image with to the maskimgs location

            filename_mask = os.path.join(self.mask_capture_dir, filename)
            img_res.save(filename_mask)

        #img_res.save(filename)

    def capture_robot_camera(self):
        """ Capture images from Robot's TOP camera. Note that the Nao's
            camera resolution is lower than the Pepper robot.
            Remember you need to subscribe and unsubscribe respectively
            see, https://ai-coordinator.jp/pepper-ssd#i-3
        """
        SubID = "Pepper"  # change to NAO if needed
        session = qi.Session()
        session.connect("tcp://" + constants['ip'] + ":" + str(constants['port'] ))

        videoDevice_robot = session.service('ALVideoDevice')
        # subscribe top camera, Image of 320*240px
        AL_kTopCamera, AL_kQVGA, Frame_Rates = 0, 1, 5  # 2.5  #10
        AL_kBGRColorSpace = 13  # Buffer contains triplet on the format 0xRRGGBB, equivalent to three unsigned char
        captureDevice_nao = videoDevice_robot.subscribeCamera(SubID, AL_kTopCamera, AL_kQVGA, AL_kBGRColorSpace,
                                                              Frame_Rates)

        width, height = 320, 240
        image = np.zeros((height, width, 3), np.uint8)
        result = videoDevice_robot.getImageRemote(captureDevice_nao)

        if result == None:
            print("Camera problem.")
        elif result[6] == None:
            print("No image. ")
        else:
            # translate value to mat
            values = result[6]
            i = 0
            for y in range(0, height):
                for x in range(0, width):
                    image[y, x, 0] = values[i + 0]
                    image[y, x, 1] = values[i + 1]
                    image[y, x, 2] = values[i + 2]
                    i += 3

        # unsubscribe from the camera
        videoDevice_robot.unsubscribe(captureDevice_nao)
        return result[6], image

    def calculate_flipped_bits(self):
        '''Calculates the bits that were flipped in the Hopfield network as a way to measure
         how easy it is to retrieve one of the trained patterns. This is based on the robots screenshots.'''

        # run the image trough the hopfield to generate an energy
        #filename_train = #set the filepath where the training images are saved
        train_imgs = self.bipolarize_pattern_robot_train(self.train_dir, 5) #5 training imgs
        weights_h = self.calc_weights(train_imgs)
        print('the masking directory', self.mask_capture_dir)
        masked_captured_files = [f for f in os.listdir(self.mask_capture_dir) if
                              f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not masked_captured_files:
            raise FileNotFoundError("No masked image files found in the specified directory.")

        print('the masked filename', masked_captured_files)

        # Extract the integer prefix and sort the files based on this prefix
        masked_captured_files.sort(key=lambda f: int(re.match(r'mask_(\d+)', f).group(1)), reverse=True)

        masked_capture_path = os.path.join(self.mask_capture_dir, masked_captured_files[0])

        #print(masked_capture_path)

        current_pattern = self.bipolarize_pattern_robot(masked_capture_path)

        new_s1, changed_bits1, epochs1 = self.calc_stateupdate_async(current_pattern, weights_h, 1000)
        # Extract the flattened image from the 'images' array
        flattened_image = new_s1
        energy_state = changed_bits1 #use this value to determine next level
        return energy_state, flattened_image

    def bipolarize_pattern_robot_train(self, path, no_imgs):

        """ Convert list of pattern images for training into Bipolarized (-1, 1) inputs.
        Parameters
        -----------
        path: filename
        location where the image is located
        no_imgs: integer
        amount of training images


        Return
        -------
        images in format for Hopfield Network"""

        print('This is generating the training images.')
        images = np.zeros((constants['rsize'][0] * constants['rsize'][1], no_imgs))
        k = 0
        for j in range(no_imgs):
            # image directory with image names as ordered ints
            g = j +  k
            filename_train = '{}.png'.format(g)
            k += 1
            filepath_train = os.path.join(path, filename_train)
            print('The training image path is', filepath_train)
            image = cv2.imread(filepath_train, cv2.IMREAD_GRAYSCALE)
            print(image.shape)
            rimg = cv2.resize(image, constants['rsize'], interpolation=cv2.INTER_AREA)
            bimg = cv2.threshold(rimg, 125, 255, cv2.THRESH_BINARY)[1]
            # convert 255 to -1 and 0 to 1
            bimg = bimg.astype('int64')
            nonz_inds = bimg.nonzero()
            bimg[nonz_inds], bimg[bimg == 0] = -1, 1  # convert 255 to -1 and 0 to 1
            savename = path + 'check%s.png' % j

            plt.imsave(savename, bimg, cmap='Greys')
            images[:, j] = bimg.flatten()

        return images
    def check_similarity(self, converged_image):
        '''This function checks how similar a converged image (from a masked image shown) is to each of the training
        and returns the training image that is most similar. In this way it allows the robot to choose the image it
        recognizes.
        '''

        accuracies = np.zeros(5)

        # pattern paths

        pattern_path = os.path.join(self.train_dir, f'*.png')
        # Use glob to get all file paths matching the pattern
        filepaths = glob.glob(pattern_path)

        for pattern_path in filepaths:
            compare_pattern = self.bipolarize_pattern_robot(pattern_path)
            print('the similaritz path is', pattern_path)
            number = pattern_path.split('/')[1].split('.')[0]
            n = int(int(number)/2)
            print('the number used is', n)
            accuracies[n] = np.mean(compare_pattern == converged_image)
            print(f"Accuracy for pattern{n}: {accuracies[n]}")

        max_pattern = np.argmax(accuracies) + 1
        accuracy_chosen = np.max(accuracies)
        print("the accuracy is ", accuracy_chosen)
        self.accuracy_pattern = float(accuracy_chosen)
        return max_pattern

    def bipolarize_pattern_robot(self, pattern_name):

        """ Convert percieved patterns images into Bipolarized (-1, 1) inputs.
        Parameters
        -----------
        pattern_name: filename
        location where the image is located
        Return
        -------
        images in format for Hopfield Network"""

        gimg = cv2.imread(pattern_name, cv2.IMREAD_GRAYSCALE)

        rimg = cv2.resize(gimg, constants['rsize'])
        bimg = cv2.threshold(rimg, 125, 255, cv2.THRESH_BINARY)[1]

        cv2.waitKey(0)

        cv2.destroyAllWindows()

        # convert 255 to -1 and 0 to 1
        bimg = bimg.astype('int64')
        print("bipolorized 2")
        nonz_inds = bimg.nonzero()
        print("bipolorized 3")
        bimg[nonz_inds], bimg[bimg == 0] = -1, 1  # convert 255 to -1 and 0 to 1
        print("bipolorized 4")

        return bimg.flatten()

    def calc_stateupdate_async(self, all_states, weights, max_epoch_count, check_interval=100, start_check_epoch=1000):
        """Calculates the state updates asynchronously.
        Parameters
        ----------
        all_states: State matrix of the network (e.g. set of binary images)
        weights: weight matrix (calculated by function calc_weights)
        max_epoch_count: counter for epochs
        """
        changed_bits = 0
        epoch_count = 0
        state_update_count = 0
        new_s = np.copy(all_states)
        # Buffer to keep track of the last few states
        state_buffer = deque(maxlen=check_interval)

        while epoch_count < max_epoch_count:
            rand_ind = np.random.randint(len(all_states))  # pick a random pixel
            epoch_count += 1
            # print('the epoch count is:',epoch_count)
            wi = weights[rand_ind, :]
            new_value = self.get_sign(self.calc_dotproduct_async(all_states, wi))

            if new_s[rand_ind] != new_value:
                new_s[rand_ind] = new_value  # update one pixel in the image according to the state update rule
                changed_bits += 1  # increase changed bits if the pixel was changed from the original input
                # print('the state update count is', state_update_count)
            state_buffer.append(np.copy(new_s))  # Add current state to buffer

            if epoch_count >= start_check_epoch and (
                    epoch_count - start_check_epoch) % check_interval == 0:  # check for convergence periodically
                # print('CONVERGENCE TEST', 'in epoch', epoch_count)
                if np.array_equal(new_s, state_buffer[0]):
                    print('Converged after {} epochs'.format(epoch_count))
                    print('state changes', changed_bits)
                    break

        return new_s, changed_bits, epoch_count

    def calc_dotproduct(self, all_states, weights):
        """Calculates dot product between two matrices, here the states and the weights of our network.
        Parameters
        ----------
        all_states: State matrix of the network (e.g. set of binary images)
        weights: weight matrix (calculated by function calc_weights)
        """
        z = np.dot(all_states.T, weights)
        return z.T

    def calc_dotproduct_async(self, states, weights_c):
        """Calculates summed product between a weight vector (one column of the weight matrix), and one set of states.
        Parameters
        ----------
        states: State matrix of the network (e.g. set of binary images)
        weights_c: weight matrix (calculated by function calc_weights)
        """
        z_async = 0
        for j in np.arange(0, len(weights_c)):
            z_async = z_async + weights_c[j] * states[j]
        return z_async

    def get_sign(self, sum_sw):
        """Returns -1 if the input is smaller than zero and 1 if the input is larger than zero.
        Parameters
        ----------
        sum_sw: Integer/Float
        """
        theta = np.sign(sum_sw)
        return theta

    def calc_weights(self, all_states):
        """Calculates the weights for the Hopfield Network using the states to train the network on.
        All set of states to train the network on, are passed in at once.
        Parameters
        ----------
        all_states: State matrix of the network (e.g. set of binary images)
        """
        w = np.dot(all_states, all_states.T)
        np.fill_diagonal(w, 0)
        return w


if __name__ == '__main__':
    app = QApplication(sys.argv)

    #Robot related

    # Connect to the robot
    session = qi.Session()
    session.connect("tcp://" + constants['ip'] + ":" + str(constants['port']))
    posture_service = session.service("ALRobotPosture")
    posture_service.goToPosture("StandInit", 0.5)
    background_movement = session.service("ALBackgroundMovement")

    # Disable the BACKGROUND_MOVEMENT AutonomousAbility
    background_movement.setEnabled(False)

    image_dir = 'patterns_uncovered'
    masked_image_dir ='masked' #'masked'
    train_dir = 'patterns_train'
    mask_capture_dir = 'masked_captured'
    window = ImageSlideshow(image_dir, masked_image_dir, train_dir, mask_capture_dir)
    window.show()


    sys.exit(app.exec())