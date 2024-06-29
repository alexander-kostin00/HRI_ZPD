from grid import *  # contains code relating to the images and grids to be displayed
from nao_imagecapture import *  # contains code to capture Nao vision
import time
from PIL import Image
import constants
# from recaudio import audio_pepper
import constants
from audio import *

'''This script trains the Hopfield Network. The playing Pepper needs to be placed in front of an external monitor. 
 The training images will be displayed on the external monitor. The disoayed image will be saved.'''

cv2.CV_LOAD_IMAGE_GRAYSCALE = 0
cv2.CV_LOAD_IMAGE_COLOR = 0

# capture images for training of the Hopfield Net
time.sleep(2)
for nimage in range(0, constants.ntrainimgs):
    print(constants.get_trainimgs)
    display_image(constants.get_trainimgs, nimage, constants.time2)
    time.sleep(constants.time1)
    result, image = capture_robot_camera_nao(constants.IP, constants.PORT)
    img = Image.fromarray(image)
    img_res = img.crop((constants.left, constants.top, constants.right, constants.bottom))
    filename = constants.store_vtrainimgs + '%s' % nimage + '.png'
    img_res.save(filename)
    time.sleep(constants.time1)
    finish_display_image()

time.sleep(1)


#bipolarise the training images and format them ready to be passed in the Hopfield net

train_imgs = bipolarize_pattern_robot_train(constants.store_vatrainimgs, constants.ntrainimgs)


np.save('/home/path/robot-playground-main/multimodal_trust/store_train_audioimg/train_imgs.npy', train_imgs)
