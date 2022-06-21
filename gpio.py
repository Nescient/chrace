#! /usr/bin/python3
import fcntl
import os
import sys

# https://stackoverflow.com/a/384493
def instance_already_running(label="default"):
    """
    Detect if an an instance with the label is already running, globally
    at the operating system level.

    Using `os.open` ensures that the file pointer won't be closed
    by Python's garbage collector after the function's scope is exited.

    The lock will be released when the program exits, or could be
    released if the file pointer were closed.
    """

    lock_file_pointer = os.open(f"/tmp/instance_{label}.lock", os.O_WRONLY | os.O_CREAT)

    try:
        fcntl.lockf(lock_file_pointer, fcntl.LOCK_EX | fcntl.LOCK_NB)
        already_running = False
    except IOError:
        already_running = True

    return already_running

if instance_already_running():
   print('This script is already running.  Wait for that to close.')
   exit(1)

##############################################################################################################
from gpiozero import Button
from signal import pause
from threading import Barrier, Event
import time, sys

CFG_EN_MID = False
CFG_DEBUG = True
CFG_RACE = None

if CFG_DEBUG:
   from gpiozero import Device
   from gpiozero.pins.mock import MockFactory
   from random import randint
   from time import sleep
   Device.pin_factory = MockFactory()

if len(sys.argv) > 1:
   print(f'Starting Race {sys.argv[1]}')
   import chrace.asgi
   from django.apps import apps
   Race = apps.get_model('tourneys', 'Race')
   myrace = Race.objects.get(id=sys.argv[1])
   print(myrace)

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
ALL_START = Button(2)
if CFG_EN_MID:
   LANE1_MID = Button(7)
   LANE2_MID = Button(8)
   LANE3_MID = Button(9)
   LANE4_MID = Button(10)
LANE1_END = Button(3)
LANE2_END = Button(4)
LANE3_END = Button(17)
LANE4_END = Button(27)

# b = Barrier(4, timeout=60.0)
done = [ Event(), Event(), Event(), Event() ]
times = []

def lane1_end():
   et = time.time_ns()
   LANE1_END.when_pressed = None
   print(f'lane1 {et}')
   times[0] = et
   done[0].set()
   return;

def lane2_end():
   et = time.time_ns()
   LANE2_END.when_pressed = None
   print(f'lane2 {et}')
   times[1] = et
   done[1].set()
   return;

def lane3_end():
   et = time.time_ns()
   LANE3_END.when_pressed = None
   print(f'lane3 {et}')
   times[2] = et
   done[2].set()
   return;

def lane4_end():
   et = time.time_ns()
   LANE4_END.when_pressed = None
   print(f'lane4 {et}')
   times[3] = et
   done[3].set()
   return;

LANE1_END.when_pressed = lane1_end
LANE2_END.when_pressed = lane2_end
LANE3_END.when_pressed = lane3_end
LANE4_END.when_pressed = lane4_end

# blocks until the start button goes
print('Waiting for start')
if CFG_DEBUG:
   sleep(1)
else:
   ALL_START.wait_for_press()
start_time = time.time_ns()
print(f'GO GO {start_time}')
times = [start_time, start_time, start_time, start_time]

if CFG_DEBUG:
   sleep(randint(1,5))
   LANE1_END.pin.drive_low()
   LANE1_END.pin.drive_high()
   LANE1_END.pin.drive_low()
   LANE1_END.pin.drive_high()
   sleep(randint(1,5))
   LANE2_END.pin.drive_low()
   LANE2_END.pin.drive_high()
   LANE2_END.pin.drive_low()
   LANE2_END.pin.drive_high()
   sleep(randint(1,5))
   LANE3_END.pin.drive_low()
   LANE3_END.pin.drive_high()
   LANE3_END.pin.drive_low()
   LANE3_END.pin.drive_high()
   sleep(randint(1,5))
   LANE4_END.pin.drive_low()
   LANE4_END.pin.drive_high()
   LANE4_END.pin.drive_low()
   LANE4_END.pin.drive_high()

hard_stop_time = (start_time / (10 ** 9)) + 15.0
for e in done:
  now = time.time_ns() / (10 ** 9)
  if now < hard_stop_time:
     if not e.wait(hard_stop_time - now):
        print('Timed out waiting for lane to finish!')
  elif not e.is_set():
     print('Timed out waiting for finish!')

print('Done')

for i, t in enumerate(times):
   print(f'lane{i + 1} {(t - start_time)/(10 ** 9)}')
