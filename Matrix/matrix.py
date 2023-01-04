#!/usr/bin/env python3

# A basic Matrix code-rain terminal animation.
# by Nik Stromberg - nikorasu85@gmail.com - MIT 2023

COLOR = ['\x1b[32m','\x1b[92m'] # green
HIGHLIGHT = '\x1b[97m' # white

import random, os, string, time

class MatrixColumn:
    def __init__(self, column):
        self.column = column
        self.start = -random.randint(0,os.get_terminal_size().lines) # random start position
        self.end = self.start-random.randint(3,os.get_terminal_size().lines) # random end position
        self.speed = random.choice([1,1,2]) # 1/3 chance of double speed
        self.prechar = ''
        self.done = False
    def update(self):
        termH = os.get_terminal_size().lines # get terminal height
        if 0 < self.start <= termH+2: # if start is on screen
            character = random.choice(string.printable.strip())
            print(f'{HIGHLIGHT}\x1b[{self.start};{self.column}H{character}',end='\b',flush=True)
            print(f'{random.choice(COLOR)}\x1b[{self.start-1};{self.column}H{self.prechar}',end='\b',flush=True)
            if self.speed == 2: # if double speed
                altchar = random.choice(string.printable.strip())
                print(f'{random.choice(COLOR)}\x1b[{self.start-1};{self.column}H{altchar}',end='\b',flush=True)
                print(f'{random.choice(COLOR)}\x1b[{self.start-2};{self.column}H{self.prechar}',end='\b',flush=True)
            if self.start <= termH: self.prechar = character
        if termH >= self.end > -1: # if end is on screen
            print(f'\x1b[{self.end};{self.column}H ',end='\b',flush=True)
            if self.speed == 2: print(f'\x1b[{self.end+1};{self.column}H ',end='\b',flush=True)
        self.start += self.speed 
        self.end += self.speed
        if self.end > termH: self.done = True # if end is off screen

chains = []
taken = set()
print('\x1b[2J\x1b[?25l') # clear screen and hide cursor

while 1: # main loop
    termW = os.get_terminal_size().columns
    for i in range(int(termW*.8)-len(chains)): # fill 80% of the terminal width with MatrixColumns
        while (column := random.randint(1,termW)) in taken: pass # ensures no overlappping columns
        chains.append(MatrixColumn(column)) # spawn MatrixColumn at open column, add to list for updating
        taken.add(column) # add column to taken set
    for mcol in chains:
        mcol.update()
        if mcol.done: # remove MatrixColumns when they finish falling
            taken.remove(mcol.column)
            chains.remove(mcol)
    time.sleep(.1)
