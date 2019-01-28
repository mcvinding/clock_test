from psychopy import visual, event
win = visual.Window([400,400])
key = event.waitKeys()
print(key)