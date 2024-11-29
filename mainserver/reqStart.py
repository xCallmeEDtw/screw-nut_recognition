import requests

# ESP32 的 IP 地址（替换为实际地址）
esp32_ip = "http://192.168.38.136"

# 请求路径
path = "/start"

# 获取 forward 的值
def get_forward_value():
    try:
        # 构建完整的 URL
        url = f"{esp32_ip}{path}"
        # 发送 GET 请求
        response = requests.get(url)
        # 检查请求状态
        if response.status_code == 200:
            #print("请求成功!")
            # 直接使用 response.text，无需重新编码
            #print("服务器返回的内容：", response.text)
            return int(response.text.split(': ')[1])
        else:
            print(f"请求失败，HTTP 状态码: {response.status_code}")
            return 0
    except Exception as e:
        print("请求过程中发生错误:", e)
        return None
def send_start():
    try:
        # 构建完整的 URL
        url = f"{esp32_ip}{'/sendStart'}"
        # 发送 GET 请求
        response = requests.get(url)
        # 检查请求状态
        if response.status_code == 200:
            # pass
            print("请求成功!")
            # 直接使用 response.text，无需重新编码
            #print("服务器返回的内容：", response.text)
            # return int(response.text.split(': ')[1])
        else:
            print(f"请求失败，HTTP 状态码: {response.status_code}")
            return 0
    except Exception as e:
        print("请求过程中发生错误:", e)
        return None

def send_fin():
    try:
        # 构建完整的 URL
        url = f"{esp32_ip}{'/sendFinish'}"
        # 发送 GET 请求
        response = requests.get(url)
        # 检查请求状态
        if response.status_code == 200:
            # pass
            print("请求成功!")
            # 直接使用 response.text，无需重新编码
            #print("服务器返回的内容：", response.text)
            # return int(response.text.split(': ')[1])
        else:
            print(f"请求失败，HTTP 状态码: {response.status_code}")
            return 0
    except Exception as e:
        print("请求过程中发生错误:", e)
        return None
def send_err():
    try:
        # 构建完整的 URL
        url = f"{esp32_ip}{'/sendERR'}"
        # 发送 GET 请求
        response = requests.get(url)
        # 检查请求状态
        if response.status_code == 200:
            # pass
            print("请求成功!")
            # 直接使用 response.text，无需重新编码
            #print("服务器返回的内容：", response.text)
            # return int(response.text.split(': ')[1])
        else:
            print(f"请求失败，HTTP 状态码: {response.status_code}")
            return 0
    except Exception as e:
        print("请求过程中发生错误:", e)
        return None
def toThinkSpeak(x):
    """
    將數值 x 發送到 ThingSpeak 的 field1
    :param x: 要發送的數值
    """
    api_key = "5XHODQCYF8573XBN"  # 你的 ThingSpeak API Key
    url = f"https://api.thingspeak.com/update"
    
    # HTTP GET 請求的參數
    params = {
        "api_key": api_key,
        "field1": x
    }

    try:
        # 發送 HTTP GET 請求
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            print(f"成功更新 ThingSpeak！回傳 ID: {response.text}")
        else:
            print(f"更新失敗，HTTP 狀態碼: {response.status_code}")
    except Exception as e:
        print(f"發生錯誤: {e}")

# if __name__ == "__main__":
#     # 获取并打印 forward 值
#     forward_value = get_forward_value()
#     if forward_value:
#         print("获取的 forward 值为:", forward_value)

# if __name__ == "__main__":
#     # 获取并打印 forward 值
#     forward_value = get_forward_value()
#     if forward_value:
#         print("获取的 forward 值为:", forward_value)
