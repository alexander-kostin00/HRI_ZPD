
# file locations
# audio_path = '/home/robot-playground-main/multimodal_trust/store_audio/'
get_gameimages = '/home/robot-playground-main/multimodal_trust/gameimg/'  # bipolar, low res images for game play are saved here, need to be named with integer numbers (e.g. 1.png)
store_imageswnoise = '/home/robot-playground-main/multimodal_trust/store_imgwnoise/'  # image storage for Nao captures
store_gameimages = '/home/robot-playground-main/multimodal_trust/store_gameimg/' # concat image storage game, used in Hopfield

store_grids = '/home/robot-playground-main/multimodal_trust/gamegrid/'  # location of all grids
get_trainimgs = '/home/robot-playground-main/multimodal_trust/trainimg/' # location of training images
store_vtrainimgs = '/home/robot-playground-main/multimodal_trust/store_trainimg/' # location of training images
store_vatrainimgs = '/home/robot-playground-main/multimodal_trust/store_train_audioimg/' # location of training images visual audio

store_captured = '/home/robot-playground-main/multimodal_trust/store_captured/'
outputs_location = '/home/robot-playground-main/multimodal_trust/outputs/phase/'
store_audio = '/home/robot-playground-main/multimodal_trust/store_audio/' # image storage for human speech training

# Pepper setup
IP = "" # Pepper's IP address
IP2 = "" 
PORT = 9559  # Pepper's port, should remain unchanged

# The coordinates for cropping the image to the correct frame (manually generated from a captured example) for the offline settings

# left =  4 # x left
# top = 6  # y top
# right = 234  # x right
# bottom = 236  # y bottom

# Cropping of the captured images for online strategy
left =  13  # x left
top = 92  # y top
right =109 # x right
bottom = 189 # y bottom

# The coordinates for cropping images with social cues 
p_left =  20 # x left
p_top = 40  # y top
p_right = 570  # x right
p_bottom = 440 

# time variables these are magic numbers must be adjusted checked and tested before experiments.
time1 = 0.5  # time sleep after grid is shown
time2 = 0.5  # time to wait after image display
time3 = 0.3 # time wait after grid display. the initial value was 2, ewduce to 1
time4 = 0.3 # the initial value was 2, reduce to 1.
time5 = 0.5 # 5
time6 = 0.5
time7 = 1


length = 11  # the length of the game grid

# Note: width x length images need to be located in get_gameimages, named 0.png to width x length in integers
nruns = 10 # number of runs --> episodes
iterations = 20 # iteration to run the SARSA for
repeats = 10 # new repeat = new q-matrix for this 'run'. We set repeats to 10 for offline experiments.
rsize = (32, 32)  # size of the images, the images displayed on screen should be in the same format
ntrainimgs = 5  # number of images that the Hopfield net is trained with
epsilon = 0.3  # exploration parameter
gamma = 0.4  # discounting
probabilities = (0, 0.05, 0.1, 0.2, 0.25, 0.5, 0.6, 0.75, 0.7, 0.8, 0.85)
state_numbers = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

#Please change depending on the settings
experiment_online=True


#audio constants
fs = 44100  # Sample rate
seconds = 3  # Duration of recording
conditions = ['Trustworthy', 'Untrustworthy', 'Deceptive', 'Random']
audio_labels = ['sweet candy',  'shiny star', 'big heart', 'fast car', 'sharp scissors']
state_labels = ['L 5',  'L 4', 'L 3', 'L 2', 'L 1', '0', ' R 1', 'R 2', 'R 3', 'R 4', 'R 5']









