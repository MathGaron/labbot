#include "Arduino.h"
#include <EasyTransfer.h>
#include "button.h"


#define LED_BUILTIN 13
#define LED_MESSAGE 4
#define BUTTON0 2
#define BUTTON1 3

int ledState = LOW;
int moisturePin = A1;

button_handle *g_button[2];


EasyTransfer g_easy_transfer;
typedef struct data_msg{
  uint8_t button0_state;
  uint8_t button1_state;
  uint16_t moisture_read;
}data_msg;

data_msg g_data_package;
int g_count = 0;

void setup()
{
    pinMode(LED_MESSAGE, OUTPUT);
    pinMode(LED_BUILTIN, OUTPUT);
    g_button[0] = init_button(BUTTON0, 50);
    g_button[1] = init_button(BUTTON1, 50);
    Serial.begin(115200);  // start Serial port
    while(!Serial);  // wait for Serial port to be opened
    g_easy_transfer.begin(details(g_data_package), &Serial);
    
}

unsigned long sendData_time = 0;

void loop()
{
    for(int i = 0; i < 2; ++i)
    {
        update_button(g_button[i]);
    }

    if (read_button(g_button[0]) == HIGH)
    {
        digitalWrite(LED_MESSAGE, HIGH);
    }
    if (read_button(g_button[1]) == HIGH)
    {
        digitalWrite(LED_BUILTIN, HIGH);
    }

    if((millis() - sendData_time) > 2000)
    {
        g_data_package.button0_state = LOW;
        g_data_package.button1_state = LOW;
        unsigned long last0 = get_last_up_event_time_button(g_button[0]);
        unsigned long last1 = get_last_up_event_time_button(g_button[1]);
        if ( last0 != 0 && millis() - last0 > 1000)
        {
            g_data_package.button0_state = HIGH;
            reset_up_event_button(g_button[0]);
            digitalWrite(LED_MESSAGE, LOW);
        }
        if ( last1 != 0 && millis() - last1 > 1000)
        {
            g_data_package.button1_state = HIGH;
            reset_up_event_button(g_button[1]);
            digitalWrite(LED_BUILTIN, LOW);
        }

	//Read sensors
        g_data_package.moisture_read = analogRead(moisturePin);	

        g_easy_transfer.sendData();
        sendData_time = millis();
    }
    delay(20);
}
