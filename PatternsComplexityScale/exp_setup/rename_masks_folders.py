import os
import re

# Define the base path containing the 5 subfolders
base_path = "/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/masks_hopfield"


# Function to extract the bracket number from the folder name
def extract_bracket_number(folder_name):
    match = re.search(r'bracket_(\d+)_', folder_name)
    return int(match.group(1)) if match else float('inf')  # Return a large number if no bracket number is found


# Loop through each of the 5 main subfolders in the base path
for subdir in os.listdir(base_path):
    subdir_path = os.path.join(base_path, subdir)

    # Ensure that subdir_path is indeed a directory
    if os.path.isdir(subdir_path):
        # Get a list of subfolders and sort them by the extracted bracket number
        subfolders = sorted(os.listdir(subdir_path), key=extract_bracket_number)

        # Loop through each subfolder and rename it to '1' to '17'
        for i, subfolder in enumerate(subfolders):
            subfolder_path = os.path.join(subdir_path, subfolder)

            # Ensure that subfolder_path is a directory
            if os.path.isdir(subfolder_path):
                # Generate the new name based on the index (1 to 17)
                new_name = str(i + 1)
                new_subfolder_path = os.path.join(subdir_path, new_name)

                # Rename the subfolder
                os.rename(subfolder_path, new_subfolder_path)
                print(f"Renamed: {subfolder_path} to {new_subfolder_path}")

print("Finished renaming subfolders.")
