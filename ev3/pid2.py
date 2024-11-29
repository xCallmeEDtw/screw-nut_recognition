#!/usr/bin/env python3
#from time import perf_counter
from ev3dev.ev3 import *
#from ev3fast import *

lMotor = LargeMotor('outB')
rMotor = LargeMotor('outA')
lSensor = ColorSensor('in2')
rSensor = ColorSensor('in1')

LOOPS = 500

#startTime = perf_counter()
for a in range(0,LOOPS):
  valueL = lSensor.raw
  valueR = rSensor.raw
  totalL = (valueL[0] + valueL[1] + valueL[2])
  totalR = (valueR[0] + valueR[1] + valueR[2])
  print(totalL)
  print(totalR)
  error = (totalR- totalL )/10
  lMotor.speed_sp = 5*(30 - error)
  rMotor.speed_sp = 5*(30 + error)
  lMotor.run_forever()
  rMotor.run_forever()
#endTime = perf_counter()

lMotor.stop()
rMotor.stop()

#print(str(LOOPS / (endTime - startTime)))