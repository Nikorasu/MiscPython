#!/usr/bin/env python3

# A basic Matrix code-rain terminal animation, with fade effect.
# by Nik Stromberg - nikorasu85@gmail.com - MIT 2023

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
            for i in range(len(self.characters)):
                if self.start-i-1 > 0:
                    brightness = 255-int(255*((i+1)/self.end)**2) if i+1 < self.end else 0
                    print(f'\x1b[0m\x1B[38;2;0;{brightness};0m\x1b[{self.start-i-1};{self.column}H{self.characters[i]}',end='\b',flush=True)
            self.characters.insert(0,random.choice(['','','\x1b[1m','\x1b[2m'])+newchar)
            if self.speed == 2: # if double speed
                addchar = random.choice(string.printable.strip())
                self.characters.insert(1,addchar)
            self.characters = self.characters[:self.end]
            self.characters.extend([' ',' ']) # add 2 blank spaces to end of list to clear old characters off screen
        self.start += self.speed 
        if self.start-len(self.characters) > termH: self.done = True # if end is off screen

chains = []
unused = set(range(1,os.get_terminal_size().columns)) # set of unused columns
print('\x1b[2J\x1b[?25l') # clear screen and hide cursor

while 1: # main loop
    termW = os.get_terminal_size().columns
    for i in range(int(termW*.85)-len(chains)): # fill 85% of the terminal width with MatrixColumns
        column = random.choice(list(unused)) # pick a random unused column
        #while (column := random.randint(1,termW)) in taken: pass # ensures no overlappping columns (inefficient)
        chains.append(MatrixColumn(column)) # spawn MatrixColumn at unused column, add to list for updating
        unused.remove(column) # remove column from unused set  old:taken.add(column)
    for mcol in chains:
        mcol.update()
        if mcol.done: # remove MatrixColumns when they finish falling
            unused.add(mcol.column) # add now unused column back to unused set  old:taken.remove(mcol.column)
            chains.remove(mcol)
    time.sleep(.08)
