import os
import subprocess
import shutil

''' This can be used to run several iterations of the eexperiment scripts in a row, 
e.g. when doing robot only runs.'''

# Define the names of your scripts
scripts = [
    "exp_setup_cond_1_robot_only",
    "exp_setup_cond_2_robot_only",
    "exp_setup_cond_3_robot_only"
]

# Number of iterations
iterations = 5

# Run the scripts
for i in range(1, iterations + 1):
    for script in scripts:
        # Run the script
        subprocess.run(["python3", f"{script}.py"])

        # Define the path to the generated file
        generated_file = "slideshow_summary.json"

        # Check if the file was created
        if os.path.exists(generated_file):
            # Define the new filename with the iteration number
            new_filename = f"slideshow_summary_{script}_iteration_{i}.json"

            # Rename the file
            shutil.move(generated_file, new_filename)
        else:
            print(f"Warning: {generated_file} not found after running {script}")

print("All iterations completed.")
