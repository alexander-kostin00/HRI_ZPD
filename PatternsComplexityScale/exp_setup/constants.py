constants = {
    'feedback_message_duration': 3000,       # milliseconds
    'pattern_image_display_duration': 1000,  # milliseconds
    'number_image_display_duration': 2000,   # milliseconds
    'mask_visibility_initial': 0.4,
    'mask_level_initial': 7,
    'mask_pieces_min': 1,
    'mask_pieces_max': 1,
    'decreasing_step': 0.05,    # value that is taken away from the visibility percentage
    'increasing_step': 0.05,  # value that is added to the visibility percentage
    'visibility_maximum': 0.80,   # upper limit
    'visibility_minimum': 0.5,  # lower limit
    'ip': '192.168.0.141', #Pepper 4: '192.168.0.141'
    'port': 9559,
    'rsize': (32, 32), # size of images passed into Hopfield,
    'left_t': 175, # training pattern cropping coordinates
    'top_t': 138,
    'right_t': 247,
    'bottom_t': 210,
    'left_m': 150,  # masked pattern cropping coordinates
    'top_m': 147,
    'right_m': 213,
    'bottom_m': 207
}

