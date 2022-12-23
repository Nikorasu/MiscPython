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
## Spectrogram

I put this together while learning to use sounddevice & numpy's fft function.
It's essentially just a reimplementation of sounddevice's spectrogram example,
using Pygame instead of ascii. The _save version outputs timestamped images.

---
## TypingWPM

This is a little typing-speed-test I wrote, after seeing someone make something
similar using Curses. I wanted to try doing it without Curses, and it worked!
`typingwpm.py` should be pretty portable, just needs the `pangrams.txt` file.
Works well, but there's a small bug if user presses 2 buttons at once rapidly.

---

If you like my projects and want to help me keep making more,
please consider donating on [my Ko-fi page](https://ko-fi.com/nik85)! Thanks!

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/F1F4GRRWB)