#! /usr/bin/python3
from gpiozero import Button

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

CFG_EN_MID = False

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
