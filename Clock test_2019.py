'''
Created on 06/08/2012. @author: Nygaard, MCV.

'''
#---------------- MISC -----------------
#---------------------------------------
from __future__ import division
from psychopy import core, visual, sound, event, gui, monitors #parallel
from math import sin, cos, radians
from numpy import average
from random import shuffle, randint, uniform
import os, csv
try:
    import winsound     # NB. There is known errors in timing using winsound (i.e. do not use)
    import thread
    windows = True
except ImportError:
    windows = False    

#---------------- VARS -----------------
#-----------------------------------------
# Trial and data options
trainingTrials = 1          # Number of initial training-trials per block
BlockTrials = 5             # Number of trials per block
toneOnset = [1.5, 7]        # [earliest, latest] onset range of tone in singleTone condition (in seconds)
toneDelay = 0               # Delay of tone (in seconds) relative to response after response (in seconds)
dotDelay = [36, 60]         # [earliest, latest] duration of dot, after last event (in frames)

# Display options
monDistance = 70            # Distance from subject eyes to monitor (in cm)
monWidth = 30               # Width of monitor display (in cm)
textSize = 0.8              # Size of text in degrees
circleRadius = 2            # Radius of circle (in degrees)
dotSize = circleRadius/10   # Size of dot (in degrees)
libetTime = 2.56            # Rotation speed of dot
dotStep = 360/libetTime/60  # Degrees shift per monitor-frame: 360/LibetTime/framerate
tics = 12                   # Number of tics on circle

# Sound
beepHz = 1000               # Frequency of sound
beepDuration = 0.1          # Duration (in seconds)

# Approximations
msScale = 1000
degScale = 10

# Time out parameters
#timeOutDistrubution = 0.5
#averageVectorSize = 3
#timeOutMeanList = range(averageVectorSize)
#timeOutScaleDown = [2, 5]
#timeOutScaleUp = [15,30]

# Questions, responses and primes
instructions = {
    'W-press':'\n\nW-press\n\nInstruction:\n\nPress as soon as you experience the intention to do so.\n\nSelect where the dot was when you experienced the first intention to press.',
    'M-press':'\n\nM-press\n\nInstruction:\n\nPress as soon as you experience the intention to do so.\n\nSelect where the dot was when you pressed.'
}

questions = {
    'W-press':'Where was the dot when you experienced the first intention to press?',
    'M-press':'Where was the dot when you pressed?'
}

moveKeys = {
    'left': -20,
    'up':1,
    'down': -1,
    'right': 20
}

errorKeys = ['f','num_subtract']
ansKeys = ['space','insert','return']
timeOutKeys = ['y','n','num_add']
quitKeys = ['q','esc','escape']

#letters = ['b','c','d','f','g','h','j','k','n','p','r','s','t','v','w','x','z']

# Data containers for each trial
dataCategories = ['id','condition','no','dotDelay','toneOnset','toneAngle','pressOnset','pressAngle','ansAngle','ansTime','timeOut','timeOutOnset','timeOutQuestion','stopCharacter','samplesToLastIdenticalCharacter','userError']
dataDict = dict(zip(dataCategories,['' for i in dataCategories]))

# Set monitor variables
myMon = monitors.Monitor('testMonitor')
myMon.setDistance(monDistance)
myMon.setWidth(monWidth)

# Intro dialogue
dialogue = gui.Dlg()
dialogue.addField('subjectID')
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
letterClock = core.Clock()
soundClock = core.Clock()
TimeOutClock = core.Clock()

#-------------- STIMULI ----------------
#---------------------------------------
win = visual.Window(monitor=myMon, size=myMon.getSizePix(), fullscr=True, allowGUI=False, color='black', units='deg')                               # Change fullscreen here: " fullscr=True/False "
mainText = visual.TextStim(win=win, height=textSize, color='white')
questionText = visual.TextStim(win=win, pos=(0, circleRadius*2), height=textSize, color='white')
clockDot = visual.PatchStim(win=win, mask="circle", color='#0000FF', tex=None, size=dotSize)
clockDotTimeOut = visual.PatchStim(win=win, mask="circle", color='#FF0000', tex=None, size=dotSize)
beep = sound.Sound(value=beepHz, secs=0.1)

