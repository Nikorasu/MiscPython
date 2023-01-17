#!/usr/bin/env python3

# Copyright (C) 2022 Nik Stromberg - nikorasu85@gmail.com

from time import strftime
import sounddevice as sd
import pygame as pg
import numpy as np

Width = 1920        # Window Width
Height = 900        # Window Height
upperfreq = 3500    # Highest frequency to display Hz
samplerate = 48000  # Sample Rate, 44100 or 48000 Hz
blocksize = 20      # ms, lower than 20 lags
dialate = 4         # Stretches out spectrum, multiples of 2, higher moves faster
strength = 250      # brightness, needs adjusting based on scale

OldRainbw = [0,0xFF0000,0xFF9900,0xCCFF00,0x33FF00,0x00FF66,0x00FFFF,0x0066FF,0x3300FF,0xCC00FF,0xFF0099]
BluePlsma = [0,0x3300FF,0x0066FF,0x00FFFF,0x00FF66,0x33FF00,0xCCFF00,0xFF9900,0xFF0000,0xCC00FF,0xFF0099]
BlueWhite = [0x000000, 0x010111, 0x121222, 0x232333, 0x343444, 0x454555, 0x565666, 0x676777, 0x787888, 0x898999, 0x9A9AAA, 0xABABBB, 0xBCBCCC, 0xCDCDDD, 0xDEDEEE, 0xEFEFFF]
PureGray = [0x000000, 0x111111, 0x222222, 0x333333, 0x444444, 0x555555, 0x666666, 0x777777, 0x888888, 0x999999, 0xAAAAAA, 0xBBBBBB, 0xCCCCCC, 0xDDDDDD, 0xEEEEEE, 0xFFFFFF]

delta_f = upperfreq / (Height - 1)
fftsize = -int(-samplerate//delta_f) # math.ceil(samplerate / delta_f)

class ScreenArray():
    def __init__(self, width, height):
        self.array = np.zeros((height, width), dtype=np.int32)
        self.inputWarn = False

    def callback(self, indata, frames, time, status):
        if status: print(status)
        if not any(indata):
            print("\x1b[31mInput Warning..\x1b[0m" if not self.inputWarn else '\x1b[31m.\x1b[0m',end='',flush=True)
            self.inputWarn = True

        magnitude = np.abs(np.fft.rfft(indata[:, 0], n=fftsize))
        magnitude *= strength / fftsize
        self.array[:, -1] = [BlueWhite[int(np.clip(x, 0, 1) * (len(BlueWhite) - 1))] for x in magnitude[0:Height]]
        self.array = np.roll(self.array, 1, axis=1) # shift one pixel to the left

def main():
    pg.init()  # prepare window
    pg.display.set_caption("Audio Spectrogram")
    screen = pg.display.set_mode((Width, Height))
    drawArray = ScreenArray(int(Width/dialate), Height)
    #savebuffer = None
    #savesurf = pg.Surface((Width, Height))
    saveprogress = 0 #dialsave = 0
    running = True
    with sd.InputStream(channels=1, callback=drawArray.callback, blocksize=int(samplerate * blocksize / 1000), samplerate=samplerate):
        while running:
            for e in pg.event.get():
                if e.type == pg.QUIT or e.type == pg.KEYDOWN and (e.key == pg.K_ESCAPE or e.key == pg.K_q):
                    running = False

            screen.fill(0)
            stretched = np.repeat(drawArray.array, dialate, axis=1)
            pg.surfarray.blit_array(screen, np.rot90(stretched,-1)) # np.fliplr(np.rot90(stretched))
            pg.display.update()
            saveprogress += 1
            if saveprogress >= int(Width/dialate):
                saveprogress = 0
                pg.image.save(screen, f"rec/{strftime('%-y-%-m-%-d_%H-%M-%S')}.png")

            ''' #compressed
            if saveprogress >= int(Width/dialate):
                saveprogress = 0
                if savebuffer == None:
                    savebuffer = np.copy(drawArray.array)
                else:
                    savebuffer = np.concatenate((drawArray.array,savebuffer), axis=1)
                dialsave += 1
                if dialsave >= dialate:
                    dialsave = 0
                    pg.surfarray.blit_array(savesurf, np.rot90(savebuffer,-1))
                    pg.image.save(savesurf, f"rec/{strftime('%-y-%-m-%-d_%H-%M-%S')}.png")
                    savebuffer = drawArray.array'''

if __name__ == '__main__':
    main()  # by Nik
    pg.quit()
