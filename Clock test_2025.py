'''
Clock experiment.
Version 3, 2025.
Useage: Run the script. Data is saved in a .csv file in a folder called "data".
Requirements: PsychoPy 1.80 or later (www.psychopy.org).

Created 2012-2025. @author(s): mc_vinding, Nygaard
'''
#----------------------- MISC -------------------------
#------------------------------------------------------
from __future__ import division
from psychopy import core, visual, sound, event, gui, monitors #parallel
from math import sin, cos, radians
from numpy import average
from random import shuffle, randint, uniform
import os, csv
from scripts.instructions import instructions, questions
from scripts.utils import get_condition_config
try:
    import winsound     # NB. There is known errors in timing using winsound (i.e. do not use)
    import thread
    windows = True
except ImportError:
    windows = False    

#-------------------- CONFIGURATION --------------------
#-------------------------------------------------------
# Import all settings from config file
try:
    from config import *
except ImportError:
    print("ERROR: Could not import config.py. Please ensure config.py exists in the same directory.")
    core.quit()

# Derived calculations (these depend on imported values)
dotStep = 360/clockSpeed/framerate                   # Degrees shift per monitor-frame
dataDict = dict(zip(dataCategories,['' for i in dataCategories]))

# Set monitor variables
myMon = monitors.Monitor('testMonitor')
myMon.setDistance(monDistance)
myMon.setWidth(monWidth)

# Intro dialogue
dialogue = gui.Dlg()
dialogue.addField('subjectID*')
dialogue.show()
if dialogue.OK:
    if dialogue.data[0].isdigit(): 
        subjectID = dialogue.data[0]
    else: 
        print('SUBJECT SHOULD BE DIGIT')
        core.quit()
else: core.quit()

# Make folder for data
saveFolder = 'data'
if not os.path.isdir(saveFolder): 
    os.makedirs(saveFolder)

# Clocks
trialClock = core.Clock()
soundClock = core.Clock()

#-------------------- STIMULI ----------------------
#---------------------------------------------------
win = visual.Window(monitor=myMon, size=myMon.getSizePix(), fullscr=fullscr, allowGUI=False, color='black', units='deg')   # Change fullscreen here: " fullscr=True/False "

mainText = visual.TextStim(win=win, height=textSize, color='white')
questionText = visual.TextStim(win=win, pos=(0, circleRadius*2), height=textSize, color='white')
fixation = visual.TextStim(win, text='+', color='white', height=textSize, antialias=False)

clockDot = visual.Circle(win=win, radius=dotSize/2, fillColor='#0000FF', lineColor='#0000FF')
clockDotTimeOut = visual.Circle(win=win, radius=dotSize/2, fillColor='#FF0000', lineColor='#FF0000') 
clockHand = visual.Line(win=win, start=(0,0), end=(0,circleRadius), lineColor='white', lineWidth=3)
clockHandTimeOut = visual.Line(win=win, start=(0,0), end=(0,circleRadius), lineColor='red', lineWidth=3)

#beep = sound.Sound(1000, secs=0.1)
beep = sound.Sound(1000, sampleRate=44100, secs=0.031, stereo=True)             # Standard tone

# Make complex figure: circle + tics + fixation cross. Render and save as single stimulus "circle"
visual.Circle(win, radius=circleRadius, edges=512, lineWidth=3, lineColor='white', fillColor=None).draw()
for angleDeg in range(0,360,int(360/tics)):
    angleRad = radians(angleDeg)
    begin = [circleRadius*sin(angleRad), circleRadius*cos(angleRad)]
    end = [begin[0]*1.1, begin[1]*1.1]
    visual.Line(win, start=(begin[0],begin[1]), end=(end[0],end[1]), lineColor='white', lineWidth=3).draw()

circle = visual.BufferImageStim(win)                                                    # Buffer it all in "circle" object
win.clearBuffer()

if clockDirection == 'counterclockwise':
    dotStep = -dotStep

# Setup additional settings
if letterMode:
    from scripts.utils import letters, makeLetterList
    blankSpace = visual.TextStim(win, text='', color='black', height=textSize, antialias=False)
    letterStim = visual.TextStim(win, color='white', height=textSize, antialias=False)
    letterClock = core.Clock()
    
if triggerOutput:
    from scripts.trigger_out import trigger
else:
    def trigger(x):             # Dummy function
        return

