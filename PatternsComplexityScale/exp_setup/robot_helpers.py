import qi
import constants
import numpy as np
from PIL import Image
import time

def capture_robot_camera():
    """ Capture images from Robot's TOP camera. Note that the Nao's
        camera resolution is lower than the Pepper robot.
        Remember you need to subscribe and unsubscribe respectively
        see, https://ai-coordinator.jp/pepper-ssd#i-3
    """
    SubID = "Pepper" #change to NAO if needed
    session = qi.Session()
    session.connect("tcp://" + constants.ip + ":" + str(constants.port))

    videoDevice_robot = session.service('ALVideoDevice')
    # subscribe top camera, Image of 320*240px
    AL_kTopCamera, AL_kQVGA, Frame_Rates = 0, 1, 5  # 2.5  #10
    AL_kBGRColorSpace = 13  # Buffer contains triplet on the format 0xRRGGBB, equivalent to three unsigned char
    captureDevice_nao = videoDevice_robot.subscribeCamera(SubID, AL_kTopCamera, AL_kQVGA, AL_kBGRColorSpace, Frame_Rates)

    width, height = 320, 240
    image = np.zeros((height, width, 3), np.uint8)
    result = videoDevice_robot.getImageRemote(captureDevice_nao)

    if result == None:
        print("Camera problem.")
    elif result[6] == None:
        print("No image. ")
    else:
        # translate value to mat
        values = result[6]
        i = 0
        for y in range(0, height):
            for x in range(0, width):
                image[y, x, 0] = values[i + 0]
                image[y, x, 1] = values[i + 1]
                image[y, x, 2] = values[i + 2]
                i += 3

    # unsubscribe from the camera
    videoDevice_robot.unsubscribe(captureDevice_nao)
    return result[6], image

def robot_speech(text):

    '''This function executes Pepper speech and behavior. The input needs to be in the following format:

    text = 'message to speak as string'

    where text is a string of words for Pepper to say,
    The speech is executed as an animated speech.
    The defined text can include the behavior mode ^mode(), pitch \\vct=120\\ and rate \\rspd=80\\ info.
    '''
    session = qi.Session()
    session.connect("tcp://" + constants.ip + ":" + str(constants.port))

    animated_speech = session.service("ALAnimatedSpeech")  # says a text and animates it with movements

    animated_speech.say(text)


def robot_speech_behavior(section):

    '''This function executes Pepper speech and behavior. The input needs to be in the following format:

    section = [
    [time11, text1, behav1, time12],
    ...
    [time51, text5, behav5, time52],
    etc.
    ]

    where text is a string of words for Pepper to say, the behavior is a special behavior to execute during the speech
    and time can be used to ensure the timing of speech to behavior is good.
    The speech is executed as an animated speech.
    The defined text can include the behavior mode ^mode(), pitch \\vct=120\\ and rate \\rspd=80\\ info.
    '''
    session = qi.Session()
    session.connect("tcp://" + constants.ip + ":" + str(constants.port))

    animated_speech = session.service("ALAnimatedSpeech")  # says a text and animates it with movements
    behavior_mng_service = session.service("ALBehaviorManager")

    for line in section:



        behavior_mng_service.runBehavior(line[2], _async=True)

        time.sleep(line[0])  # extracts the first time

        animated_speech.say(line[1])



        time.sleep(line[3]) # extracts the second time


def close_running_behavs():

    session = qi.Session()
    session.connect("tcp://" + constants.ip + ":" + str(constants.port))
    behavior_mng_service = session.service("ALBehaviorManager")
    names = behavior_mng_service.getRunningBehaviors()

    print(names)

    for behavior in names:
        behavior_mng_service.stopBehavior(behavior)

    print(names)

result, image = capture_robot_camera()

img = Image.fromarray(image)

filename_vis = 'test.png'
img.save(filename_vis)