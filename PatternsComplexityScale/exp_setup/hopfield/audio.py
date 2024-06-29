import numpy as np
from numpy import loadtxt
import matplotlib.pyplot as plt
from scipy.io import wavfile
import cv2
import constants
import datetime



def hopfield_format(path, no_imgs):

    """ Converts pattern images in folder for training into Hopfield training format.
    Parameters
    -----------
    path: filename
    location where the image is located
    no_imgs: integer
    amount of training images

    Return
    -------
    images in format for Hopfield Network"""

    print('This is generating the training images.')
    images = np.zeros((constants.rsize[0] * constants.rsize[1], no_imgs))
    for j in range(no_imgs):
        # image directory with image names as ordered ints
        filename = path + '%s' % j + '.png'
        image = cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE)
        images[:, j] = image.flatten()

    return images

def concat_audio_visual(visual_img_path, savepath, imgn):
    """ preprocess video image for hopfield network
    """
    
    img_v = cv2.imread(visual_img_path + '%s.png' % imgn, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    img_v = inverted_image = cv2.bitwise_not(img_v)
    rimg_v = cv2.resize(img_v, constants.rsize, interpolation=cv2.INTER_AREA)
    
    savename = savepath + '%s.png' % imgn

    plt.imsave(savename, rimg_v, cmap = 'Greys')

def concat_audio_visual2(visual_img_path, savepath, imgn):
    """ preprocess video image for hopfield network
    """
    img_v = cv2.imread(visual_img_path + '%s.png' % imgn, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    img_v = inverted_image = cv2.bitwise_not(img_v)
    rimg_v = cv2.resize(img_v, constants.rsize, interpolation=cv2.INTER_AREA)
    bimg_v = cv2.threshold(rimg_v, 125, 255, cv2.THRESH_BINARY)[1] 
    # image_h = cv2.hconcat([bimg_a, rimg_v])
    savename = savepath + '%s.png' % imgn
    # these lines must be uncommented if check of the captured images is required.
    # dt = datetime.datetime.now()
    # timestamp = '%s-%s-%s_%s:%s:%s' % (dt.month, dt.day, dt.year, dt.hour, dt.minute, dt.second)
    # img_name = '/home/path/test_captured/' + timestamp + '_gameimg.png' 
    # plt.imsave(img_name, bimg_v, cmap = 'Greys')
    plt.imsave(savename, bimg_v, cmap = 'Greys')
