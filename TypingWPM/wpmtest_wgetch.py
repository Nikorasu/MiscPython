#!/usr/bin/env python3
import time, random
from getchlib import getkey

# A quick program to test the user's typing speed in the terminal by printing random pangrams,
# then overlapping user input over the same line as they type, green for correct red for incorrect,
# finally printing the user's WPM and accuracy. This version uses getchlib and supports arrows keys.
# by Nik Stromberg - nikorasu85@gmail.com - MIT 2022

with open('pangrams.txt') as f:
    pangrams = f.read().splitlines()
    #pangrams = f.readlines() #pangrams = [sentence.strip() for sentence in pangrams]

randPan = random.choice(pangrams) # pick a random pangram

print(randPan,end='\x0D') # print the pangram and move cursor to beginning of line

pos = 0
typedPan = ''
#done = False # not needed
while 1:
    keypress = getkey()
    if keypress in ('\x1b',chr(10)): break
    elif keypress == chr(127):
        pos -= 1
        typedPan = typedPan[:-1]
        print('\x1b[0m'+'\b'+randPan[pos]+'\b',end='',flush=True)

    if keypress.isalnum() or keypress in (' ',',','.',"'",'?','!','-','\x1b[C','\x1b[D'):
        if keypress == randPan[pos]: print('\x1b[32m'+keypress,end='',flush=True) # green
        else: print('\x1b[31m'+keypress,end='',flush=True) # red for incorrect
        
        # This is why ARROWS might be a bad idea, makes it hard to tell where the cursor is.
        if keypress == '\x1b[C':
            pos += 1
            typedPan += keypress
        elif keypress == '\x1b[D':
            pos -= 1
            typedPan = typedPan[:-1]
        #pos += -1 if keypress == '\x1b[D' else 1

print('\x1b[0m') # reset color