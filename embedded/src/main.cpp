#include "Arduino.h"
#include <EasyTransfer.h>


#ifndef LED_BUILTIN
#define LED_BUILTIN 13
#endif

EasyTransfer g_easy_transfer;

typedef struct data_msg{
  uint32_t valueint;
  float valuefloat;
}data_msg;

data_msg g_data_package;
int g_count = 0;

void setup()
{
    pinMode(LED_BUILTIN, OUTPUT);
    Serial.begin(115200);  // start Serial port
    while(!Serial);  // wait for Serial port to be opened
    g_easy_transfer.begin(details(g_data_package), &Serial);
}

void loop()
{
    g_data_package.valueint = g_count++;
    g_data_package.valuefloat = random(0, 10);
    g_easy_transfer.sendData();
    delay(1000);
}
