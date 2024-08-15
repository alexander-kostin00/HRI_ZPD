import qi




# Define the robot's IP address and port
robot_ip = '192.168.0.141'
port = 9559


# Speech rate (adjust to change speed)
speech_rate = 89

# Connect to the robot
session = qi.Session()
session.connect("tcp://" + robot_ip + ":" + str(port))


# Get the ALMotion service
motion_service = session.service("ALMotion")
speech_service = session.service("ALTextToSpeech")
posture_service = session.service("ALRobotPosture")
behavior_mng_service = session.service("ALBehaviorManager")

## Get the ALAnimatedSpeech service
animated_speech = session.service("ALAnimatedSpeech") #says a text and animates it with movements
speak_move_service = session.service("ALSpeakingMovement")
posture_service.goToPosture("StandInit", 0.5)
speech_service.setParameter("speed", speech_rate)


## Start active tracking

behavior_mng_service.runBehavior('p50_study1-5ba9db/basic_awareness_ON', _async=True)

# Speak the text with animation

def robot_speech(section):

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


    animated_speech.say(section)



robot_speech('Hello')
