import serial
import numpy as np
import math
import struct
import matplotlib.pyplot as plt
import binascii

import matplotlib.pyplot as plt
from math import pi, atan2, sqrt
from scipy.linalg import eig

ser = serial.Serial('COM5', 115200)

import cmath

SPEED_OF_LIGHT  = 299792458
num_iterations = 200     # 进行的循环次数
iteration = 0

rawFrame = []

while True:
    byte  = ser.read(1)        
    rawFrame += byte
    print(rawFrame)
    #print(len(rawFrame))
    if rawFrame[-3:]==[255, 255, 255, 255]:
        if len(rawFrame) == 7:
            print(rawFrame)