# Make complex figure: circle + tics + fixation cross. Render and save as single stimulus "circle"
visual.Circle(win, radius=circleRadius, edges=512, lineWidth=3, lineColor='white').draw()
for angleDeg in range(0,360,int(360/tics)):
    angleRad = radians(angleDeg)
    begin = [circleRadius*sin(angleRad), circleRadius*cos(angleRad)]
    end = [begin[0]*1.1, begin[1]*1.1]
    visual.Line(win, start=(begin[0],begin[1]), end=(end[0],end[1]), lineColor='white', lineWidth=3).draw()

circle = visual.BufferImageStim(win)                                                    # Buffer it all in "circle" object
win.clearBuffer()

#------------- FUNCTIONS ---------------
#---------------------------------------
# Make a trigger fun (uncomment if computer does not have parallel port)
#def trigger(signal):
#    parallel.setData(signal)
#    core.wait(0.020,0.01)
#    parallel.setData(0)

# Make a list of trials (dictionaries) given a condition
def makeBlock(condition,training):
    if training == True:
        conditionRep = trainingTrials                                                               # Set number of training repetitions? 
    else:
        conditionRep = BlockTrials                                                               # Set number of repetitions? 
        
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

#        if condition is 'singleTone': 
#            trialList[trialNo]['toneOnset'] = uniform(toneOnset[0], toneOnset[1])

    return trialList


# Draws a dot on the circle, given an angle
def drawDot(angleDeg,timeOut):
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

def windowsBeep():
    lock = thread.allocate_lock()
    lock.acquire()                                                                      # Entering critical section
    winsound.Beep(beepHz, int(beepDuration*msScale))
    lock.release()                                                                      # Exiting critical section

# Run a block of trials and save results
def runBlock(condition, training, letterMode):
    trialList = makeBlock(condition,training)
    
    # Letter mode
#    letterListLength = 6
#    randomLetterListSetPoint = randint(0,len(letters)-letterListLength-1)
#    letterBlock = letters[randomLetterListSetPoint:randomLetterListSetPoint+letterListLength]
#    letterCounter = 0
#    letterOffsetMinimum = 2
#    letterOffsetMaximum = letterListLength/2
#    letterInterval = len(letterBlock)-letterOffsetMinimum
#    letterList = range(len(letterBlock))
#    shuffle(letterList)
#    letterListOld = letterList

    # Time out
#    timeOutLogic = False
#    timeOutCounter = 0
#    timeOutListCounter = 0
#    timeOutMeanListAverage = 1
    trialCounter = 0
#    timeOutScale = 1
    triggerList = [1]           # Trigger codes to send to parallel port


    # Set up .csv save function
    if not training:
        saveFile = saveFolder+'/subject_' +str(subjectID)+'_'+condition+'.csv'          # Filename for save-data
        csvWriter = csv.writer(open(saveFile, 'w'), delimiter=';').writerow            # The writer function to csv
        csvWriter(dataCategories)                                                       # Writes title-row in csv           

    # Show instruction
    mainText.setText(instructions[condition])
    mainText.draw()
    win.flip()
    event.waitKeys() #    event.waitKeys(ansKeys)


    # Loop through trials
    for trial in trialList:
        # Prepare each trial
        if training: 
            mainText.setText('TRAINING')                                                # Show "TRAINING" instead of prime in training condition
        
        questionText.setText(questions[condition])                                      # Set text of question
        dotAngle = uniform(0,360)                                                       # Angle of dot in degrees
        dotDelayFrames = 0                                                              # When not 0, indicates that the last event has occurred and the number of frames since that event

