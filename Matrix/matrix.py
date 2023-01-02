#!/usr/bin/env python3

# Matrix code-rain terminal animation
# by Nik Stromberg - nikorasu85@gmail.com - MIT 2022 - copilot

import random, os, string, time

color = ['\x1b[32m','\x1b[92m'] # green
highlight = '\x1b[97m' # white

class MatrixColumn:
    def __init__(self, column):
        self.column = column
        self.termH = os.get_terminal_size().lines # get terminal height
        self.start = -random.randint(0,self.termH) #self.start = 0 #self.end = -random.randint(3,self.termH)
        self.end = self.start - random.randint(3,self.termH) #-random.randint(-self.start, self.termH)
        self.speed = random.choice([1,1,2])
        self.prechar = ''
        self.fastchar = ''
        self.done = False
    def update(self):
        character = random.choice(string.printable.strip())
        if 0 < self.start <= self.termH+2:
            print(f'{highlight}\x1b[{self.start};{self.column}H{character}',end='\b',flush=True)
            print(f'{random.choice(color)}\x1b[{self.start-1};{self.column}H{self.prechar}',end='\b',flush=True)
            if self.speed == 2:
                print(f'{random.choice(color)}\x1b[{self.start-2};{self.column}H{self.fastchar}',end='\b',flush=True)
        if self.termH >= self.end > -1:
            print(f'\x1b[{self.end};{self.column}H ',end='\b',flush=True)
            if self.speed == 2:
                print(f'\x1b[{self.end+1};{self.column}H ',end='\b',flush=True)
        self.start += self.speed
        self.end += self.speed
        self.fastchar = self.prechar
        self.prechar = character
        if self.end > self.termH: self.done = True

print('\x1b[2J') # clear screen
chains = []
taken = set()
termW = os.get_terminal_size().columns
for i in range(int(termW*.7)):
    while (column := random.randint(1,termW)) in taken: pass
    taken.add(column)
    chains.append(MatrixColumn(column))

while 1:
    for mcol in chains:
        mcol.update()
        if mcol.done:
            taken.remove(mcol.column)
            chains.remove(mcol)
            termW = os.get_terminal_size().columns
            while (column := random.randint(1,termW)) in taken: pass
            taken.add(column)
            chains.append(MatrixColumn(column))
    time.sleep(0.1)
