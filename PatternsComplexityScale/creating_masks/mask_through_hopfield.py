import os
import shutil
import sys
from tabnanny import check

import numpy as np
import glob
import re

# Add the project root directory to the sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(project_root)

from PatternsComplexityScale.exp_setup.hopfield.grid import bipolarize_pattern_robot, bipolarize_pattern_robot_train
from PatternsComplexityScale.exp_setup.hopfield.hopfieldnetwork import calc_stateupdate_async, calc_weights


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)


def collect_all_image_paths(base_dir):
    image_paths = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.png'):
                image_paths.append(os.path.join(root, file))
    return image_paths

def check_similarity(converged_image, correct_pattern):
    ''''This function checks how similar a converged image (from a masked image shown) is to each of the training
        and returns the training image that is most similar. In this way it allows the robot to choose the image it
        recognizes.
        '''
    accuracies = np.zeros(5)
    filename_trainimgs = "/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/images/Pattern_check/clean/"
    check_correct = False

        # pattern paths

    pattern_path = os.path.join(filename_trainimgs, f'*.png')
        # Use glob to get all file paths matching the pattern
    filepaths = glob.glob(pattern_path)

    for n, pattern_path in enumerate(filepaths):
        compare_pattern = bipolarize_pattern_robot(pattern_path)
        # Regular expression to find the number before .png
        match = re.search(r'(\d+)\.png$', pattern_path)

        # Extract and print the number if found
        if match:
            number = int(match.group(1))
            print(number)
            accuracies[number] = np.mean(compare_pattern == converged_image)
            print(f"Accuracy for pattern{number}: {accuracies[number]}", pattern_path)
        else:
            print("No number found before .png")



    max_pattern = np.argmax(accuracies)
    if max_pattern == correct_pattern:
        check_correct = True
        print('True')

    return check_correct


def run_hopfield_on_images(image_paths):
    images_with_outputs = []
    discarded = 0

    # Train the hopfield
    # Bipolarize the training images and format them ready to be passed in the Hopfield net
    filename_trainimgs = "/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/images/Pattern_check/"  # Set 14 has the best convergence, chosen as game pattern

    train_imgs = bipolarize_pattern_robot_train(filename_trainimgs,
                                                5)  # File to uncovered patterns and number of patterns
    np.save(
        '/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/images/Pattern_check/train_imgs.npy',
        train_imgs)

    weights_h = calc_weights(train_imgs)
    for image_path in image_paths:
        compare_path = os.path.join(filename_trainimgs, '4.png')
        compare_pattern = bipolarize_pattern_robot(compare_path)
        current_maskimage = bipolarize_pattern_robot(image_path)
        new_s1, changed_bits1, epochs1 = calc_stateupdate_async(current_maskimage, weights_h, 4000)


        accuracy = np.mean(compare_pattern == new_s1)
        check_recognised = check_similarity(new_s1, 4)
        if check_recognised:
            images_with_outputs.append((image_path, changed_bits1, accuracy))
            print('The accuracy for', image_path, 'is', accuracy)
        if not check_recognised:
            discarded += 1


    # Convert to a structured array
    dtype = [('image_path', 'U256'), ('changed_bits', 'int32'), ('accuracy', 'float64')]
    structured_array = np.array(images_with_outputs, dtype=dtype)
    np.save(
        '/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/images/Masks/images_with_hopfield_outputs.npy',
        structured_array)
    print("amount discarded:", discarded)

    return images_with_outputs


def sort_images_by_output(images_with_outputs, sorted_output_dir, output_ranges):
    for output_range in output_ranges:
        range_dir = os.path.join(sorted_output_dir, f'{output_range[0]}-{output_range[1]}')
        create_directory(range_dir)

    for image_path, output_value, accuracy_value in images_with_outputs:
        for output_range in output_ranges:
            if output_range[0] <= output_value < output_range[1] and accuracy_value > 0.9:
                range_dir = os.path.join(sorted_output_dir, f'{output_range[0]}-{output_range[1]}')
                shutil.copy(image_path, range_dir)
                break


if __name__ == '__main__':
    base_dir = '/home/anna/codebase/git_codebase/HRI_ZPD/PatterPatterPatternsComplexityScale/exp_setup/hopfield/images/Masks/4'  # Directory where masks are saved
    sorted_output_dir = '/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/images/Masks_hopfield'  # Directory where sorted masks will be saved

    output_ranges = [
        (0, 62), (62, 79), (79, 96), (96, 113), (113, 130), (130, 147),
        (147, 164), (164, 181), (181, 198), (198, 215), (215, 232), (232, 249),
        (249, 266), (266, 283), (283, 300), (300, 317), (317, 1000)
    ]  # Define output ranges

    # Step 1: Collect all image paths
    image_paths = collect_all_image_paths(base_dir)

    # Step 2: Run Hopfield network on all images and collect outputs
    images_with_outputs = run_hopfield_on_images(image_paths)

    # Step 3: Sort and organize images based on output values
    sort_images_by_output(images_with_outputs, sorted_output_dir, output_ranges)