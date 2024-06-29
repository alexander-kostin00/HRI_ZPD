import os

# Define the base directory containing the sets
base_directory = "/home/anna/codebase/git_codebase/HRI_ZPD/Hopfield/Patterns"

# Iterate over each set directory
for set_number in range(1, 21):  # Assuming you have 20 sets
    set_directory = os.path.join(base_directory, f"Set{set_number}")

    # Check if the directory exists
    if not os.path.exists(set_directory):
        print(f"Directory {set_directory} does not exist.")
        continue

    # Get a list of all image files in the set directory
    image_files = [f for f in os.listdir(set_directory) if f.endswith(".png")]

    # Sort the image files to ensure consistent renaming
    image_files.sort()

    # Rename the images
    for i, image_file in enumerate(image_files):
        if i >= 5:
            print(f"More than 5 images in {set_directory}. Skipping extra images.")
            break

        old_file_path = os.path.join(set_directory, image_file)
        new_file_path = os.path.join(set_directory, f"{i}.png")

        os.rename(old_file_path, new_file_path)
        print(f"Renamed {old_file_path} to {new_file_path}")

print("Renaming completed.")