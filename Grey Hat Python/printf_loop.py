from ctypes import *
import time

msvcrt = cdll.msvcrt
counter = 0

string = "Loop iteration %d!\n" % counter

while True:
    msvcrt.printf(string.encode("ASCII"))
    time.sleep(2)
    counter += 1
