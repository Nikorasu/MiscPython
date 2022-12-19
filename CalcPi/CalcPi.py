#!/usr/bin/env python3
# by Nik Stromberg - nikorasu85@gmail.com - MIT 2022

import time
start = time.perf_counter()

# from https://www.gavalas.dev/blog/spigot-algorithms-for-pi-in-python/
def calcPi(n=1000):
    q,r,t,i = 1,180,60,2
    while i < n+2:
        u,y = 3*(3*i+1)*(3*i+2),(q*(27*i-12)+5*r)//(5*t)
        yield y
        q,r,t,i = 10*q*i*(2*i-1),10*u*(q*(5*i-2)+r-y*t),t*u,i+1

colors = ('\033[90m','\033[37m','\033[36m','\033[96m','\033[94m','\033[32m','\033[93m','\033[31m','\033[91m','\033[95m')
pi_digits = calcPi(100000)
fullDigits = []
lastDigit = 0

try:
    for d in pi_digits:
        fullDigits.append(str(d))
        print(colors[d] + str(d), end='', flush=True)
        lastDigit += 1
except KeyboardInterrupt:
    print("\n\033[93mStopped by user!", end='')

print("\n\033[0mDigits calculated:", lastDigit)
with open("pi_"+str(lastDigit)+".txt", "w") as savefile:
    print(*fullDigits,sep='',file=savefile)

end = time.perf_counter()
howlong = end - start
print("Time:", howlong)
