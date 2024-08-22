from hopfieldnetwork import *
from grid import *
from wn import *
from audio import *

# image convergence for images and noisy images
#train_imgs = bipolarize_pattern_robot_train(constants.store_vtrainimgs, constants.ntrainimgs)

#weights_h = calc_weights(train_imgs)
#accuracies = np.zeros((constants.ntrainimgs, len(constants.probabilities)))
set_path = '/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/images/Pattern_check/'
#set_path = '/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/creating_patterns/patterns_murat/'
#set_path = '/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/images/Patterns/Set14_wmasks/Set14/' # 5 pattern images for training
#set_path = '/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/images/Pattern_check/'
check_directory = '/home/anna/codebase/git_codebase/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/images/Masks_check/' # set 0f any amount of masked images with e.g. 20% visibility


train_imgs = bipolarize_pattern_robot_train(set_path, constants.ntrainimgs)
weights_h = calc_weights(train_imgs)
accuracies = np.zeros(30)
n = 0

for mask_filename in os.listdir(check_directory):

    image_path = os.path.join(set_path, '0.png')
    compare_pattern = bipolarize_pattern_robot(image_path)
    mask_path = os.path.join(check_directory, mask_filename)
    mask_bin = bipolarize_pattern_robot(mask_path)

    new_s, changed_bits, epochs = calc_stateupdate_async(mask_bin, weights_h, 4000)
    filename = os.path.join(check_directory, f'converged{n}.png')

    # Extract the flattened image from the 'images' array
    flattened_image = new_s
    new_s_reversed = new_s * -1

    # Reshape the flattened array back to the original shape
    reconstructed_bimg = flattened_image.reshape(constants.rsize)
    accuracies[n] = max(np.mean(compare_pattern == new_s), np.mean(compare_pattern == new_s_reversed))
    print(f"Accuracy for mask{n}, image 0: {accuracies[n]}")
    plt.imsave(filename, reconstructed_bimg, cmap='Greys')
    n += 1



