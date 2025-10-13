"""
Configuration file for Clock test experiment
Modify these settings to customize your experiment

OPTIONS FOR CONDITIONS: 
 'W-press': Press. Report time of intention (W-time). cf. Libet et al. 1983.
 'M-press': Press. Report time of intention (M-time). cf. Libet et al. 1983
 'IB-press': Indicate when a press is made. Part of the Intentional Binding paradigm. cf. Haggard et al. 2002.
 'IB-tone': Indicate when a tone is heard. Part of the Intentional Binding paradigm. cf. Haggard et al. 2002.
 'IB-singleTone': Indicate when a single tone is heard. Part of the Intentional Binding paradigm. cf. Haggard et al. 2002.
 'IB-singlePress': Indicate when a single press is made. Part of the Intentional Binding paradigm. cf. Haggard et al. 2002.
 'interruption': Libertus interuptus. cf. Schurger et al. 2012.

OTHER IMPORTANT SETTINGS:
    'letterMode': Whether to run in letter-memory mode (True/False). cf. Vinding et al. 2012 and Vinding et al. 2015.
    'triggerOutput': Whether to send trigger outputs (True/False)

"""

# ==================== EXPERIMENTAL DESIGN ====================
# Trial and data options
condition_keys = ['IB-singleTone','IB-singlePress','IB-press','IB-tone']
blockRepetitions = 2                                # Number of times each block will occur
trainingCondition_keys = ['IB-press','IB-tone']     # Keys to identify what type of block to run in training
trainingBlockRepetitions = 1                        # Number of times each block will occur in training
letterMode = False                                  # Whether to run in letter-memory mode (True/False)
triggerOutput = False                               # Whether to send trigger outputs via parallel port (True/False)

# Trials per block
trainingTrials = 5                                  # Number of initial training-trials per block
BlockTrials = 25                                    # Number of trials per block

# ==================== DISPLAY SETTINGS ====================
# Monitor configuration
monDistance = 70                                    # Distance from subject eyes to monitor (in cm)
monWidth = 30                                       # Width of monitor display (in cm)
fullscr = False                                     # Run in fullscreen mode (set to True for experiments)
framerate = 60                                      # Framerate of monitor (in Hz)

# Visual appearance
textSize = 0.8                                      # Size of text in degrees
circleRadius = 2                                    # Radius of circle (in degrees)
dotSize = circleRadius/10                           # Size of dot (in degrees)
tics = 12                                           # Number of tics on circle

# ==================== TIMING SETTINGS ====================
# Clock behavior
clockSpeed = 2.56                                   # Rotation speed of clock (seconds per full rotation)
clockDirection = 'clockwise'                        # 'clockwise' or 'counterclockwise'
drawMode = 'dot'                                    # 'dot' or 'hand'

# Event timing
toneOnset = [1.5, 7]                                # [earliest, latest] onset range of tone in singleTone condition (in seconds)
toneDelay = 0.25                                    # Delay of tone (in seconds) relative to response after response (in seconds)
dotDelay = [36, 60]                                 # [earliest, latest] duration of dot, after last event (in frames)

# Adaptive timeout settings (for interruption condition)
timeOutRatio = 0.5                                  # Target ratio of responses before timeout (0.0-1.0)
timeOutWinBase = [2.0, 8.0]                         # Base timeout window range [min, max] in seconds
averageVectorSize = 5                               # Number of recent trials used for adaptive calculation
timeOutScaleDown = [0.85, 0.95]                     # Multiplier range to decrease timeout [min, max]
timeOutScaleUp = [1.05, 1.15]                       # Multiplier range to increase timeout [min, max]

# ==================== AUDIO SETTINGS ====================
beepHz = 1000                                       # Frequency of sound
beepDuration = 0.1                                  # Duration (in seconds)

# ==================== LETTER SETTINGS ====================
letterDisplayTime = 0.8                             # Time a single letter is shown
letterSpaceTime = 0.2                               # Time of blank between letters
nletters = 30                                       # length of letter string.
nfwdValues = [3,4,5]                                # Possible n-fwd values

# ==================== TRIGGER SETTINGS ====================
leftTrigger     = 1
rightTrigger    = 2
commonTrigger   = 3
startTrigger    = 64

# ==================== INPUT SETTINGS ====================
# Key mappings
moveKeys = {
    'left': -20,
    'up': 1,
    'down': -1,
    'right': 20
}
errorKeys = ['f','num_subtract']
leftKeys = ['d']
rightKeys = ['k']
ansKeys = ['return','space']
timeOutKeys = ['y','n','num_add']
quitKeys = ['q','esc','escape']

# ==================== DATA SETTINGS ====================
# Data containers for each trial
dataCategories = ['id','condition','no','dotDelay','toneOnset','toneAngle','pressOnset','pressAngle','ansAngle','ansTime','timeOut','timeOutOnset','timeOutQuestion','stopCharacter','nFwd','userError','response']

# File paths
saveFolder = 'data'

# ==================== DERIVED SETTINGS ====================
# These are calculated from other settings - usually don't need to change
msScale = 1000
degScale = 10
