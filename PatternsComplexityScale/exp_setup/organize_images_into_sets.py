from PatternsComplexityScale.creating_masks.creating_masks import CreatingMasks
from PatternsComplexityScale.exp_setup.hopfield.grid import *
import random
import shutil

def organize_images_into_sets(input_directory='hopfield/sets/', set_size=5, amount_masks_each_pattern=10, mask_visibility=0.2, mask_pieces=1):
    # Check if the input directory exists
    if not os.path.exists(input_directory):
        print(f"Error: The directory {input_directory} does not exist.")
        return

    # Get a list of files in the directory
    images = [f for f in os.listdir(input_directory) if f.startswith("image_")]

    # Check if there are more than 5 images
    if len(images) <= 5:
        print(f"Error: Not enough images in {input_directory}. Need more than 5 images.")
        return

    # Shuffle the images to ensure random selection
    random.shuffle(images)

    # Initialize set counter
    set_counter = 0

    # Create sets of images
    while len(images) >= set_size:
        # Take a batch of set_size images
        selected_images = images[:set_size]
        images = images[set_size:]

        # Create a new directory for this set
        set_directory = os.path.join(input_directory, str(set_counter))
        os.makedirs(set_directory, exist_ok=True)

        # Move and rename images in the new directory
        for idx, image in enumerate(selected_images):
            src_path = os.path.join(input_directory, image)
            ext = os.path.splitext(image)[1]  # Extract the file extension
            dest_filename = f"{idx}{ext}"
            dest_path = os.path.join(set_directory, dest_filename)
            shutil.move(src_path, dest_path)

            # Create masked directories
            masked_dir = os.path.join(set_directory, f"masked_{idx}")
            os.makedirs(masked_dir, exist_ok=True)

            # Generate 10 masked images
            for mask_idx in range(amount_masks_each_pattern):
                masked_image_path = os.path.join(masked_dir, f"masked_{idx}_{mask_idx}{ext}")
                create_masked_image(dest_path, masked_image_path, visible=mask_visibility, pieces=mask_pieces)

        print(f"Set {set_counter} created with {set_size} images.")
        set_counter += 1

    # Handle remaining images
    if images:
        set_directory = os.path.join(input_directory, str(set_counter))
        os.makedirs(set_directory, exist_ok=True)
        for idx, image in enumerate(images):
            src_path = os.path.join(input_directory, image)
            ext = os.path.splitext(image)[1]  # Extract the file extension
            dest_filename = f"{idx}{ext}"
            dest_path = os.path.join(set_directory, dest_filename)
            shutil.move(src_path, dest_path)

            # Create masked directories if not a full set
            masked_dir = os.path.join(set_directory, f"masked_{idx}")
            os.makedirs(masked_dir, exist_ok=True)

            # Generate 10 masked images
            for mask_idx in range(amount_masks_each_pattern):
                masked_image_path = os.path.join(masked_dir, f"masked_{idx}_{mask_idx}{ext}")
                create_masked_image(dest_path, masked_image_path, visible=mask_visibility, pieces=mask_pieces)

        # Check the number of images in the last directory
        if len(images) < set_size:
            # Remove the last directory if it contains less than set_size images
            print(f"Removing incomplete set {set_counter} with {len(images)} images.")
            shutil.rmtree(set_directory)
        else:
            print(f"Remaining {len(images)} images moved to set {set_counter}.")

def create_masked_image(input_path, output_path, visible, pieces):
    try:
        creating_masks = CreatingMasks(input_path, visible, pieces)
        creating_masks.create_visible_areas()
        creating_masks.cover_image()
        creating_masks.matrix_to_image(creating_masks.color_matrix, output_path)
    except Exception as e:
        print(f"Error generating mask for {input_path}: {e}")



def main():
    organize_images_into_sets()

if __name__ == '__main__':
    main()
