import time
import serial
import random
import csv
from datetime import datetime

PORT = "COM5"
BAUD = 9600

HIGH = 127
MED = 85
LOW = 50

SHORT = 0.25
LONG = 0.8

vib = serial.Serial(PORT, BAUD)

def buzz_motor(ser, strength, duration=1):
    ser.write(f"{int(strength)}\n".encode())
    time.sleep(duration)
    ser.write(b"0\n")

def like1():
    buzz_motor(vib, LOW, 0.1)
    time.sleep(0.075)
    buzz_motor(vib, LOW, 0.1)

def heart1():
    buzz_motor(vib, MED, 0.25)
    time.sleep(0.1)
    buzz_motor(vib, MED, 0.25)

def sad1():
    buzz_motor(vib, LOW, 0.8)

def angry1():
    buzz_motor(vib, HIGH, 0.8)

def haha1():
    buzz_motor(vib, LOW, 0.15)
    time.sleep(0.05)
    buzz_motor(vib, MED, 0.15)
    time.sleep(0.05)
    buzz_motor(vib, HIGH, 0.15)

def yay1():
    buzz_motor(vib, HIGH, 0.25)
    time.sleep(0.1)
    buzz_motor(vib, HIGH, 0.25)
    time.sleep(0.1)
    buzz_motor(vib, HIGH, 0.25)

def like2():
    buzz_motor(vib, LOW, SHORT)

def heart2():
    buzz_motor(vib, MED, SHORT)

def sad2():
    buzz_motor(vib, LOW, LONG)

def angry2():
    buzz_motor(vib, HIGH, LONG)

def haha2():
    buzz_motor(vib, HIGH, SHORT)

def yay2():
    buzz_motor(vib, MED, LONG)

def do_trials(v):
    now = datetime.now()
    filename = "../raw-data/" + now.strftime("%H%M%S") + ".csv"
    types = ["like", "heart", "sad", "angry", "haha", "yay"]
    trials = []
    for type in types:
        trials += [type] * 4
    random.shuffle(trials)
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        for trial in trials:
            writer.writerow([trial,])
            exec(trial + str(v) + "()")
            time.sleep(5)

do_trials(1)