#ifndef FUNCTIONS_H
#define FUNCTIONS_H

#include <Arduino.h>  // 包含 Arduino 函數庫
#include <WiFi.h>
#include <HTTPClient.h>
// #include <Arduino_JSON.h>
// 聲明全域變數
extern int RedPin;  // 讓其他文件可以使用 RedPin
extern int BluePin;
extern int GreenPin;


extern char* ssid;// = "Edw";
extern char* password;// = "12345678";

extern String htmlPage;

extern WiFiServer server;//(80);




// Motor parameters
extern int motorSpeed;// = 0;            // Initial speed
extern bool motorDirection;// = true;    // true for clockwise, false for counterclockwise
extern bool motorStatus;// = false;      // true for ON, false for OFF


// 模板函數的定義必須在頭文件中
template<typename... Pins>
void myPinOut(Pins... pins) {
    int pinsArray[] = {pins...};
    for (int pin : pinsArray) {
        pinMode(pin, OUTPUT);
        // Serial.print("Pin ");
        // Serial.print(pin);
        // Serial.println(" set to OUTPUT");
    }
}

template<typename... Pins>
void myPinIn(Pins... pins) {
    int pinsArray[] = {pins...};
    for (int pin : pinsArray) {
        pinMode(pin, INPUT);
        // Serial.print("Pin ");
        // Serial.print(pin);
        // Serial.println(" set to INPUT");
    }
}


void myRGB(int r,int g, int b);
void setupWifi();
void sendHTMLPage(WiFiClient& client) ;


extern String serverName;
extern String apiKey_write;
extern String apiKey_read;
extern String readChannel;

// 模板函數聲明
template<typename... Values>
void PostToThingSpeak(Values... values) {
    // 確認 WiFi 是否已連接
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("WiFi Disconnected");
        return;
    }

    HTTPClient http;
    WiFiClient client;

    // 構建 HTTP POST 數據
    String httpRequestData = "api_key=" + apiKey_write;

    // 使用可變參數來構建 field1, field2, ..., fieldN
    int fieldIndex = 1;
    int dataArray[] = {values...};  // 將參數包轉為數組
    for (int value : dataArray) {
        httpRequestData += "&field" + String(fieldIndex) + "=" + String(value);
        fieldIndex++;
    }

    // 開始連接並設置 HTTP 請求頭
    http.begin(client, serverName);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");

    // 發送 HTTP POST 請求
    int httpResponseCode = http.POST(httpRequestData);

    // 檢查響應代碼
    if (httpResponseCode > 0) {
        Serial.print("HTTP POST Response code: ");
        Serial.println(httpResponseCode);
    } else {
        Serial.println("Error on HTTP POST request");
    }

    http.end();  // 釋放資源
}

// template<typename... Values>
// void getFromThingSpeak(Values*... values) {
//     // 確認 WiFi 是否已連接
//     if (WiFi.status() != WL_CONNECTED) {
//         Serial.println("WiFi Disconnected");
//         return;
//     }

//     HTTPClient http;
//     WiFiClient client;

//     // 組合 URL
//     // String url = "https://api.thingspeak.com/channels/"+ readChannel + "/feeds.json?api_key=" + apiKey_read + "&results=2";
//     String url = "https://api.thingspeak.com/channels/2733797/feeds.json?api_key=GC406KVGSLOWTW33&results=2";
//     // 發送 GET 請求
//     delay(10000); // 等待 10 秒
//     http.begin(url);
//     int httpResponseCode = http.GET();

//     if (httpResponseCode > 0) {
//         String payload = http.getString();
//         Serial.print("HTTP Response code: ");
//         Serial.println(httpResponseCode);

//         // 解析 JSON 數據
//         JSONVar jsonData = JSON.parse(payload);
//         if (JSON.typeof(jsonData) == "undefined") {
//             Serial.println("Parsing input failed!");
//             return;
//         }

//         // 提取字段值並更新指向的變量
//         String* valuesArray[] = {values...};  // 獲取所有變量指針
//         for (size_t i = 0; i < sizeof...(values); ++i) {
//             if (valuesArray[i] != nullptr) {
//                 // 根據數組索引動態生成字段名稱，例如 "field1", "field2" 等
//                 String fieldName = "field" + String(i + 1);
//                 *valuesArray[i] = (const char*) jsonData["feeds"][0][fieldName];
                
//                 // 打印提取出的字段值
//                 // Serial.print("Field ");
//                 // Serial.print(i + 1);
//                 // Serial.print(" value: ");
//                 // Serial.println(*valuesArray[i]);
//             }
//         }
//     } else {
//         Serial.println("Error on HTTP request");
//     }

//     http.end();  // 釋放資源
// }



#endif
