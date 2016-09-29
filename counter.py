import RPi.GPIO as GPIO
from time import sleep


GPIO.setmode(GPIO.BCM)

data = 22
latch = 27
clock = 17
up_in = 23
reset = 24

GPIO.setwarnings(False)
GPIO.setup(data, GPIO.OUT)
GPIO.setup(latch, GPIO.OUT)
GPIO.setup(clock, GPIO.OUT)
GPIO.setup(up_in, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(reset, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

dig_state = 0

digits = {
    "off": "0",
    "0" : "222",
    "1" : "6",
    "2" : "186",
    "3" : "174",
    "4" : "102",
    "5" : "236",
    "6" : "252",
    "7" : "134",
    "8" : "254",
    "9" : "238",
    "10" : "247",
    "11" : "255",
    "12" : "217",
    "13" : "223",
    "14" : "249",
    "15" : "241",
    }


def shiftout(byte):
    GPIO.output(latch, 0)
    for x in range(8):
        GPIO.output(data, (int(byte) >> x) & 1)
        GPIO.output(clock, 1)
        GPIO.output(clock, 0)
    GPIO.output(latch, 1)


def circle_load(iterations):

    pattern = [2,4,8,16,64,128]
    #pattern = [32, 98, 118, 236, 254]

    for x in range(iterations):
        for item in pattern:
            shiftout(int(item))
            sleep(.1)
    shiftout(digits["off"])    
 
    return


def loop_load(iterations):

    pattern = [160,68,40,18]

    for x in range(iterations):
        for item in pattern:
            shiftout(int(item))
            sleep(.2)
    shiftout(digits["off"])    
 
    return


def counter_callback():
    """
    Increment the number up to F
    """
    global dig_state


    if dig_state >= 15:
        print "F reached"
        return
    else:
        dig_state += 1
        print dig_state
        shiftout(digits[str(dig_state)])

    return


def counter_reset():
    """
    Reset the counter back to 0
    """

    global dig_state
    hold_time = 3

    # need hold for hold timer to avoid accidental resets
    sleep(3)

    if GPIO.input(24) == GPIO.LOW:
        dig_state = 0
        print "Resetting for new game..."
        circle_load(6)
        shiftout(digits[str(dig_state)])
    
    return


if __name__ == "__main__":


    #starting position
    shiftout(digits["0"])

    while True:

        if GPIO.input(23) == GPIO.LOW:
            counter_callback()
            sleep(.5)
        elif GPIO.input(24) == GPIO.LOW:
            counter_reset()
            sleep(.5)
        

"""
        x =raw_input(">> ")
        
        if not x.strip():
            pass 
        elif x.strip() == "circle":
            circle_load(10)
        elif x.strip() == "loop":
            loop_load(10)
        else:
            shiftout(digits[x])
        sleep(.1)

"""
