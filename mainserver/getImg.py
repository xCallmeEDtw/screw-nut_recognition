import requests

def download_image(url, save_path):
    try:
        # 發送 HTTP GET 請求
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 如果請求失敗，會拋出 HTTPError

        # 保存圖片到本地
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"圖片已成功保存到: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"下載圖片時發生錯誤: {e}")

if __name__ == "__main__":
    # 網頁圖片 URL
    image_url = "http://192.168.145.78/capture"
    
    # 保存的檔案路徑
    save_path = "capture_image.jpg"
    
    # 下載圖片
    download_image(image_url, save_path)
