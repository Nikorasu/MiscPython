#!/usr/bin/env python3

# Stripped-down version of my Snake game, meant for use with a neural network!
# This version is not meant to be played by a human, I hope to try to train an AI to play it.
# Copyright (C) 2022  Nik Stromberg - nikorasu85@gmail.com

import random as rnd, numpy as np, time

COLS, ROWS = 20, 20

class Snake:
    def __init__(self):
        self.pos = [COLS//2-1, ROWS//2-1] # start position
        self.dir = rnd.choice([(0,-1),(0,1),(-1,0),(1,0)]) # random direction
        self.segments = [self.pos] # list of previous positions
        self.len = 3 # starting length of snake
        self.food = [rnd.randint(0,COLS-1),rnd.randint(0,ROWS-1)] # random food position
        self.gameover = False
    def update(self,newdir=None):
        if newdir and newdir != (-self.dir[0],-self.dir[1]): # if new direction is not opposite of current direction
            self.dir = newdir # update direction
        hitself = [self.pos[0]+self.dir[0],self.pos[1]+self.dir[1]] in self.segments[1:]
        if self.pos[0]+self.dir[0] in (-1,COLS) or self.pos[1]+self.dir[1] in (-1,ROWS) or hitself:
            self.gameover = True; return # if snake hits border or itself, game over
        self.pos[0] += self.dir[0]; self.pos[1] += self.dir[1] # update position
        self.segments.insert(0,self.pos[:]) # add new position to segments
        self.segments = self.segments[:self.len] # remove segments that are too long
        if self.pos == self.food: # if snake eats food
            self.len += 1 # increase length of snake
            field = {(x,y) for x in range(0,COLS-1) for y in range(0,ROWS-1)} # create a set of all possible positions
            field = list(filter(lambda x: x not in self.segments, field)) # remove positions that are part of the snake
            self.food = list(rnd.choice(field)) # pick a random position from the remaining positions

        gameOutput = np.zeros((ROWS,COLS),int)
        gameOutput[self.food[1],self.food[0]] = 2
        for x, y in self.segments:
            gameOutput[y,x] = 1
        print(gameOutput)

def main():
    try:
        print('\x1b[2J\x1b[?25l\x1b[H\x1b]0;Snake',end='\a',flush=True)
        player = Snake()
        player.update()
        directions = {'w':(0,-1),'s':(0,1),'a':(-1,0),'d':(1,0)} # key directions
        while (action:=input()) != 'q': # will need to be changed to AI input later
            start = time.perf_counter()
            print('\x1b[0m\x1b[2J\x1b[H',end='',flush=True) # clear screen
            player.update(directions.get(action)) # update player with the direction of key pressed
            if player.gameover: break # if game over, break out of loop
            # later a time.sleep() will be added here to slow down the game
            end = time.perf_counter()
            howlong = end - start
            print(howlong)
    except KeyboardInterrupt: pass # catch Ctrl+C
    finally: print(f'\x1b[0m\x1b[2J\x1b[?25h\x1b[HGame Over! Score: {(player.len-3)}') # reset terminal, show cursor, print score

if __name__ == '__main__':
    main() # by Nik
