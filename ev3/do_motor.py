#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#from time import perf_counter
from ev3dev.ev3 import *
from ev3dev2.sound import Sound
from time import sleep
import socket


outer_motor = LargeMotor('outA')

control_motor = LargeMotor('outC')

def connect_to_server():
    server_ip = '192.168.38.242'  # 將此處替換為伺服器的 IP 位址
    server_port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print("link")
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data or data == "close":
                print("aa")
                break
            
            print(":")
            if data == "forward":
                outer_motor.run_forever(speed_sp=-5*(50))
                sleep(3)
                outer_motor.stop()
            elif data == "r":
                control_motor.run_forever(speed_sp=5*(50))
                sleep(3)
                control_motor.stop()
            elif data == "l":
                control_motor.run_forever(speed_sp=-5*(50))
                sleep(3)
                control_motor.stop()
            elif data == "stop":
                outer_motor.stop()
                control_motor.stop()
            elif data == "beep":
                sound.beep()
            else:
                print("ig")
    finally:
        client_socket.close()
        print("discon")

connect_to_server()
# while True:

#   #totalL = (valueL[0] + valueL[1] + valueL[2])
#   #totalR = (valueR[0] + valueR[1] + valueR[2])
#   # print(valueL)
#   # print(valueR)
#   # error = (valueR- valueL )
#   outer_motor.run_forever(speed_sp=-5*(50))
#   # outer_motor.run_forever(speed_sp=5*(50 + Pi*error))
#   sleep(5)
#   break
# outer_motor.stop()
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