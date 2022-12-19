#!/usr/bin/env python3

# A quick program to test the user's typing speed in the terminal by printing random pangrams,
# then overlapping user input over the same line as they type, green for correct red for incorrect,
# finally printing the user's WPM and accuracy. PORTABLE VERSION! No getchlib required.
# by Nik Stromberg - nikorasu85@gmail.com - MIT 2022 - copilot

print('\x1b[36mBegin typing when ready..\x1b[0m')

import tty, termios, sys, time, random
from difflib import SequenceMatcher

def getch(): # Gets a single character from the user, without requiring the user to press enter.
    old_settings = termios.tcgetattr(sys.stdin) # or sys.stdin.fileno()
    try:
        tty.setcbreak(sys.stdin) # disables buffer #alt tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings) # restore terminal settings
    return ch

with open('pangrams.txt') as f:
    pangrams = f.read().splitlines()

randPan = random.choice(pangrams) # pick a random pangram
print(randPan,end='\x0D') # print the pangram and move cursor to beginning of line

startTime = pos = 0
typedPan = ''

while 1:
    if pos == 1 and startTime == 0: # start the timer when the user starts typing
        startTime = time.time()

    keypress = getch()
    if keypress == chr(127) and pos > 0: # backspace
        pos -= 1
        typedPan = typedPan[:-1]
        print(f'\x1b[0m\b{randPan[pos]}\b',end='',flush=True)  #'\x1b[D'
    elif keypress in ('\x1b',chr(10)) or pos == len(randPan): break # Enter or Esc, or reached end

    if keypress.isalnum() or keypress in (' ',',','.',"'",'?','!','-'):  #pos < len(randPan) and (
        if keypress == randPan[pos]: print('\x1b[32m'+keypress,end='',flush=True) # green
        else: print('\x1b[31m'+keypress,end='',flush=True) # red for incorrect
        typedPan += keypress
        pos += len(keypress) # still has bug if 2 keys pressed at once

endTime = time.time()
print('\x1b[0m') # reset color

timeElapsed = endTime - startTime
wpm = round((len(typedPan)/5)/(timeElapsed/60),1) # 5 characters per word on average
accuracy = round(SequenceMatcher(None,randPan,typedPan).ratio()*100,1)

if len(typedPan) > len(randPan)-5:
    print(f'WPM: {str(wpm)}  Accuracy: ~{str(accuracy)}%')
else:
    print('Typing incomplete..')
