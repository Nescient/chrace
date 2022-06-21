#! /usr/bin/python3
import fcntl, os, sys

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

##############################################################################################################
from threading import Event
done = [ Event(), Event(), Event(), Event() ]
times = [ 0, 0, 0, 0]

def lane1_end(Button):
   et = time.time_ns()
   Button.when_pressed = None
   print(f'lane1 {et}')
   times[0] = et
   done[0].set()
   return;

def lane2_end(Button):
   et = time.time_ns()
   Button.when_pressed = None
   print(f'lane2 {et}')
   times[1] = et
   done[1].set()
   return;

def lane3_end(Button):
   et = time.time_ns()
   Button.when_pressed = None
   print(f'lane3 {et}')
   times[2] = et
   done[2].set()
   return;

def lane4_end(Button):
   et = time.time_ns()
   Button.when_pressed = None
   print(f'lane4 {et}')
   times[3] = et
   done[3].set()
   return;
   
def twiddle_buttons(buttons):
   for b in buttons:
      sleep(randint(1,5))
      b.pin.drive_low()
      b.pin.drive_high()
      b.pin.drive_low()
      b.pin.drive_high()
   return

def start_race(debug):
   pihw.LANE1_END.when_pressed = lane1_end
   pihw.LANE2_END.when_pressed = lane2_end
   pihw.LANE3_END.when_pressed = lane3_end
   pihw.LANE4_END.when_pressed = lane4_end

   # blocks until the start button goes
   print('Waiting for start')
   if debug:
      sleep(1)
   else:
      ALL_START.wait_for_press()
   start_time = time.time_ns()
   print(f'GO GO {start_time}')
   times[0] = start_time
   times[1] = start_time
   times[2] = start_time
   times[3] = start_time

   if debug:
      twiddle_buttons([pihw.LANE1_END, pihw.LANE2_END, pihw.LANE3_END, pihw.LANE4_END])

   hard_stop_time = (start_time / (10 ** 9)) + 15.0
   for e in done:
      now = time.time_ns() / (10 ** 9)
      if now < hard_stop_time:
         if not e.wait(hard_stop_time - now):
            print('Timed out waiting for lane to finish!')
      elif not e.is_set():
         print('Timed out waiting for finish!')
   print('Done')
   return start_time, times

def finish_race(race, start, times):
   for i, t in enumerate(times):
      print(f'lane{i + 1} {(t - start)/(10 ** 9)}')
   if race:
      print(f'Setting lane times for {race}')

if __name__ == "__main__":
   if instance_already_running():
      print('This script is already running.  Wait for that to close.')
      exit(1)

   from gpiozero import Button
   from signal import pause
   import time, sys

   CFG_DEBUG = True
   CFG_RACE = None

   if CFG_DEBUG:
      from gpiozero import Device
      from gpiozero.pins.mock import MockFactory
      from random import randint
      from time import sleep
      Device.pin_factory = MockFactory()

   # the default pin assignments for our track
   import gpio_pi1B2 as pihw
   ALL_START = pihw.ALL_START
   LANE1_END = pihw.LANE1_END
   LANE2_END = pihw.LANE2_END
   LANE3_END = pihw.LANE3_END
   LANE4_END = pihw.LANE4_END
   
   # get the race
   if len(sys.argv) > 1:
      print(f'Starting Race {sys.argv[1]}')
      import chrace.asgi
      from django.apps import apps
      Race = apps.get_model('tourneys', 'Race')
      CFG_RACE = Race.objects.get(id=sys.argv[1])

   start_time, times = start_race(CFG_DEBUG)
   finish_race(CFG_RACE, start_time, times)
