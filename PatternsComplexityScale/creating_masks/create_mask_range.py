import os
from creating_masks import generate_mask_file  # Import your generate_mask function from the module

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def generate_masks_for_parameters(input_paths, visible_range, num_masks_per_set, base_output_dir):
    for image_no, input_path in enumerate(input_paths):
        input_filename = os.path.basename(input_path).split('.')[0]
        for visible in visible_range:
            # Create a directory for each visible parameter
            output_dir = os.path.join(base_output_dir, f'{input_filename}/visible_{visible:.2f}')
            create_directory(output_dir)

            for i in range(num_masks_per_set):
                output_path = os.path.join(output_dir, f'mask_{i}_visible_{visible:.2f}_pattern_{image_no}.png')
                generate_mask_file(input_path, visible, num_pieces, output_path)

if __name__ == '__main__':
    input_paths = [
        '/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/images/Pattern_check/0.png',
        '/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/images/Pattern_check/2.png',
        '/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/images/Pattern_check/3.png',
        '/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/images/Pattern_check/4.png',
        '/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/images/Pattern_check/1.png'
    ] #'/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/creating_patterns/patterns_murat/1.png', '/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/Patterns/Set14_wmasks/Set14/4.png'

    visible_range = [0.2, 0.4] #[i / 25.0 for i in range(1, 21)]  # Generate 25 visible parameters from 0.04 to 0.8
    num_masks_per_set = 10
    num_pieces = 1  # Define the number of pieces;

    base_output_dir = '/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/images/Masks_check_new_set/'  # Define the base directory where masks will be saved

    generate_masks_for_parameters(input_paths, visible_range, num_masks_per_set, base_output_dir)
