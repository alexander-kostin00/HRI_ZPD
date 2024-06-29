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
mean_accuracies_per_set = []

for set_number in range(1, n_sets + 1):
    set_folder = f"Set{set_number}/"
    set_path = os.path.join(base_directory, set_folder)

    train_imgs = bipolarize_pattern_robot_train(set_path, constants.ntrainimgs)
    weights_h = calc_weights(train_imgs)
    accuracies = np.zeros((constants.ntrainimgs, len(constants.probabilities)))


    for i in range(constants.ntrainimgs):
        image_path = os.path.join(set_path, f'{i}.png')
        compare_pattern = bipolarize_pattern_robot(image_path)

        for counter, value in enumerate(constants.probabilities):
            noise_img = sp_noise(set_path,i, value)

            filename = '/home/anna/codebase/git_codebase/HRI_ZPD/Hopfield/Patterns/%s' % counter + '.png'

            cv2.imwrite(filename, noise_img)

            current_pattern = bipolarize_pattern_robot(filename)

            new_s, changed_bits, state_changes, epochs = calc_stateupdate_async(current_pattern, weights_h, 1000, 1000)

            accuracies[i, counter] = np.mean(compare_pattern == new_s)





        for accuracy in accuracies[i]:
            if accuracy < 0.85:
                print(accuracy, 'LOW ACCURACY')
    mean_accuracies = np.mean(accuracies, axis = 1)
    accuracies_per_set.append(accuracies)
    mean_accuracies_per_set.append(np.mean(mean_accuracies))
    print(f"Accuracies for Set{set_number}: {accuracies}")

print("All accuracies:", accuracies_per_set)

print('Mean accuracy per set:', mean_accuracies_per_set)

set_sorted_by_descending_means = np.argsort(mean_accuracies_per_set)[::-1] + 1

print('The sets with the highest mean accuracy in descending order', set_sorted_by_descending_means)
