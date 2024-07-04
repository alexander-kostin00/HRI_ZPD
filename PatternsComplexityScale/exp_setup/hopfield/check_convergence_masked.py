from hopfieldnetwork import *
from grid import *
from wn import *
from audio import *

# image convergence for images and noisy images
#train_imgs = bipolarize_pattern_robot_train(constants.store_vtrainimgs, constants.ntrainimgs)

#weights_h = calc_weights(train_imgs)
#accuracies = np.zeros((constants.ntrainimgs, len(constants.probabilities)))
set_path = '/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/Patterns/Set14_wmasks/Set14/'
check_directory = '/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/Masks_check/'


train_imgs = bipolarize_pattern_robot_train(set_path, constants.ntrainimgs)
weights_h = calc_weights(train_imgs)
accuracies = np.zeros(30)
n = 0

for mask_filename in os.listdir(check_directory):

    image_path = os.path.join(set_path, '3.png')
    compare_pattern = bipolarize_pattern_robot(image_path)
    mask_path = os.path.join(check_directory, mask_filename)
    mask_bin = bipolarize_pattern_robot(mask_path)

    new_s, changed_bits, state_changes, epochs = calc_stateupdate_async(mask_bin, weights_h, 12000, 12000)
    filename = os.path.join(check_directory, f'converged{n}.png')

    # Extract the flattened image from the 'images' array
    flattened_image = new_s

    # Reshape the flattened array back to the original shape
    reconstructed_bimg = flattened_image.reshape(constants.rsize)
    accuracies[n] = np.mean(compare_pattern == new_s)
    print(f"Accuracy for mask{n}, image 0: {accuracies[n]}")
    plt.imsave(filename, reconstructed_bimg, cmap='Greys')
    n += 1



