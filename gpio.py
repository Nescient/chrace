#! /usr/bin/python3
from gpiozero import Button
from signal import pause
from threading import Barrier, Event
import time

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
ALL_START_PIN = 2
LANE1_MID_PIN = 3
LANE2_MID_PIN = 4
LANE3_MID_PIN = 17
LANE4_MID_PIN = 27
LANE1_END_PIN = 22
LANE2_END_PIN = 10
LANE3_END_PIN = 9
LANE4_END_PIN = 11

ALL_START = Button(ALL_START_PIN)
#GPIO.setup(LANE1_MID_PIN, GPIO.IN)
#GPIO.setup(LANE2_MID_PIN, GPIO.IN)
#GPIO.setup(LANE3_MID_PIN, GPIO.IN)
#GPIO.setup(LANE4_MID_PIN, GPIO.IN)
LANE1_END = Button(LANE1_END_PIN)
LANE2_END = Button(LANE2_END_PIN)
LANE3_END = Button(LANE3_END_PIN)
LANE4_END = Button(LANE4_END_PIN)

# b = Barrier(4, timeout=60.0)
done = [ Event(), Event(), Event(), Event() ]

def lane1_end():
   et = time.time_ns()
   print(f'lane1 {et}')
   done[0].set()
   return;

def lane2_end():
   et = time.time_ns()
   print(f'lane2 {et}')
   done[1].set()
   return;

def lane3_end():
   et = time.time_ns()
   print(f'lane3 {et}')
   done[2].set()
   return;

def lane4_end():
   et = time.time_ns()
   print(f'lane4 {et}')
   done[3].set()
   return;

LANE1_END.when_pressed = lane1_end
LANE2_END.when_pressed = lane2_end
LANE3_END.when_pressed = lane3_end
LANE4_END.when_pressed = lane4_end

# blocks until the start button goes
print('Waiting for start')
ALL_START.wait_for_press()
start_time = time.time_ns()
print(f'GO {start_time}')

hard_stop_time = (start_time / (10 ** 9)) + 5.0
for e in done:
   now = time.time_ns() / (10 ** 9)
   if now < hard_stop_time:
      if not e.wait(hard_stop_time - now):
         print('Timed out waiting for lane to finish!')
   elif not e.is_set():
      print('Timed out waiting for finish!')

print('Done')
