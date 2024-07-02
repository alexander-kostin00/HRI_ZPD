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

    #train the hopfield
    # bipolarise the training images and format them ready to be passed in the Hopfield net

    filename_trainimgs = '/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/Patterns/Set14_wmasks/Set14/' #Set 14 has the best convergence, chosen as game patten

    train_imgs = bipolarize_pattern_robot_train(filename_trainimgs, 5) # file to uncovered patterns and number of patterns

    np.save('/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/Patterns/Set14_wmasks/Set14/train_imgs.npy', train_imgs)

    weights_h= calc_weights(train_imgs)
    for image_path in image_paths:
        current_maskimage = bipolarize_pattern_robot(image_path)
        new_s1, changed_bits1, state_changes1, epochs1 = calc_stateupdate_async(current_maskimage, weights_h, 1000, 1000)
        images_with_outputs.append((image_path, changed_bits1))
        np.save('/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/Masks/images_with_hopfield_outputs.npy', train_imgs)
    return images_with_outputs


def sort_images_by_output(images_with_outputs, sorted_output_dir, output_ranges):
    for output_range in output_ranges:
        range_dir = os.path.join(sorted_output_dir, f'{output_range[0]}-{output_range[1]}')
        create_directory(range_dir)

    for image_path, output_value in images_with_outputs:
        for output_range in output_ranges:
            if output_range[0] <= output_value < output_range[1]:
                range_dir = os.path.join(sorted_output_dir, f'{output_range[0]}-{output_range[1]}')
                shutil.copy(image_path, range_dir)
                break


if __name__ == '__main__':
    base_dir = '/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/Masks'  # Directory where masks are saved
    sorted_output_dir = '/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/Masks_hopfield'  # Directory where sorted masks will be saved

    output_ranges = [(0, 50), (50, 100), (100, 150), (150, 200), (200, 250), (250, 300), (300, 350), (350, 400),
                     (400, 500), (500, 550), (550, 600), (600, 650), (650, 700), (700, 750), (750, 800), (800, 850),
                     (850, 900), (900, 950), (950, 1000)]  # Define output ranges

    # Step 1: Collect all image paths
    image_paths = collect_all_image_paths(base_dir)


    # Step 2: Run Hopfield network on all images and collect outputs
    images_with_outputs = run_hopfield_on_images(image_paths)

    # Step 3: Sort and organize images based on output values
    sort_images_by_output(images_with_outputs, sorted_output_dir, output_ranges)