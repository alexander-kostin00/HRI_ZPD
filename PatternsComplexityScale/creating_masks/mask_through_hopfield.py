import os
import shutil
import sys
import numpy as np

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


def run_hopfield_on_images(image_paths):
    images_with_outputs = []

    # Train the hopfield
    # Bipolarize the training images and format them ready to be passed in the Hopfield net
    filename_trainimgs = '/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/Patterns/Set14_wmasks/Set14/'  # Set 14 has the best convergence, chosen as game pattern

    train_imgs = bipolarize_pattern_robot_train(filename_trainimgs,
                                                5)  # File to uncovered patterns and number of patterns
    np.save(
        '/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/Patterns/Set14_wmasks/Set14/train_imgs.npy',
        train_imgs)

    weights_h = calc_weights(train_imgs)
    for image_path in image_paths:
        compare_path = os.path.join(filename_trainimgs, '0.png')
        compare_pattern = bipolarize_pattern_robot(compare_path)
        current_maskimage = bipolarize_pattern_robot(image_path)
        new_s1, changed_bits1, state_changes1, epochs1 = calc_stateupdate_async(current_maskimage, weights_h, 1000,
                                                                                1000)
        accuracy = np.mean(compare_pattern == new_s1)
        images_with_outputs.append((image_path, changed_bits1, accuracy))
        print('The accuracy for', image_path, 'is', accuracy)

    # Convert to a structured array
    dtype = [('image_path', 'U256'), ('changed_bits', 'int32'), ('accuracy', 'float64')]
    structured_array = np.array(images_with_outputs, dtype=dtype)
    np.save(
        '/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/Masks/images_with_hopfield_outputs.npy',
        structured_array)

    return images_with_outputs


def sort_images_by_output(images_with_outputs, sorted_output_dir, output_ranges):
    for output_range in output_ranges:
        range_dir = os.path.join(sorted_output_dir, f'{output_range[0]}-{output_range[1]}')
        create_directory(range_dir)

    for image_path, output_value, accuracy_value in images_with_outputs:
        for output_range in output_ranges:
            if output_range[0] <= output_value < output_range[1] and accuracy_value > 0.6:
                range_dir = os.path.join(sorted_output_dir, f'{output_range[0]}-{output_range[1]}')
                shutil.copy(image_path, range_dir)
                break


if __name__ == '__main__':
    base_dir = '/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/Masks/0'  # Directory where masks are saved
    sorted_output_dir = '/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/Masks_hopfield'  # Directory where sorted masks will be saved

    output_ranges = [
        (0, 50), (50, 62), (62, 74), (74, 86), (86, 98), (98, 110), (110, 122),
        (122, 134), (134, 146), (146, 158), (158, 170), (170, 182), (182, 194),
        (194, 206), (206, 218), (218, 230), (230, 242), (242, 254), (254, 266),
        (266, 278), (278, 290), (290, 302), (302, 314), (314, 326), (326, 338),
        (338, 350), (350, 362), (362, 374), (374, 386), (386, 398), (398, 410),
        (410, 422), (422, 434), (434, 446), (446, 458), (458, 470), (470, 482),
        (482, 494), (494, 506), (506, 1000)
    ]  # Define output ranges

    # Step 1: Collect all image paths
    image_paths = collect_all_image_paths(base_dir)

    # Step 2: Run Hopfield network on all images and collect outputs
    images_with_outputs = run_hopfield_on_images(image_paths)

    # Step 3: Sort and organize images based on output values
    sort_images_by_output(images_with_outputs, sorted_output_dir, output_ranges)