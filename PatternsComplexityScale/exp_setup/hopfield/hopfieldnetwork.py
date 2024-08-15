# Hopfield Network

import numpy as np
from collections import deque




def calc_dotproduct(all_states, weights):
    """Calculates dot product between two matrices, here the states and the weights of our network.
    Parameters
    ----------
    all_states: State matrix of the network (e.g. set of binary images)
    weights: weight matrix (calculated by function calc_weights)
    """
    z = np.dot(all_states.T, weights)
    return z.T


def calc_dotproduct_async(states, weights_c):
    """Calculates summed product between a weight vector (one column of the weight matrix), and one set of states.
    Parameters
    ----------
    states: State matrix of the network (e.g. set of binary images)
    weights_c: weight matrix (calculated by function calc_weights)
    """
    z_async = 0
    for j in np.arange(0, len(weights_c)):
        z_async = z_async + weights_c[j]*states[j]
    return z_async


def get_sign(sum_sw):
    """Returns -1 if the input is smaller than zero and 1 if the input is larger than zero.
    Parameters
    ----------
    sum_sw: Integer/Float
    """
    theta = np.sign(sum_sw)
    return theta


def calc_weights(all_states):
    """Calculates the weights for the Hopfield Network using the states to train the network on.
    All set of states to train the network on, are passed in at once.
    Parameters
    ----------
    all_states: State matrix of the network (e.g. set of binary images)
    """
    w = np.dot(all_states, all_states.T)
    np.fill_diagonal(w, 0)
    return w


def calc_stateupdate(all_states, weights):
    """Calculates the state updates synchronously.
    Parameters
    ----------
    all_states: State matrix of the network (e.g. set of binary images)
    weights: weight matrix (calculated by function calc_weights)
    """
    epoch_count = 0
    max_epoch_count = 200
    while True:
        epoch_count += 1
        new_s = get_sign(calc_dotproduct(all_states, weights))
        test_converge = new_s == all_states
        if np.all(test_converge):
            print('converged after {} epocs'.format(epoch_count))
            break
        if epoch_count > max_epoch_count:
            print('did not converge after {}'.format(epoch_count))
            break
        all_states = new_s
    return new_s



def calc_stateupdate_async(all_states, weights, max_epoch_count, check_interval=150, start_check_epoch=2000):
    """Calculates the state updates asynchronously.
    Parameters
    ----------
    all_states: State matrix of the network (e.g. set of binary images)
    weights: weight matrix (calculated by function calc_weights)
    max_epoch_count: counter for epochs
    """
    changed_bits = 0
    epoch_count = 0
    state_update_count = 0
    new_s = np.copy(all_states)
    # Buffer to keep track of the last few states
    state_buffer = deque(maxlen=check_interval)


    while epoch_count < max_epoch_count:
        rand_ind = np.random.randint(len(all_states))  # pick a random pixel
        epoch_count += 1
        #print('the epoch count is:',epoch_count)
        wi = weights[rand_ind, :]
        new_value = get_sign(calc_dotproduct_async(all_states, wi))

        if new_s[rand_ind] != new_value:
            new_s[rand_ind] = new_value  # update one pixel in the image according to the state update rule
            changed_bits += 1  # increase changed bits if the pixel was changed from the original input
            #print('the state update count is', state_update_count)
        state_buffer.append(np.copy(new_s))  # Add current state to buffer

        if epoch_count >= start_check_epoch and (epoch_count - start_check_epoch) % check_interval == 0:  # check for convergence periodically
            #print('CONVERGENCE TEST', 'in epoch', epoch_count)
            if  np.array_equal(new_s, state_buffer[0]):
                print('Converged after {} epochs'.format(epoch_count))
                print('state changes', changed_bits)
                break

    return new_s, changed_bits, epoch_count
