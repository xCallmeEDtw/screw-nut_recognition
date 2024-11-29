#include "myFuncLib.h"
#include <SPIFFS.h>    // 包含 SPIFFS 庫
#include <FS.h>        // 包含文件系統支持
void myRGB(int r,int g, int b){
  analogWrite(RedPin, r); 
  analogWrite(GreenPin, g); 
  analogWrite(BluePin, b); 
}

void setupWifi(){
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());

    // Start the server
    server.begin();
    Serial.println("Server started");
}


void sendHTMLPage(WiFiClient& client) {



    client.println("HTTP/1.1 200 OK");
    client.println("Content-type:text/html");
    client.println("Connection: close");
    client.println();
    client.println(htmlPage);
}

