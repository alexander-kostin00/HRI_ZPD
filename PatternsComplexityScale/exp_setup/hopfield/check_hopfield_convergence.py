from hopfieldnetwork import *
from grid import *
from wn import *
from audio import *

# image convergence for images and noisy images
#train_imgs = bipolarize_pattern_robot_train(constants.store_vtrainimgs, constants.ntrainimgs)

#weights_h = calc_weights(train_imgs)
#accuracies = np.zeros((constants.ntrainimgs, len(constants.probabilities)))

base_directory = "/home/anna/codebase/git_codebase/HRI_ZPD/Hopfield/Patterns/"
n_sets = 20  # Number of sets
accuracies_per_set = []

for set_number in range(1, n_sets + 1):
    set_folder = f"Set{set_number}/"
    set_path = os.path.join(base_directory, set_folder)

    train_imgs = bipolarize_pattern_robot_train(set_path, constants.ntrainimgs)
    weights_h = calc_weights(train_imgs)
    accuracies = np.zeros((constants.ntrainimgs))

    for i in range(constants.ntrainimgs):
        image_path = os.path.join(set_path, f'{i}.png')
        compare_pattern = bipolarize_pattern_robot(image_path)

        new_s, changed_bits, state_changes, epochs = calc_stateupdate_async(compare_pattern, weights_h, 1000, 1000)
        filename = os.path.join(set_path, f'converged{i}.png')

        # Extract the flattened image from the 'images' array
        flattened_image = new_s

        # Reshape the flattened array back to the original shape
        reconstructed_bimg = flattened_image.reshape(constants.rsize)

        print(f"Reconstructed image shape for Set{set_number}, image {i}: {reconstructed_bimg.shape}")
        plt.imsave(filename, reconstructed_bimg, cmap='Greys')
        accuracies[i] = np.mean(compare_pattern == new_s)

    for accuracy in accuracies:
        if accuracy < 0.85:
            print(accuracy, 'LOW ACCURACY')
    accuracies_per_set.append(accuracies)
    print(f"Accuracies for Set{set_number}: {accuracies}")

print("All accuracies:", accuracies_per_set)