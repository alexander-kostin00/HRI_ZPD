import os
from creating_masks import generate_mask  # Import your generate_mask function from the module

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def generate_masks_for_parameters(input_paths, visible_range, num_masks_per_set):
    for input_path in input_paths:
        for visible in visible_range:
            # Create a directory for each visible parameter
            input_filename = os.path.basename(input_path).split('.')[0]
            output_dir = f'masks/{input_filename}/visible_{visible}'
            create_directory(output_dir)

            for i in range(num_masks_per_set):
                output_path = os.path.join(output_dir, f'mask_{i + 1}.png')
                generate_mask(input_path, visible, num_pieces, output_path)

if __name__ == '__main__':
    input_paths = [
        '/home/anna/codebase/git_codebase/HRI_ZPD/Hopfield/Patterns/Set14_wmasks/Set14/0.png',
        '/home/anna/codebase/git_codebase/HRI_ZPD/Hopfield/Patterns/Set14_wmasks/Set14/1.png',
        '/home/anna/codebase/git_codebase/HRI_ZPD/Hopfield/Patterns/Set14_wmasks/Set14/2.png',
        '/home/anna/codebase/git_codebase/HRI_ZPD/Hopfield/Patterns/Set14_wmasks/Set14/3.png',
        '/home/anna/codebase/git_codebase/HRI_ZPD/Hopfield/Patterns/Set14_wmasks/Set14/4.png'
    ]

    visible_range = [i / 25.0 for i in range(1, 21)]  # Generate 25 visible parameters from 0.04 to 0.8
    num_masks_per_set = 100
    num_pieces = 5  # Define the number of pieces;

    generate_masks_for_parameters(input_paths, visible_range, num_masks_per_set)
