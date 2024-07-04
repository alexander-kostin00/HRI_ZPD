import os


def rename_masks(root_folder):
    # Traverse through the root directory
    for image_no_folder in os.listdir(root_folder):
        image_no_path = os.path.join(root_folder, image_no_folder)

        if os.path.isdir(image_no_path):
            # Check each subfolder inside the image_no_folder
            for visibility_folder in os.listdir(image_no_path):
                visibility_path = os.path.join(image_no_path, visibility_folder)

                if os.path.isdir(visibility_path):
                    # Iterate through each mask file in the visibility folder
                    for mask_filename in os.listdir(visibility_path):
                        mask_path = os.path.join(visibility_path, mask_filename)

                        if os.path.isfile(mask_path):
                            # Create the new mask name with visibility and image_no
                            new_mask_name = f"{visibility_folder}_{image_no_folder}_{mask_filename}"
                            new_mask_path = os.path.join(visibility_path, new_mask_name)

                            # Ensure the new mask path is unique
                            count = 1
                            base_new_mask_path = new_mask_path
                            while os.path.exists(new_mask_path):
                                name, ext = os.path.splitext(base_new_mask_path)
                                new_mask_path = f"{name}_{count}{ext}"
                                count += 1

                            # Rename the file
                            os.rename(mask_path, new_mask_path)
                            print(f"Renamed: {mask_path} to {new_mask_path}")


# Specify the root folder
root_folder = '/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/Masks/'

# Call the rename function
rename_masks(root_folder)