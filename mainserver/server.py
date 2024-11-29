import socket
import getImg
import processIMG
from time import sleep
from reqStart import *
running = 0

def start_server():
    global running
    host = '192.168.38.242'  # 伺服器監聽所有可用網路介面
    port = 12345      # 自訂的通訊埠號

    # 建立 socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"伺服器已啟動，正在監聽 {host}:{port}")

    conn, addr = server_socket.accept()
    print(f"來自 {addr} 的連線已建立")

    try:
        while True:
            if running == 1:
                continue
            if get_forward_value() == 0:
                sleep(3)
                continue
            else:
                running = 1
                send_start()
                # message = input("輸入要發送的訊號 (q 結束): ")
                # if message == 'c':
                message = "forward"
                conn.sendall(message.encode())
                sleep(5)
                image_url = "http://192.168.38.78/capture"
                
                # 保存的檔案路徑
                save_path = "capture_image.jpg"
                
                # 下載圖片
                getImg.download_image(image_url, save_path)

                itemName = processIMG.proc_img()
                if itemName == "err":
                    toThinkSpeak(3)
                    send_err()
                    running = 0
                    continue


                if (itemName=='screw'):
                    message = 'r'
                    toThinkSpeak(0)
                else:
                    message = 'l'
                    toThinkSpeak(1)
                conn.sendall(message.encode())
                sleep(10)
                
                send_fin()
                running = 0

            # elif message.lower() == 'q':
            #     conn.sendall("close".encode())
            #     break
            # else:
            #     conn.sendall(message.encode())
    finally:
        conn.close()
        server_socket.close()
        print("伺服器已關閉")

if __name__ == "__main__":
    start_server()
