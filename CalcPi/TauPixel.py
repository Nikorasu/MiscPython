#!/usr/bin/env python3
# by Nik Stromberg - nikorasu85@gmail.com - MIT 2022

import pygame as pg

WIDTH = 1920           # Window Width
HIGHT = 1080           # Window Height
PSIZE = 4              # Pixel size/ratio
# unused alternative color palettes
GRYGRAD = [0,0x1C1C1C,0x383838,0x545454,0x707070,0x8C8C8C,0xA8A8A8,0xC4C4C4,0xE0E0E0,0xFFFFFF]
RAINBOW = [0xFF0000,0xFF7F00,0xFFFF00,0x7FFF00,0x00FF00,0x00FF7F,0x00FFFF,0x007FFF,0x0000FF,0x7F00FF]
RAINALT = [0xFF0000,0xFF9900,0xCCFF00,0x33FF00,0x00FF66,0x00FFFF,0x0066FF,0x3300FF,0xCC00FF,0xFF0099]

# from https://www.gavalas.dev/blog/spigot-algorithms-for-pi-in-python/
def calcTau(n=1000):
    q,r,t,i = 1, 180, 30, 2
    while i < n+2:
        u,y = 3*(3*i+1)*(3*i+2), (q*(27*i-12)+5*r)//(5*t)
        yield y
        q,r,t,i = 10*q*i*(2*i-1),10*u*(q*(5*i-2)+r-y*t),t*u,i+1

class drawArray():
    def __init__(self, bigSize):
        self.size = (bigSize[0]//PSIZE, bigSize[1]//PSIZE)
        self.image = pg.Surface(self.size).convert()
        self.iarray = pg.surfarray.array3d(self.image)
        self.maxdigits = self.size[0] * self.size[1]
        self.tau_digits = calcTau(self.maxdigits)
        self.dcount = self.pixelX = self.pixelY = 0
    def update(self):
        digit = next(self.tau_digits)
        color = pg.Color(0)  # preps color so we can use hsva
        color.hsva = ((360/10*digit), 100, 100) # (0,0,100/10*digit)
        self.iarray[(self.pixelX,self.pixelY)] = color[0:3] #GRYGRAD[digit]
        if self.pixelX <= self.size[0]-2:
            self.pixelX += 1
        else:  #self.pixelX = 0 if self.pixelX >= self.size[0]-1 else self.pixelX + 1
            self.pixelX = 0
            self.pixelY += 1
        self.dcount += 1
        pg.surfarray.blit_array(self.image, self.iarray)
        return self.image, (self.dcount < self.maxdigits)

def main():
    pg.init()  # prepare window
    pg.display.set_caption("TauPixels")
    screen = pg.display.set_mode((WIDTH, HIGHT))
    drawLayer = drawArray((WIDTH, HIGHT))
    calculating = True
    # Main Loop
    while calculating:
        for e in pg.event.get():
            if e.type == pg.QUIT or e.type == pg.KEYDOWN and (e.key == pg.K_ESCAPE or e.key == pg.K_q):
                return

        screen.fill(0)
        drawImg, calculating = drawLayer.update()
        # resizes and draws the surfArray to screen
        rescaled_img = pg.transform.scale(drawImg, (WIDTH, HIGHT))
        pg.Surface.blit(screen, rescaled_img, (0,0))
        pg.display.update()

    pg.image.save(rescaled_img, "tau_output.png")

    clock = pg.time.Clock()
    while True: # hold result on screen
        for e in pg.event.get():
            if e.type == pg.QUIT or e.type == pg.KEYDOWN and (e.key == pg.K_ESCAPE or e.key == pg.K_q or e.key==pg.K_SPACE):
                return
        clock.tick(30)
if __name__ == '__main__':
    main()  # by Nik
    pg.quit()
