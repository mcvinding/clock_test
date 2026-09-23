'''
Instructions for the Clock experiment.
Version 2.1, 2026
author(s): @mc_vinding
'''

# Instructions for main screen
instructions = {
    # Libet instructions
    'W-press':         'W-press\n\nInstruction:\n\nPress as soon as you experience the intention to do so.\n\nReport the time on the clock when you experienced the first intention to press.',
    'M-press':         'M-press\n\nInstruction:\n\nPress as soon as you experience the intention to do so.\n\nReport the time on the clock when you pressed.',

    # Intentional binding instructions
    'IB-singleTone':   'Tone only \n\nInstruction:\n\nDo not press. A tone will be played at a random time.\n\nReport the time on the clock when you heard the tone',                                   # singleTone
    'IB-singlePress':  'Press only\n\nInstruction:\n\nPress as soon as you experience the intention to do so.\n\nReport the time on the clock when you pressed.',                                      # singlePress
    'IB-press':        'Press\n\nInstruction:\n\nPress as soon as you experience the intention to do so. A tone will follow the press.\n\nReport the time on the clock when you pressed.',        # actionPress
    'IB-tone':         'Tone \n\nInstruction:\n\nPress as soon as you experience the intention to do so. A tone will follow the press.\n\nReport the time on the clock when you heard the tone',  # actionTone

    # Distal intentions instructions
    'distalPress':     'Distal Press\n\nInstruction:\nWhen you intend to act, note which letter is in the center of the clock. Press the button when this letter appears again.\n\nReport the time on the clock when you pressed.',
    'distalTone':      'Distal Tone \n\nInstruction:\nWhen you intend to act, note which letter is in the center of the clock. Press the button when this letter appears again.\n\nReport the time on the clock when you heard the tone.',
    'singleDistPress': 'Distal Press\n\nInstruction:\nWhen you intend to act, note which letter is in the center of the clock. Press the button when this letter appears again.\n\nReport the time on the clock when you pressed.',

    # Libertus interuptus instructions
    'interruption':    'Interruption\n\nInstruction:\n\nPress as soon as you experience the intention to do so. At a random time, the clock will change color and then you must press as fast as possible.\n\nReport the time on the clock when you pressed.',

    # Interval task [not implemented]
    'W-interval':'',
    'M-interval':'',
}

# Questions for answer screen
questions = {
    'W-press':         'What was the time when you experienced the first intention to press?',
    'M-press':         'What was the time when you pressed?',

    'IB-singleTone':   'What was the time when you heard the tone?',
    'IB-singlePress':  'What was the time when you pressed?',
    'IB-press':        'What was the time when you pressed?',
    'IB-tone':         'What was the time when you heard the tone?',

    'distalPress':     'What was the time when you pressed?',
    'distalTone':      'What was the time when you heard the tone?',
    'singleDistPress': 'What was the time when you pressed?',

    'interruption':    'What was the time when you pressed?',

    'W-interval':'',
    'M-interval':''
}