import socket

def start_client():
    server_ip = '192.168.100.123'  # 伺服器 IP (與伺服器的 IP 一致)
    server_port = 12345            # 伺服器的通訊埠號

    # 建立 socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"已連接到伺服器 {server_ip}:{server_port}")

    try:
        while True:
            # 接收伺服器訊息
            data = client_socket.recv(1024)
            if not data:
                print("伺服器已斷開連接")
                break
            
            # 打印接收到的訊息
            message = data.decode()
            print(f"收到伺服器訊息: {message}")

            # 如果訊息是 "close"，則結束
            if message == "close":
                print("伺服器請求結束連接")
                break
    finally:
        client_socket.close()
        print("已關閉與伺服器的連接")

if __name__ == "__main__":
    start_client()
