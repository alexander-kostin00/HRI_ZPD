from hopfieldnetwork import *
from grid import *
from audio import *
import matplotlib.pyplot as plt
import constants


def check_hopfield_convergence(
        base_directory='/home/oleksandr/PycharmProjects/HRI_ZPD/PatternsComplexityScale/exp_setup/hopfield/sets/'):
    # Open report.txt in append mode
    report_path = os.path.join(base_directory, 'report.txt')
    with open(report_path, 'a') as report_file:
        # Skip first three lines
        report_file.write("\n" * 3)
        # Write separator
        report_file.write("--------------------------------------------------------------\n")
        report_file.write('\n')
        report_file.flush()

        set_accuracies_dict = {}

        # Iterate over each set directory
        for set_dir in sorted(os.listdir(base_directory)):
            set_path = os.path.join(base_directory, set_dir) + '/'
            if os.path.isdir(set_path):
                # Load original pattern images
                original_images = sorted([f for f in os.listdir(set_path) if f.endswith('.png') and f.split('.')[0].isdigit()])
                train_images = bipolarize_pattern_robot_train(set_path, constants.ntrainimgs)
                weights_h = calc_weights(train_images)

                set_accuracies = []

                for original_image in original_images:
                    original_index = int(os.path.splitext(original_image)[0])
                    original_image_path = os.path.join(set_path, original_image)
                    original_pattern = bipolarize_pattern_robot(original_image_path)

                    # Iterate over each "masked_x" directory
                    masked_dir = os.path.join(set_path, f"masked_{original_index}")
                    if os.path.isdir(masked_dir):
                        masked_images = sorted([f for f in os.listdir(masked_dir) if f.endswith('.png')])

                        image_accuracies = []

                        for masked_image in masked_images:
                            masked_image_path = os.path.join(masked_dir, masked_image)
                            masked_pattern = bipolarize_pattern_robot(masked_image_path)

                            # Calculate Hopfield convergence
                            new_s, changed_bits, state_changes, epochs = calc_stateupdate_async(
                                masked_pattern, weights_h, 12000, 12000)

                            new_s_reversed = -1 * new_s
                            accuracy = np.max([
                                np.mean((original_pattern == new_s)),
                                np.mean((original_pattern == new_s_reversed))
                            ])
                            image_accuracies.append(accuracy)
                            report_file.write(
                                f"Accuracy for masked image {masked_image} in set {set_dir}: {accuracy}\n")
                            report_file.flush()
                            print(f"Accuracy for masked image {masked_image} in set {set_dir}: {accuracy}")

                            # Save the reconstructed image
                            reconstructed_bimg = new_s.reshape(constants.rsize)
                            recon_image_path = os.path.join(masked_dir, f"reconstructed_{masked_image}")
                            plt.imsave(recon_image_path, reconstructed_bimg, cmap='Greys')

                        mean_image_accuracy = np.mean(image_accuracies)
                        set_accuracies.append(mean_image_accuracy)
                        report_file.write(f"Mean accuracy for image {original_image}: {mean_image_accuracy}\n")
                        report_file.flush()
                        print(f"Mean accuracy for image {original_image}: {mean_image_accuracy}")

                mean_set_accuracy = np.mean(set_accuracies)
                set_accuracies_dict[set_dir] = mean_set_accuracy
                report_file.write(f"Mean accuracy for set {set_dir}: {mean_set_accuracy}\n")
                report_file.flush()
                print(f"Mean accuracy for set {set_dir}: {mean_set_accuracy}")
                report_file.write('\n')
                report_file.write("--------------------------------------------------------------\n")
                report_file.write('\n')
                report_file.flush()

        if set_accuracies_dict:
            highest_accuracy_set = max(set_accuracies_dict, key=set_accuracies_dict.get)
            highest_accuracy = set_accuracies_dict[highest_accuracy_set]
            report_file.write(
                f"The set with the highest accuracy is {highest_accuracy_set} with a mean accuracy of {highest_accuracy}\n")
            print(f"The set with the highest accuracy is {highest_accuracy_set} with a mean accuracy of {highest_accuracy}")

def main():
    check_hopfield_convergence()

if __name__ == '__main__':
    main()