"""
Utility functions for the clock experiment.
Includes a function to make a pseudo-random letter list for the letter-memory task.

"""
from random import shuffle, choice
from collections import Counter

letters = ['b','c','d','g','h','k','m','n','p','r','s','t','v','w','x','z']

# Make pseudo-random letter mode.
def makeLetterList(nletters, repValues, letters=letters):
    nfwdValues = list(repValues)
    letterBlock = [0]*nletters
    nfwdList = [0]*len(letterBlock)
    for ii in range(nletters):
        shuffle(letters)
        temp_nfwdValues = list(repValues)
#        print temp_nfwdValues, nfwdValues, repValues
        if nfwdList[ii-1] == max(temp_nfwdValues):
            temp_nfwdValues[temp_nfwdValues.index(max(temp_nfwdValues))] = min(temp_nfwdValues)
        shuffle(temp_nfwdValues)
        if letterBlock[ii] == 0:
            currentLetter = letters[0]
            letters[letters.index(currentLetter)] = 0
            while currentLetter == 0:
                shuffle(letters)
                currentLetter = letters[0]
            if ii < len(letterBlock)-max(nfwdValues):
                for xx in range(len(temp_nfwdValues)):
                    nfwd = temp_nfwdValues[xx]
                    if letterBlock[ii+nfwd] == 0:
                        break
                letterBlock[ii] = currentLetter
                letterBlock[ii+nfwd] = currentLetter
                nfwdList[ii] = nfwd
            else:
                letterBlock[ii]=choice(letters)
        elif letterBlock[ii] != 0:
            currentLetter = letterBlock[ii]
            nfwd = temp_nfwdValues[0]
            if ii < len(letterBlock)-max(nfwdValues):
                for xx in range(len(temp_nfwdValues)):
                    nfwd = temp_nfwdValues[xx]
                    if letterBlock[ii+nfwd] == 0:
                        break
                letterBlock[ii+nfwd] = currentLetter
                nfwdList[ii] = nfwd
            else:
                letterBlock[ii]=choice(letters)
        temp_nfwdValues = repValues
    # print(zip(letterBlock, nfwdList))
    # print(Counter(nfwdList))
    return letterBlock

if __name__ == '__main__':
    ll = makeLetterList(30, [3,4,5])
    print(ll)
    print(list(set(ll)))

## CONDITION CONFIGURATION
CONDITION_CONFIG = {
    'W-press':        {'conid': 'W-press',        'get_press': True,  'play_tone': False, 'timeOut': False},
    'M-press':        {'conid': 'M-press',        'get_press': True,  'play_tone': False, 'timeOut': False},
    'singleTone':     {'conid': 'IB-singleTone',  'get_press': False, 'play_tone': True , 'timeOut': False},
    'IB-singlePress': {'conid': 'IB-singlePress', 'get_press': True,  'play_tone': False, 'timeOut': False},
    'IB-press':       {'conid': 'IB-press',       'get_press': True,  'play_tone': True , 'timeOut': False},
    'IB-tone':        {'conid': 'IB-tone',        'get_press': True,  'play_tone': True , 'timeOut': False},
    'W-interval':     {'conid': 'W-interval',     'get_press': True,  'play_tone': False, 'timeOut': False},
    'M-interval':     {'conid': 'M-interval',     'get_press': True,  'play_tone': False, 'timeOut': False},
    'interruption':   {'conid': 'interruption',   'get_press': True,  'play_tone': False, 'timeOut': True},
}

def get_condition_config(condition):
    for key, config in CONDITION_CONFIG.items():
        if key in condition:
            return config
    raise ValueError(f"Unknown condition: {condition}")