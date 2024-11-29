#include <Arduino.h>
#include "myFuncLib.h"  // 包含頭文件，這樣可以訪問全域變數和函數

// LED
int RedPin = 32;  
int BluePin = 33;
int GreenPin =25;
int forward = 0;
/*wifi*/
char* ssid = "e";
char* password = "11111111";
WiFiServer server(80);

int ButtPin = 23;

/*THink Speak*/
String serverName = "http://api.thingspeak.com/update"; // 設置 ThingSpeak 的伺服器 URL
String apiKey_write = "FGGT16C2UCECVLK9"; // 替換為您的 API Key
String apiKey_read = "GC406KVGSLOWTW33"; // 替換為您的 API Key
String readChannel = "2733797";

void setup() {
    Serial.begin(115200);

    // 測試 myPinOut 和 myPinIn 函數
    myPinOut(RedPin,BluePin,GreenPin);
    myPinIn(ButtPin);
    setupWifi();
    
}

int nowState = 0; //0 av //1 doing // 3 err
int shingFlag=0;
int butState ;
void loop() {
    // 检查是否有新的客户端连接
  if(nowState==0){
    myRGB(0,255,0);
  }else if(nowState==1){
    myRGB(255,255,0);
  }else{
    myRGB(255,0,0);
  }

    butState = digitalRead(ButtPin);
    // Serial.println(butState);
    if (butState == LOW && forward == 0 && nowState!=-1){
      
      while (butState == LOW){
        butState = digitalRead(ButtPin);
      //  Serial.println(butState);
      }
      forward = 1;
    }
    if (butState == LOW && nowState==-1){
      
      while (butState == LOW){
        butState = digitalRead(ButtPin);
      //  Serial.println(butState);
      }
      nowState = 0;
      delay(3000);
    }






    WiFiClient client = server.available();
    if (client) {
        Serial.println("Client connected");
        String request = client.readStringUntil('\r'); // 读取 HTTP 请求行
        client.flush(); // 清空缓冲区

        Serial.println("Request: " + request);

        // 处理 /start 路径
        if (request.indexOf("GET /start") >= 0) {
            // 保存当前的 forward 值供返回
            int currentForward = forward;

            // 将 forward 设置为 0，供下次返回
            forward = 0;

            // 返回当前的 forward 值
            client.println("HTTP/1.1 200 OK");
            client.println("Content-Type: text/plain; charset=utf-8");
            client.println("Connection: close");
            client.println();
            client.println("当前 forward 值为: " + String(currentForward));

            // 调试日志
            Serial.println("Returned forward: " + String(currentForward));
            Serial.println("Forward 已设置为: " + String(forward));
        } else if (request.indexOf("GET /sendStart") >= 0){
            nowState = 1; // 设置 nowState
            Serial.println("sendStart 请求触发, nowState 设置为: " + String(nowState));

            // 返回成功响应
            client.println("HTTP/1.1 200 OK");
            client.println("Content-Type: text/plain; charset=utf-8");
            client.println("Connection: close");
            client.println();
            client.println("sendStart 请求已处理");
        } else if (request.indexOf("GET /sendFinish") >= 0){
            nowState = 0; // 设置 nowState
            Serial.println("sendStart 请求触发, nowState 设置为: " + String(nowState));

            // 返回成功响应
            client.println("HTTP/1.1 200 OK");
            client.println("Content-Type: text/plain; charset=utf-8");
            client.println("Connection: close");
            client.println();
            client.println("sendStart 请求已处理");
        } else if (request.indexOf("GET /sendERR") >= 0){
            nowState = -1; // 设置 nowState
            Serial.println("sendStart 请求触发, nowState 设置为: " + String(nowState));

            // 返回成功响应
            client.println("HTTP/1.1 200 OK");
            client.println("Content-Type: text/plain; charset=utf-8");
            client.println("Connection: close");
            client.println();
            client.println("sendStart 请求已处理");        
        }else {
            // 未找到路径时返回 404
            client.println("HTTP/1.1 404 Not Found");
            client.println("Content-Type: text/plain; charset=utf-8");
            client.println("Connection: close");
            client.println();
            client.println("路径未找到");
        }

        client.stop(); // 关闭客户端连接
        Serial.println("Client disconnected");
    }
}






void shinging(){
    // 呼吸燈逐漸變亮的過程
    for (int brightness = 0; brightness <= 255; brightness++) {
        myRGB(brightness, 0, 0);  // 使用 myRGB() 將亮度設置為逐漸增加
        // Serial.println(brightness);
        delay(10);  // 調整這個延遲以控制變亮速度
    }

    // 呼吸燈逐漸變暗的過程
    for (int brightness = 255; brightness >= 0; brightness--) {
        myRGB(brightness, 0, 0);  // 使用 myRGB() 將亮度設置為逐漸減少
        delay(10);  // 調整這個延遲以控制變暗速度
    }   
}

void dealHtml(){
    WiFiClient client = server.available();
    if (client) {
        // Serial.println("Client connected");
        String request = "";

        // Read client request
        while (client.connected()) {
            if (client.available()) {
                char c = client.read();
                request += c;
                if (c == '\n') break;
            }
        }

        // Process motor control commands based on request
        if (request.indexOf("GET /cmd?command=shinging") >= 0) {
            shingFlag = 1;
            shinging();
        } else if (request.indexOf("GET /cmd?command=stop") >= 0) {
            myRGB(0,0,0);
            shingFlag = 0;
            
        } 

        // Serve the HTML page
        sendHTMLPage(client);

        // Close the client connection
        client.stop();
        // Serial.println("Client disconnected");
    }
}


String htmlPage = R"=====(
<!DOCTYPE html>
<html>
<head>
    <title>ESP32 Motor Control Web Server</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
        }
        h1 {
            color: #333;
        }
        .button-container {
            margin: 20px;
        }
        button {
            width: 150px;
            height: 40px;
            margin: 10px;
            font-size: 16px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>ESP32 Motor Control</h1>
    <p>Control the motor with the buttons below:</p>

    <div class="button-container">
        <button onclick="sendCommand('shinging')">Shinging</button>
        <button onclick="sendCommand('stop')">Stop</button>
<!--         <button onclick="sendCommand('toggle_direction')">Toggle Direction</button>
        <button onclick="sendCommand('accelerate')">Accelerate</button>
        <button onclick="sendCommand('decelerate')">Decelerate</button> -->
    </div>

    <script>
        function sendCommand(command) {
            // 假設發送請求到 ESP32 的 URL，並帶上命令參數
            fetch(`/cmd?command=${command}`)
                .then(response => response.text())
                .then(data => {
                    console.log(`Command ${command} sent successfully`);
                })
                .catch(error => {
                    console.error(`Error sending command ${command}:`, error);
                });
        }
    </script>
</body>
</html>
)=====";