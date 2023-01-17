#!/usr/bin/env python3

# A quick program to test the user's typing speed in the terminal by printing random pangrams,
# and overlapping user input over the same line as they type, green for correct red for incorrect,
# then when they complete it, the program ends by printing the user's WPM and accuracy.
# Copyright (C) 2022 Nik Stromberg - nikorasu85@gmail.com

import tty, termios, sys, time, random
from difflib import SequenceMatcher

def getch(): # Gets keypresses from terminal, without requiring the user to press enter.
    old_settings = termios.tcgetattr(sys.stdin) # save current terminal settings
    tty.setraw(sys.stdin) # set terminal to raw mode, alt: #tty.setcbreak(fd) #fd=sys.stdin.fileno()
    ch = sys.stdin.read(1) # read a single character from the terminal
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings) # restore saved terminal settings
    return ch

with open('pangrams.txt') as f:
    pangrams = f.read().splitlines()

print('\x1b[96mBegin typing when ready..\x1b[0m')
randPan = random.choice(pangrams) # pick a random pangram
print(f'\x1b[97m{randPan}\x1b[0m',end='\x0D') # print the pangram and move cursor to beginning of line

startTime = pos = 0 # start time, position in pangram
typedPan = '' # user's typed pangram

while 1:
    if pos == 1 and startTime == 0: # start the timer when the user starts typing
        startTime = time.time()

    key = getch()
    if key in ('\x1b',chr(10),chr(13)) or pos == len(randPan): break # Esc, Enter, or reached end
    elif key == chr(127) and pos > 0: # backspace
        pos -= 1  # subtract 1 from position
        typedPan = typedPan[:-1] # remove last character from typedPan
        print(f'\x1b[97m\b{randPan[pos]}\b\x1b[0m',end='',flush=True)  #'\x1b[D'
    elif key.isalnum() or key in (' ',',','.',"'",'?','!','-'):  #pos < len(randPan)
        if key == randPan[pos]: print('\x1b[92m'+key,end='\x1b[0m',flush=True) # green
        else: print('\x1b[91m'+key,end='\x1b[0m',flush=True) # red for incorrect
        typedPan += key
        pos += 1 #len(key) # some terminals bug if pressing multiple keys at once

endTime = time.time()
timeElapsed = endTime - startTime
wpm = round((len(typedPan)/5)/(timeElapsed/60),1) # 5 characters per word on average
accuracy = round(SequenceMatcher(None,randPan,typedPan).ratio()*100,1)

if len(typedPan) > len(randPan)/2:
    print(f'\nWPM: {wpm}  Accuracy: ~{accuracy}%')
else:
    print('\nTyping incomplete..')
