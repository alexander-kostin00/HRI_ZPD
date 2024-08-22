import os

# Define the base path containing the first level of subdirectories
base_path = "/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/images/Mask_hopfield_2"

# Loop through each subdirectory in the base path
for subdir in os.listdir(base_path):
    subdir_path = os.path.join(base_path, subdir)

    # Ensure that subdir_path is indeed a directory
    if os.path.isdir(subdir_path):
        # Loop through the subfolders within this subdirectory
        for subfolder in os.listdir(subdir_path):
            subfolder_path = os.path.join(subdir_path, subfolder)

            # Ensure that subfolder_path is a directory
            if os.path.isdir(subfolder_path):
                # Loop through each file in the subfolder
                for filename in os.listdir(subfolder_path):
                    if "0.05" in filename:
                        # Construct the full file path
                        file_path = os.path.join(subfolder_path, filename)
                        # Delete the file
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")

print("Finished deleting files containing '0.05' in their filenames.")
