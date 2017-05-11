#ifndef _BUTTON_H_   // if x.h hasn't been included yet...
#define _BUTTON_H_   //   #define this so the compiler knows it has been included
#include "Arduino.h"

typedef struct button_handle
{
    int pin;
    int previous_state;
    int current_state;

    unsigned long debounce_delay;
    unsigned long last_debounce_time;

    unsigned long event_up_lock;
}button_handle;

button_handle* init_button(int pin, int debounce_delay);
void update_button(button_handle *handle);
int read_button(button_handle *handle);
void reset_up_event_button(button_handle *handle);
unsigned long get_last_up_event_time_button(button_handle *handle);

#endif