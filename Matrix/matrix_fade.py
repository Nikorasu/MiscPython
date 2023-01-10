#!/usr/bin/env python3

# A basic Matrix code-rain terminal animation, with fade effect.
# by Nik Stromberg - nikorasu85@gmail.com - MIT 2022

DENSITY = 0.80 # percentage of terminal width to fill (default 0.80)
MOVERATE = 0.08 # seconds between updates (default 0.08) lower is faster

import random, os, string, time

class MatrixColumn:
    def __init__(self, column):
        self.column = column
        self.start = -random.randint(0,os.get_terminal_size().lines) # random start position
        self.end = random.randint(5,os.get_terminal_size().lines) # random end length
        self.speed = random.choice([1,1,2]) # 1/3 chance of double speed
        self.characters = random.choices(string.printable.strip(),k=self.end)
        self.done = False
    def update(self):
        termH = os.get_terminal_size().lines # get terminal height
        if 0 < self.start <= termH+len(self.characters): # if start is on screen
            newchar = random.choice(string.printable.strip())
            print(f'\x1b[0m\x1b[97m\x1b[{self.start};{self.column}H{newchar}',end='\b',flush=True)
            for i, char in enumerate(self.characters): # loop through all characters
                if self.start-i-1 > 0: # if characters are on screen
                    brightness = 255-int(255*((i+1)/self.end)**2) if i+1 < self.end else 0
                    print(f'\x1b[0m\x1b[38;2;0;{brightness};0m\x1b[{self.start-i-1};{self.column}H{char}',end='\b',flush=True)
            self.characters.insert(0,random.choice(['','','\x1b[1m','\x1b[2m'])+newchar)
            if self.speed == 2: # if double speed
                addchar = random.choice(string.printable.strip()) # add an additional character
                self.characters.insert(1,random.choice(['','','\x1b[1m','\x1b[2m'])+addchar)
            self.characters = self.characters[:self.end]
            self.characters.extend([' ',' ']) # add 2 blank spaces to end of list to clear old characters off screen
        self.start += self.speed 
        if self.start-len(self.characters) > termH: self.done = True # if end is off screen

chains = []
taken = set()
unused = set(range(1,os.get_terminal_size().columns)) # set of unused columns
print('\x1b[2J\x1b[?25l') # clear screen and hide cursor
try:
    while 1: # main loop
        FullCols = set(range(1,termW := os.get_terminal_size().columns)) # set of all columns, & store terminal width
        if unused.union(taken) != FullCols: unused = FullCols - taken # accounts for terminal resizing
        for i in range(int(termW*DENSITY)-len(chains)): # fill Density% of the terminal width with MatrixColumns
            column = random.choice(list(unused)) # pick a random unused column
            chains.append(MatrixColumn(column)) # create a new MatrixColumn in that column
            taken.add(column) # add column to taken set
            unused.remove(column) # remove column from unused set
        for mcol in chains: # loop through all MatrixColumns
            mcol.update() # run update function in each MatrixColumn
            if mcol.done: # remove MatrixColumns when they finish falling
                taken.remove(mcol.column) # remove column from taken set
                if mcol.column <= termW: unused.add(mcol.column) # add now unused column back to unused set
                chains.remove(mcol) # remove finished MatrixColumn from list
        time.sleep(MOVERATE) # controls the speed of the animation
except KeyboardInterrupt: print('\x1b[2J\x1b[0m\x1b[?25h') # reset terminal and show cursor on ctrl+c