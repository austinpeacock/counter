import RPi.GPIO as GPIO
from time import sleep


GPIO.setmode(GPIO.BCM)

reset = 26

a_counter ={
        "trigger":4,
        "latch":17,
        "clock":27,
        "data":22,
        }

b_counter ={
        "trigger":18,
        "latch":23,
        "clock":24,
        "data":25,
        }

c_counter ={
        "trigger":12,
        "latch":16,
        "clock":20,
        "data":21,
        }

d_counter ={
        "trigger":5,
        "latch":6,
        "clock":13,
        "data":19,
        }

# set up GPIO pins, using BCM ports
GPIO.setwarnings(False)
# A
GPIO.setup(a_counter["data"], GPIO.OUT)
GPIO.setup(a_counter["latch"], GPIO.OUT)
GPIO.setup(a_counter["clock"], GPIO.OUT)
GPIO.setup(a_counter["trigger"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# B
GPIO.setup(b_counter["data"], GPIO.OUT)
GPIO.setup(b_counter["latch"], GPIO.OUT)
GPIO.setup(b_counter["clock"], GPIO.OUT)
GPIO.setup(b_counter["trigger"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# C
GPIO.setup(c_counter["data"], GPIO.OUT)
GPIO.setup(c_counter["latch"], GPIO.OUT)
GPIO.setup(c_counter["clock"], GPIO.OUT)
GPIO.setup(c_counter["trigger"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# D
GPIO.setup(d_counter["data"], GPIO.OUT)
GPIO.setup(d_counter["latch"], GPIO.OUT)
GPIO.setup(d_counter["clock"], GPIO.OUT)
GPIO.setup(d_counter["trigger"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# global reset
GPIO.setup(reset, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

a_dig_state = 0
b_dig_state = 0
c_dig_state = 0
d_dig state = 0 


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


def shiftout(byte, color):
    GPIO.output(color["latch"], 0)
    for x in range(8):
        GPIO.output(color["data"], (int(byte) >> x) & 1)
        GPIO.output(color["clock"], 1)
        GPIO.output(color["clock"], 0)
    GPIO.output(color["latch"], 1)

    return True


def load(iterations, _type):
    """
    Load animations for start up and reset
    """
    global a_counter
    global b_counter
    global c_counter
    global d_counter

    patterns = {
            "circle":[2,4,8,16,64,128],
            "loop":[160,68,40.18],
            "other":[32, 98, 118, 236, 254],
            }

    for x in range(iterations):
        for item in pattern[_type]:
            shiftout(int(item), a_counter)
            shiftout(int(item), b_counter)
            shiftout(int(item), c_counter) 
            shiftout(int(item), d_counter)
            sleep(.1)
    shiftout(digits["off"], a_counter)    
    shiftout(digits["off"], b_counter)    
    shiftout(digits["off"], c_counter)    
    shiftout(digits["off"], d_counter)    
 
    return


def a_counter_callback():
    """
    Increment the number up to F
    """
    global a_dig_state
    global a_counter

    if a_dig_state >= 15:
        print "A Counter F reached"
        return
    else:
        a_dig_state += 1
        print (f'A: {a_dig_state}')
        shiftout(digits[str(a_dig_state)], a_counter)

    return


def b_counter_callback():
    """
    Increment the number up to F
    """
    global b_dig_state
    global b_counter

    if b_dig_state >= 15:
        print "B Counter F reached"
        return
    else:
        b_dig_state += 1
        print (f'B: {b_dig_state}')
        shiftout(digits[str(b_dig_state)], b_counter)

    return


def c_counter_callback():
    """
    Increment the number up to F
    """
    global c_dig_state
    global c_counter

    if c_dig_state >= 15:
        print "C Counter F reached"
        return
    else:
        c_dig_state += 1
        print {f'C: {c_dig_state}')
        shiftout(digits[str(c_dig_state)], c_counter)

    return


def d_counter_callback():
    """
    Increment the number up to F
    """
    global d_dig_state
    global d_counter

    if d_dig_state >= 15:
        print "D Counter F reached"
        return
    else:
        d_dig_state += 1
        print (f'D: {d_dig_state}')
        shiftout(digits[str(d_dig_state)], d_counter)

    return


def counter_reset():
    """
    Reset all counters back to 0
    """

    global a_dig_state
    global b_dig_state
    global c_dig_state
    global d_dig_state

    global a_counter
    global b_counter
    global c_counter
    global d_counter

    hold_time = 3

    # need hold for hold timer to avoid accidental resets
    sleep(3)

    if GPIO.input(26) == GPIO.LOW:
        a_dig_state = 0
        b_dig_state = 0
        c_dig_state = 0
        d_dig_state = 0 

        print "Resetting for new game..."
        load(6,"circle")

        shiftout(digits[str(a_dig_state)], a_counter)
        shiftout(digits[str(b_dig_state)], b_counter)
        shiftout(digits[str(c_dig_state)], c_counter)
        shiftout(digits[str(d_dig_state)], d_coutner)
 
    return


if __name__ == "__main__":

    #starting positions
    load(6,"loop")

    shiftout(digits["0"], a_counter)
    shiftout(digits["0"], b_counter)
    shiftout(digits["0"], c_counter)
    shiftout(digits["0"], d_counter)

    while True:

        if GPIO.input(4) == GPIO.HIGH:
            a_counter_callback()
            sleep(2.5)
        elif GPIO.input(18) == GPIO.HIGH:
            b_counter_callback()
            sleep(2.5)
        elif GPIO.input(12) == GPIO.HIGH:
            c_counter_callback()
            sleep(2.5)
        elif GPIO.input(5) == GPIO.HIGH:
            d_counter_callback()
            sleep(2.5)
       # reset all 
        elif GPIO.input(26) == GPIO.HIGH:
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
