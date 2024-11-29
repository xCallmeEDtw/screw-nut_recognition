# -*- coding: utf-8 -*-
import socket
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B
from ev3dev2.sound import Sound

def connect_to_server():
    server_ip = '192.168.145.26'  # 將此處替換為伺服器的 IP 位址
    server_port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print("link")

    # motor_left = LargeMotor(OUTPUT_A)
    # motor_right = LargeMotor(OUTPUT_B)
    sound = Sound()

    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data or data == "close":
                print("aa")
                break
            
            print(":")
            if data == "forward":
                pass
                # motor_left.on(50)
                # motor_right.on(50)
            elif data == "stop":
                pass
                # motor_left.off()
                # motor_right.off()
            elif data == "beep":
                sound.beep()
            else:
                print("ig")
    finally:
        client_socket.close()
        print("discon")

if __name__ == "__main__":
    connect_to_server()
