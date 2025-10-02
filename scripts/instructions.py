'''
Instructions for the Clock experiment.
Version 2.0, 2025
author(s): @mc_vinding
'''

# Instructions for main screen
instructions = {
    'W-press':        'W-press\n\nInstruction:\n\nPress as soon as you experience the intention to do so.\n\nReport the time on the clock was when you experienced the first intention to press.',
    'M-press':        'M-press\n\nInstruction:\n\nPress as soon as you experience the intention to do so.\n\nReport the time on the clock was when you pressed.',
    'IB-singleTone':  'Tone only\n\nInstruction:\n\nDo not press. A tone will be played at a random time.\n\nReport the time on the clock was when you heard the tone',                                   # singleTone
    'IB-singlePress': 'Press only\n\nInstruction:\n\nPress as soon as you experience the intention to do so.\n\nReport the time on the clock was when you pressed.',                                      # singlePress
    'IB-press':       'Press\n\nInstruction:\n\nPress as soon as you experience the intention to do so. A tone will follow the press.\n\nReport the time on the clock was when you pressed.',        # actionPress
    'IB-tone':        'Tone\n\nInstruction:\n\nPress as soon as you experience the intention to do so. A tone will follow the press.\n\nReport the time on the clock was when you heard the tone',  # actionTone
    'W-interval':'',
    'M-interval':'',
    # distalPress
    # distalTone
    # singleDistalPress
    'interruption': 'Interruption\n\nInstruction:\n\nPress as soon as you experience the intention to do so. At a random time, the clock will change color and then you must press as fast as possible.\n\nReport the time on the clock was when you pressed.',
}

# Questions for answer screen
questions = {
    'W-press':          'What was the time when you experienced the first intention to press?',
    'M-press':          'What was the time when you pressed?',
    'IB-singleTone':    'What was the time when you heard the tone?',
    'IB-singlePress':   'What was the time when you pressed?',
    'IB-press':         'What was the time when you pressed?',
    'IB-tone':          'What was the time when you heard the tone?',
    'W-interval':'',
    'M-interval':'',
    'interruption':     'What was the time when you pressed?'
}