#        beepTime = trial['toneOnset']                                                   # Time of beep (0=unset, for non toneOnset conditions)

        # Show rotating dot and handle events
        event.clearEvents()
        trialClock.reset()
        letterClock.reset()
        TimeOutClock.reset()
        timeOutLogic = False
        trialCounter = trialCounter + 1

        while True:
            dotAngle += dotStep
            if dotAngle > 360:
                dotAngle -= 360
            circle.draw()
            visual.TextStim(win, text='+', color='white', height=textSize, antialias=False).draw()
            drawDot(dotAngle,timeOutLogic)
            win.flip()

            # Record press
            if condition in ['W-press','M-press','W-press1','M-press1']:

                # Log event
                response = event.getKeys(keyList=ansKeys+quitKeys, timeStamped=trialClock)
                if len(response) and not trial['pressOnset']:       # Only react on first response to this trial
                    if response[-1][0] in quitKeys: core.quit()
                    trial['pressOnset'] = int((response[-1][1])*msScale)/msScale
                    trial['pressAngle'] = int((dotAngle-dotStep)*degScale)/degScale

#                    trigger(triggerList[0])                            # Parllel trigger
#                    beep.play()                                        # Sound trigger

                    trial['toneOnset'] = int((trialClock.getTime())*msScale)/msScale
                    trial['toneAngle'] = int((dotAngle)*degScale)/degScale

#                    for wordInList in range(len(letterList)):
#                        if letterBlock[letterList[letterCounter]] == letterBlock[letterListOld[wordInList]]:
#                            wordInListNumberOfDifferentCharactersBetween = (len(letterList)-wordInList) + letterCounter - 1
                    #print wordInListMemo
                    #print letterCounter
#                    trial['stopCharacter'] = letterBlock[letterList[letterCounter]]
#                    trial['samplesToLastIdenticalCharacter'] = wordInListNumberOfDifferentCharactersBetween

                    if condition in ['W-press','M-press','W-press1','M-press1']: #or 'singlePressTimeOut': 
                        dotDelayFrames = 1   # Mark as last event

            # Play beep when time is up and mark as last event
#            if beepTime and trialClock.getTime() > beepTime:

#                # Play differently on windows and mac/linux

#                if windows: 
#                    thread.start_new_thread(windowsBeep,())
#                else: 
#                    beep.play()
#                trial['toneOnset'] = int((trialClock.getTime())*msScale)/msScale
#                trial['toneAngle'] = int((dotAngle)*degScale)/degScale
#                beepTime = 0
#                dotDelayFrames = 1

            # The little time after last event, where the dot keeps rotating.
            if dotDelayFrames:
                TimeOutClock.reset()
#                if trial['timeOut'] == 'yes':
#                    timeOutLogic = True
#                else:
#                    timeOutLogic = False

                if dotDelayFrames > trial['dotDelay']: 
                    break
                dotDelayFrames += 1

                

        # Subjects selects location of target event
        dotAngle = uniform(0,360)
        trialClock.reset()
        while True:
            circle.draw()
            questionText.draw()
            visual.TextStim(win, text='+', color='white', height=textSize, antialias=False).draw()

            if trial['timeOut'] == 'yes':
                drawDot(dotAngle,True)
            else:
                drawDot(dotAngle,False)
            win.flip()

            # Handle responses: quit, move or answer
            response = event.waitKeys() #             response = event.waitKeys(moveKeys.keys()+ansKeys+quitKeys)
            print(response)
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

        # Additional question    
        if condition in ['W-press','M-press','W-press1','M-press1']:
            waitTimeBeforeNextTrial = 0.75
            questionText.setText('Press (Y) to continue \n\n (F) if error in last trial')                                      # !!!!!! Set text of question text !!!!!!!
            questionText.draw()
            win.flip()

            while True:
                # Handle responses: quit, move or answer
                response = event.waitKeys() #                response = event.waitKeys(timeOutKeys+errorKeys+quitKeys)

#                print('response: '+response)
                if response[-1] in quitKeys: 
                    core.quit()
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


#---------- RUN EXPERIMENT -------------
#---------------------------------------
# Make random order of conditions and run experiment
conditions = ['W-press','M-press']
shuffle(conditions)
conditionsT = ['M-press','W-press']

# Real experiment

#for condition in conditionsT:
#    runBlock(condition, training=True, letterMode=False)
trainingIsOver()
for condition in conditions: 
    runBlock(condition, training=False, letterMode=False)
ThankYou()
core.quit()