#-------------------- FUNCTIONS ----------------------
#-----------------------------------------------------
# Make a list of trials (dictionaries) given a condition
def makeBlock(condition,training):
    if training == True:
        conditionRep = trainingTrials          # Set number of training repetitions? 
    else:
        conditionRep = BlockTrials             # Set number of repetitions? 
        
    # Make a trialList with trialsPerPrime of each prime
    tmpTrials = [dict(dataDict.items()) for rep in range(conditionRep)]
    shuffle(tmpTrials)

    # Update every trial with trial-specific info
    trialList = ['']*conditionRep
    for trialNo in range(len(tmpTrials)):
        trialList[trialNo] = dict(tmpTrials[trialNo].items())
        trialList[trialNo]['no'] = trialNo+1
        trialList[trialNo]['id'] = subjectID
        trialList[trialNo]['condition'] = condition
        trialList[trialNo]['dotDelay'] = randint(dotDelay[0], dotDelay[1])
        if 'singleTone' in condition: 
            trialList[trialNo]['toneOnset'] = uniform(toneOnset[0], toneOnset[1])
    return trialList

# Dot or clack hand mode
if drawMode == 'dot':
    # Draws a dot on the circle, given an angle
    def drawDot(angleDeg, timeOut):
        if timeOut == False:
            angleRad = radians(angleDeg)
            x = circleRadius*sin(angleRad)
            y = circleRadius*cos(angleRad)
            clockDot.setPos([x,y])
            clockDot.draw()
        else:
            angleRad = radians(angleDeg)
            x = circleRadius*sin(angleRad)
            y = circleRadius*cos(angleRad)
            clockDotTimeOut.setPos([x,y])
            clockDotTimeOut.draw()
elif drawMode == 'hand':
    # Draws a hand on the circle, given an angle
    def drawDot(angleDeg, timeOut):
        if timeOut == False:
            angleRad = radians(angleDeg)
            x = circleRadius*sin(angleRad)
            y = circleRadius*cos(angleRad)
            clockHand.setEnd([x,y])
            clockHand.draw()
        else:
            angleRad = radians(angleDeg)
            x = circleRadius*sin(angleRad)
            y = circleRadius*cos(angleRad)
            clockHandTimeOut.setEnd([x,y])
            clockHandTimeOut.draw()

# Play beep on windows [THIS FUNCTION IS NOT USED!]
def windowsBeep():
    lock = thread.allocate_lock()
    lock.acquire()                                                                      # Entering critical section
    winsound.Beep(beepHz, int(beepDuration*msScale))
    lock.release()                                                                      # Exiting critical section

