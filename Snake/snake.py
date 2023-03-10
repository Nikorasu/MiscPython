#!/usr/bin/env python3

# This is a simple terminal-based Snake game!
# Copyright (C) 2022  Nik Stromberg - nikorasu85@gmail.com

import time, sys, os, random # for randomization, terminal size, timing
from colorsys import hsv_to_rgb # for converting colors from HSV to RGB
if os.name == 'nt': from msvcrt import kbhit, getch # for Windows keyboard input
else: import termios, tty, select # for Linux keyboard input

class NonBlockingInput:
    def __enter__(self):
        if os.name == 'posix': # if on Linux
            self.oldsettings = termios.tcgetattr(sys.stdin) # store old terminal settings
            tty.setcbreak(sys.stdin) # set terminal to cbreak mode (so input doesn't wait for enter)
        return self
    def __exit__(self,type,val,tb):
        if os.name == 'posix': termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.oldsettings) # restore terminal settings
    def keypress(self):
        if os.name == 'nt' and kbhit(): # for Windows
            if (ch := getch()) == b'\xe0': return {b"H":"\x1b[A",b"P":"\x1b[B",b"M":"\x1b[C",b"K":"\x1b[D"}[getch()]
            return ch.decode()
        elif os.name == 'posix' and sys.stdin in select.select([sys.stdin],[],[],0)[0]: # for Linux
            if (ch := sys.stdin.read(1)) == '\x1b': ch += sys.stdin.read(2) # if escape, read 2 more characters
            return ch
        return None

def cols(): return os.get_terminal_size().columns
def rows(): return os.get_terminal_size().lines

def border(score):
    print(f'\x1b[48;5;237m\x1b[H\{f"Score: {score}": ^{cols()}}\x1b[{rows()};H{"": ^{cols()}}',end='',flush=True) # top & bottom
    print('\x1b[48;5;237m\x1b[H'+(f'  \x1b[{cols()-1}G  \n'*rows())[:-1],end='\x1b[0m',flush=True) # left & right

class TheSnake:
    def __init__(self):
        self.color = tuple(int(x*255) for x in hsv_to_rgb(random.randint(20,320)/360,1,1)) # random color using HSV
        self.pos = [cols()//2, rows()//2] # start position
        self.dir = random.choice([(0,-1),(0,1),(-2,0),(2,0)]) # random direction
        self.segments = [self.pos] # list of previous positions
        self.len = 5 # starting length of snake
        self.food = [random.randint(3,cols()-3),random.randint(2,rows()-1)] # random food position
        self.gameover = False
    def update(self,newdir=None):
        if newdir and newdir != (-self.dir[0],-self.dir[1]): # if new direction is not opposite of current direction
            self.dir = newdir # update direction
        hitself = [self.pos[0]+self.dir[0],self.pos[1]+self.dir[1]] in self.segments[1:]
        if self.pos[0] in (1,2,cols()-1,cols()-2) or self.pos[1] in (1,rows()) or hitself:
            self.gameover = True; return # if snake hits border or itself, game over
        self.pos[0] += self.dir[0]; self.pos[1] += self.dir[1] # update position
        self.segments.insert(0,self.pos[:]) # add new position to segments
        self.segments = self.segments[:self.len] # remove segments that are too long
        if self.pos in (self.food,[self.food[0]+1,self.food[1]],[self.food[0]-1,self.food[1]]): # if snake is on food
            self.len += 5 # increase length of snake by 5
            field = {(x,y) for x in range(3,cols()-2) for y in range(2,rows())} # create a set of all possible positions
            field = list(filter(lambda x: x not in self.segments, field)) # remove positions that are part of the snake
            self.food = list(random.choice(field)) # pick a random position from the remaining positions
        # Draws the food, and segments of the snake
        print(f'\x1b[{self.food[1]};{self.food[0]}H\x1b[38;2;255;0;0m\u2588\u2588',end='',flush=True) # draw food
        for x, y in self.segments: # draw snake segments
            print(f'\x1b[{y};{x}H\x1b[38;2;{"{};{};{}".format(*self.color)}m\u2588\u2588',end='',flush=True)

def main():
    try:
        print('\x1b[2J\x1b[?25l\x1b]0;Snake',end='\a',flush=True)
        player = TheSnake()
        directions = {'\x1b[A':(0,-1),'\x1b[B':(0,1),'\x1b[D':(-2,0),'\x1b[C':(2,0),'w':(0,-1),'s':(0,1),'a':(-2,0),'d':(2,0)} # key directions
        with NonBlockingInput() as nbi: # enables non-blocking input
            while (key:=nbi.keypress()) not in ('q','\x1b\x1b\x1b'):# q or ESC quit (Esc x3 due to bug with detecting arrow keys)
                print('\x1b[0m\x1b[2J',end='',flush=True) # clear screen
                player.update(directions.get(key)) # update player with the direction of key pressed
                if player.gameover: break # if game over, break out of loop
                border((player.len-5)//5) # draw border
                time.sleep(.06) # seconds between updates & inputs (.06 seems to be a good balance)
    except KeyboardInterrupt: pass # catch Ctrl+C
    finally: print(f'\x1b[0m\x1b[2J\x1b[?25h\x1b[HGame Over! Score: {(player.len-5)//5}') # reset terminal, show cursor, print score

if __name__ == '__main__':
    main() # by Nik
