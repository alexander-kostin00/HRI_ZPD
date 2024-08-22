import numpy as np
import os
import shutil

# Load the images_with_outputs data from the .npy file
file_path = "/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/images/Masks/images_with_hopfield_outputs.npy"
images_with_outputs = np.load(file_path, allow_pickle=True)

# Extract the changed_bits1 values
changed_bits = [entry[1] for entry in images_with_outputs]

# Sort the changed_bits1 values
sorted_bits = sorted(changed_bits)

# Create 17 brackets using percentiles
brackets = [np.percentile(sorted_bits, i * 100 / 17) for i in range(18)]  # 18 edges for 17 brackets

# Define the output directory
output_dir = "/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/images/Mask_hopfield_2"

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Sort images into the 17 quantile-based brackets and copy them to the corresponding folders
for image_data in images_with_outputs:
    image_path, changed_bits1, accuracy = image_data

    # Determine the appropriate bracket for the current changed_bits1 value
    for i in range(len(brackets) - 1):
        if brackets[i] <= changed_bits1 < brackets[i + 1]:
            bracket_name = f"bracket_{i + 1}_{int(brackets[i])}_to_{int(brackets[i + 1])}"
            bracket_dir = os.path.join(output_dir, bracket_name)

            # Create the directory for this bracket if it doesn't exist
            if not os.path.exists(bracket_dir):
                os.makedirs(bracket_dir)

            # Copy the image to the bracket directory
            shutil.copy(image_path, bracket_dir)
            break