# Run a block of trials and save results
def runBlock(condition, training, letterMode=False):
    trialList = makeBlock(condition, training)
    
    # Configure block
    cfg = get_condition_config(condition)
    conid = cfg['conid']
    get_press = cfg['get_press']
    play_tone = cfg['play_tone']
    timeOut = cfg['timeOut']

    # Time out logic initialization (per block)
    timeOutCounter = 0
    timeOutListCounter = 0
    timeOutMeanList = []
    timeOutMeanListAverage = 0.5
    trialCounter = 0
    timeOutScale = 1

    # Set up .csv save function
    if not training:
        saveFile = saveFolder+'/subject_' +str(subjectID)+'_'+condition+'.csv'              # Filename for save-data
        csvWriter = csv.writer(open(saveFile, 'w', newline=''), delimiter=';').writerow     # The writer function to csv
        csvWriter(dataCategories)                                                           # Writes title-row in csv           

    # Show instruction
    mainText.setText(instructions[conid])
    mainText.draw()
    win.flip()
    event.waitKeys(keyList=ansKeys)

    # Loop through trials
    for trial in trialList:
        # Prepare each trial
        if training: 
            mainText.setText('TRAINING')                                                # Show "TRAINING" instead of prime in training condition
        
        # Prepare trial
        questionText.setText(questions[conid])                                      # Set text of question
        dotAngle = uniform(0,360)                                                   # Angle of dot in degrees
        dotDelayFrames = 0                                                          # When not 0, indicates that the last event has occurred and the number of frames since that event
        userError = False
        beepTime = trial['toneOnset']                  # Time of beep (0=unset, for non toneOnset conditions)
        
        # Calculate timeout time for this trial if timeOut condition
        timeOutTime = None
        if timeOut:
            # Adaptive scaling based on response ratio vs target timeOutRatio
            if timeOutCounter > 0 and len(timeOutMeanList) >= 3:  # Need at least 3 trials for reliable adaptation
                # Calculate current ratio of responses before timeout
                current_ratio = sum(timeOutMeanList) / len(timeOutMeanList)
                ratio_difference = current_ratio - timeOutRatio
                
                # Adapt timeout based on ratio difference
                if ratio_difference > 0.1:  # Too many responses before timeout (ratio too high)
                    timeOutScale *= uniform(*timeOutScaleDown)  # Decrease timeout to make it harder
                    scaling_direction = "DOWN"
                elif ratio_difference < -0.1:  # Too few responses before timeout (ratio too low)
                    timeOutScale *= uniform(*timeOutScaleUp)  # Increase timeout to make it easier
                    scaling_direction = "UP"
                else:
                    scaling_direction = "STABLE"
                print(f'Current ratio: {current_ratio:.3f}, Target: {timeOutRatio}, Diff: {ratio_difference:.3f}, Scale: {scaling_direction}')
            
            # Random timeout between 2-8 seconds with adaptive scaling
            base_timeout = uniform(timeOutWinBase[0], timeOutWinBase[1])
            timeOutTime = base_timeout * timeOutScale
            print(f'Base timeout: {base_timeout:.2f}s, Scale factor: {timeOutScale:.3f}, Final timeout: {timeOutTime:.2f}s')

        # Show rotating dot and handle events
        event.clearEvents()
        trialClock.reset()
        timeOutLogic = False
        trialCounter = trialCounter + 1
        
        if letterMode:
            letterShifted = False
            letterCounter = 0
            letterBlock = makeLetterList(nletters, nfwdValues)
            letterClock.reset()

        # Send start trigger
        trigger(startTrigger)

        # Run trial
        while True:
            dotAngle += dotStep
            if dotAngle > 360:
                dotAngle -= 360
            circle.draw()
            
            if letterMode:
                if letterClock.getTime() > letterDisplayTime:
                    letterCounter = letterCounter + 1
                    letterShifted = True
                    letterClock.reset()
                elif letterCounter >= len(letterBlock)-1:
                    letterCounter = 0
                    pass
                if letterShifted == True:
                    blankSpace.draw()
                    if letterClock.getTime() > letterSpaceTime:
                        letterClock.reset()
                        letterShifted = False
                else:
                    letterStim.setText(letterBlock[letterCounter])
                    letterStim.draw()
            else:
                fixation.draw()
            drawDot(dotAngle, timeOutLogic)
            win.flip()
            
            # Record press
            response = event.getKeys(keyList=leftKeys+rightKeys+ansKeys+quitKeys, timeStamped=trialClock)
            if len(response) and not trial['pressOnset']:       # Only react on first response to this trial
                if response[-1][0] in quitKeys: core.quit()     # Escape
                trial['pressOnset'] = int((response[-1][1])*msScale)/msScale
                trial['pressAngle'] = int((dotAngle-dotStep)*degScale)/degScale
                    
                # Left/right trigger based on response
                if response[-1][0] in leftKeys:
                    trigger(leftTrigger)
                    trial['response'] = rightTrigger
                elif response[-1][0] in rightKeys:
                    trigger(leftTrigger)
                    trial['response'] = rightTrigger
                elif response[-1][0] in ansKeys:
                    trigger(commonTrigger)
                    trial['response'] = commonTrigger
                
                if not get_press:
                    print('Error') # make some feedback not to press if not supposd to press
                    trial['userError'] = True
                    userError = True
                    
                if play_tone:
                    beepTime = trial['pressOnset']+toneDelay   # Set time for beep
                else:
                    dotDelayFrames = 1   # Mark as last event
                
                if letterMode:
                    trial['nFwd'] = 'NaN'  # Default value
                    for nfwd in nfwdValues:
                        if letterCounter >= nfwd and letterBlock[letterCounter] == letterBlock[letterCounter - nfwd]:
                            trial['nFwd'] = nfwd
                            break  # Stop at first match
                    trial['stopCharacter'] = letterBlock[letterCounter]

            if userError:
                break
            
            # Check for timeout interruption
            if timeOutTime and trialClock.getTime() > timeOutTime and not trial['pressOnset']:
                # Random interruption occurred before any response
                timeOutLogic = True
                trial['timeOut'] = True
                trial['timeOutOnset'] = int(trialClock.getTime() * msScale) / msScale
                # trial['timeOutAngle'] = int(dotAngle * degScale) / degScale

            # Play beep when time is up and mark as last event
            if beepTime and trialClock.getTime() > beepTime:
                beep.play()
                trial['toneOnset'] = int((trialClock.getTime())*msScale)/msScale
                trial['toneAngle'] = int((dotAngle)*degScale)/degScale
                beepTime = 0
                dotDelayFrames = 1

            # The little time after last event, where the dot keeps rotating.
            if dotDelayFrames:
                if dotDelayFrames > trial['dotDelay']: 
                    break
                dotDelayFrames += 1

        if userError:
            mainText.setText('Error. Do not press the key this round.\n(Press key to continue)')                                      # !!!!!! Set text
            mainText.draw()
            win.flip()
            event.waitKeys() 
        else:
            # Report clock time of event
            dotAngle = uniform(0,360)
            trialClock.reset()
            while True:
                circle.draw()
                questionText.draw()
                visual.TextStim(win, text='+', color='white', height=textSize, antialias=False).draw()
                drawDot(dotAngle, timeOutLogic)
                win.flip()

                # Handle responses: quit, move or answer
                response = event.waitKeys(keyList=list(moveKeys.keys())+ansKeys+quitKeys+errorKeys) #             response = event.waitKeys(moveKeys.keys()+ansKeys+quitKeys)
                if response[-1] in quitKeys: core.quit()
                if response[-1] in moveKeys: 
                    dotAngle += moveKeys[response[-1]]
                    if dotAngle > 360: 
                        dotAngle = dotAngle-360
                    if dotAngle < 0: 
                        dotAngle = 360+dotAngle
                if response[-1] in ansKeys:
                    trial['ansTime'] = int((trialClock.getTime())*msScale)/msScale
                    trial['ansAngle'] = int((dotAngle)*degScale)/degScale
                    break
                if response[-1] in errorKeys:
                    trial['userError'] = True
                    break

        # Update timeout statistics for adaptive scaling
        if timeOut:  # Only track for timeout conditions
            if len(timeOutMeanList) >= averageVectorSize:
                timeOutMeanList.pop(0)  # Remove oldest
            if trial['pressOnset'] and timeOutTime and trial['pressOnset'] < timeOutTime:
                # Response occurred before timeout
                timeOutMeanList.append(1)
                trial['timeOut'] = False
            else:
                # No response or response after timeout
                timeOutMeanList.append(0)
                if timeOutLogic:
                    trial['timeOut'] = True
                    timeOutCounter += 1
        
        # Additional question. Only for W-press and M-press conditions.
        if conid in ['W-press','M-press']:
            waitTimeBeforeNextTrial = 0.75
            questionText.setText('Press (Y) to continue \n\n (F) if error in last trial')                                      # !!!!!! Set text of question text !!!!!!!
            questionText.draw()
            win.flip()
            
            while True:
                # Handle responses: quit, move or answer
                response = event.waitKeys(keyList=timeOutKeys+errorKeys+quitKeys) #                response = event.waitKeys(timeOutKeys+errorKeys+quitKeys)
                if response[-1] in quitKeys: core.quit()
                if response[-1] in timeOutKeys: 
                    trial['timeOutQuestion'] = response[-1]
                    trial['userError'] = False
                    break
                if response[-1] in errorKeys:
                    trial['timeOutQuestion'] = 'NA'
                    trial['userError'] = True
                    break

            # Set baseline libet clock for 0.75 seconds
            circle.draw()
            visual.TextStim(win, text='+', color='white', height=textSize, antialias=False).draw()
            win.flip()
            core.wait(waitTimeBeforeNextTrial)

        # End of trial: save by appending data to csv. If training: stop after trainingTrials trials
        if not training: 
            csvWriter([trial[category] for category in dataCategories])
        else: 
            if trial['no'] >= trainingTrials: return

def trainingIsOver():
    questionText.setText('Training is over \n\nGet ready...')                                      # !!!!!! Set text
    questionText.draw()
    win.flip()
    event.waitKeys()

def ThankYou():
    questionText.setText('This part of the experiment is over now \n\nThank You... :)')                                      # !!!!!! Set text
    questionText.draw()
    win.flip()
    event.waitKeys() #    event.waitKeys(ansKeys)

#--------------- RUN EXPERIMENT ------------------
#-------------------------------------------------
# Make random order of conditions and run experiment
conditions = [x + str(y+1) for x in condition_keys for y in range(blockRepetitions)]
shuffle(conditions)
conditionsT = [x + str(y+1) for x in trainingCondition_keys for y in range(trainingBlockRepetitions)]

# Run the experiment
for condition in conditionsT:
    runBlock(condition, training=True, letterMode=letterMode)
trainingIsOver()
for condition in conditions: 
    runBlock(condition, training=False, letterMode=letterMode)
ThankYou()
core.quit()