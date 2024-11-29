#!/usr/bin/env python3
#from time import perf_counter
from ev3dev.ev3 import *
from time import sleep
#from ev3fast import *

lMotor = LargeMotor('outB')
rMotor = LargeMotor('outA')
lSensor = ColorSensor('in2')
rSensor = ColorSensor('in1')

LOOPS = 1500
Pi =3
#startTime = perf_counter()
while True:
  valueL = lSensor.reflected_light_intensity
  valueR = rSensor.reflected_light_intensity
  #totalL = (valueL[0] + valueL[1] + valueL[2])
  #totalR = (valueR[0] + valueR[1] + valueR[2])
  print(valueL)
  print(valueR)
  error = (valueR- valueL )
  lMotor.run_forever(speed_sp=5*(50 - Pi*error))
  rMotor.run_forever(speed_sp=5*(50 + Pi*error))
  # lMotor.run_forever(speed_sp=5*(-10))
  # rMotor.run_forever(speed_sp=5*(-10))
  #lMotor.stop()
  #rMotor.stop()
  #lMotor.run_forever()
  #rMotor.run_forever()
#endTime = perf_counter()

#lMotor.stop()
#rMotor.stop()

#print(str(LOOPS / (endTime - startTime)))