#!/usr/bin/env python3

# Stripped-down version of my Snake game, meant for use with a neural network! (more numpy)
# This version is not meant to be played by a human, I hope to try to train an AI to play it.
# Copyright (C) 2022  Nik Stromberg - nikorasu85@gmail.com

import random as rnd, numpy as np

COLS, ROWS = 20, 20

class Snake:
    def __init__(self):
        self.pos = np.array([COLS//2-1, ROWS//2-1], int) # start position
        self.dir = np.array(rnd.choice([(0,-1),(0,1),(-1,0),(1,0)]), int) # random direction
        self.segments = np.array([self.pos], int) # array of previous positions
        self.len = 3 # starting length of snake
        self.food = np.array([rnd.randint(0,COLS-1),rnd.randint(0,ROWS-1)], int) # random food position
        self.state = np.zeros((ROWS,COLS), int)
        self.state[self.food[1], self.food[0]] = 2
        self.state[self.segments[:,1], self.segments[:,0]] = 1
        self.gameover = False
    def update(self, newdir=None):
        if newdir and np.all(newdir != -self.dir): # if new direction is not opposite of current direction
            self.dir = np.array(newdir, int) # update direction
        hitself = np.all(self.pos + self.dir == self.segments[1:], axis=1).any()
        if np.any(self.pos + self.dir < 0) or np.any(self.pos + self.dir >= [COLS, ROWS]) or hitself:
            self.gameover = True; return # if snake hits border or itself, game over
        self.pos += self.dir # update position
        self.segments = np.concatenate([[self.pos], self.segments[:self.len-1]]) # add new position to segments
        if np.all(self.pos == self.food): # if snake eats food
            self.len += 1 # increase length of snake
            field = np.array(np.meshgrid(np.arange(COLS), np.arange(ROWS))).T.reshape(-1, 2)
            field = np.array([p for p in field if not np.any(np.all(p == self.segments, axis=1))])
            self.food = field[np.random.choice(len(field))] # random food position that is not on snake
        self.state[:] = 0 # reset state
        self.state[self.food[1], self.food[0]] = 2 # update food position
        self.state[self.segments[:,1], self.segments[:,0]] = 1 # update snake positions
        return self.state

def main():
    try:
        import time
        print('\x1b[2J\x1b[H\x1b]0;Snake',end='\a',flush=True)
        player = Snake()
        print(player.state)
        directions = {'w':(0,-1),'s':(0,1),'a':(-1,0),'d':(1,0)} # key directions
        while (action:=input()) != 'q': # will need to be changed to AI input later
            start = time.perf_counter()
            print('\x1b[0m\x1b[2J\x1b[H',end='',flush=True) # clear screen
            player.update(directions.get(action)) # update player with the direction of key pressed
            print(player.state)
            end = time.perf_counter()
            howlong = end - start
            print(howlong)
            if player.gameover: break # if game over, break out of loop
    except KeyboardInterrupt: pass # catch Ctrl+C
    finally: print(f'\x1b[0mGame Over! Score: {(player.len-3)}') # reset terminal, show cursor, print score

if __name__ == '__main__':
    main() # by Nik