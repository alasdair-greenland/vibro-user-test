import time
import serial

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

def like():
    buzz_motor(vib, LOW, 0.1)
    time.sleep(0.075)
    buzz_motor(vib, LOW, 0.1)

def heart():
    buzz_motor(vib, MED, 0.25)
    time.sleep(0.1)
    buzz_motor(vib, MED, 0.25)

def sad():
    buzz_motor(vib, LOW, 0.8)

def angry():
    buzz_motor(vib, HIGH, 0.8)

def haha():
    buzz_motor(vib, LOW, 0.15)
    time.sleep(0.05)
    buzz_motor(vib, MED, 0.15)
    time.sleep(0.05)
    buzz_motor(vib, HIGH, 0.15)

def yay():
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

like2()
time.sleep(1)
sad2()