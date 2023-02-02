# Miscellaneous Python Projects

This is a collection of my smaller Python projects that don't fit elsewhere.

---

## CalcPi

These are scripts I wrote to play with and visualize generating digits of Pi.

While researching that, I came across an article on [Spigot algorithms for Pi](https://www.gavalas.dev/blog/spigot-algorithms-for-pi-in-python/),
and their various Python implementations. The author seems to have discovered
one of the fastest ways of doing that in Python, & I couldn't find any faster.

Using the generator function by [GavalasDev](https://github.com/GavalasDev),
`CalcPi.py` & `CalcTau.py` live-print the digits in color to the terminal, and
`PiPixel.py` & `TauPixel.py` use Pygame to draw digits as color-coded pixels.
`DigitCompare.py` takes 1000 digits of half-Pi, Pi, and Tau, prints them out
together in rows, coloring digits which overlap in either 2 or all 3 rows.

---

## Matrix

This is my version of the classic Matrix code-rain animation, for the terminal.
Made this as a personal challenge on New Year's, and it turned out pretty nice.
I've since made improvements, some alternate versions, and added Japanese kana.
Might be Linux only, `Ctrl+C` to quit. [New version here!](https://github.com/Nikorasu/MatrixCode)

---

## Snake

This is a terminal-based Snake game I made, without using additional libraries.
It's pretty basic, play area fills the terminal, so resize it to your liking.
Use arrow keys or wasd to move, `q` to quit.
To get arrow keys working, Esc key won't work quite right, and needs 3 presses.

---

## Spectrogram

I put this together while learning to use sounddevice & numpy's fft function.
It's essentially just a reimplementation of sounddevice's spectrogram example,
using Pygame instead of ascii. The _save version outputs timestamped images.

---

## TypingWPM

This is a little typing-speed-test I wrote, after seeing someone make something
similar using Curses. I wanted to try doing it without Curses, and it worked!
`typingwpm.py` should be pretty portable, just needs the `pangrams.txt` file.

*Note: Slower terminals may bug after rapidly pressing 2 keys at the same time.*

---

If you like my projects and want to help me keep making more,
please consider donating on [my Ko-fi page](https://ko-fi.com/nik85)! Thanks!

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/F1F4GRRWB)

---

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.
        If not, see: https://www.gnu.org/licenses/gpl-3.0.html

Copyright (c) 2022  Nikolaus Stromberg - nikorasu85@gmail.com
