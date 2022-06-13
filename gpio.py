#! /usr/bin/python3
import RPi.GPIO as GPIO
import time

# lets use pin numbers, i guess
GPIO.setmode(GPIO.BOARD)

# P1:
#    3V3  (1) (2)  5V
#  GPIO2  (3) (4)  5V
#  GPIO3  (5) (6)  GND
#  GPIO4  (7) (8)  GPIO14
#    GND  (9) (10) GPIO15
# GPIO17 (11) (12) GPIO18
# GPIO27 (13) (14) GND
# GPIO22 (15) (16) GPIO23
#    3V3 (17) (18) GPIO24
# GPIO10 (19) (20) GND
#  GPIO9 (21) (22) GPIO25
# GPIO11 (23) (24) GPIO8
#    GND (25) (26) GPIO7
# pinout ----^

# the default pin assignments for our track
ALL_START_PIN = 3
LANE1_MID_PIN = 5
LANE2_MID_PIN = 7
LANE3_MID_PIN = 11
LANE4_MID_PIN = 13
LANE1_END_PIN = 15
LANE2_END_PIN = 19
LANE3_END_PIN = 21
LANE4_END_PIN = 23

GPIO.setup(ALL_START_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(LANE1_MID_PIN, GPIO.IN)
#GPIO.setup(LANE2_MID_PIN, GPIO.IN)
#GPIO.setup(LANE3_MID_PIN, GPIO.IN)
#GPIO.setup(LANE4_MID_PIN, GPIO.IN)
GPIO.setup(LANE1_END_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LANE2_END_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LANE3_END_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LANE4_END_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def lane1_end():
   et = time.time_ns()
   return;

GPIO.add_event_detect(LANE1_END_PIN, GPIO.RISING, callback=lane1_end)



GPIO.cleanup()
