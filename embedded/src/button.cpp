
#include "button.h"

button_handle* init_button(int pin, int debounce_delay)
{
    button_handle *ret = malloc(sizeof(button_handle));
    pinMode(pin, INPUT);
    ret->pin = pin;
    ret->previous_state = LOW;
    ret->current_state = LOW;
    ret->debounce_delay = debounce_delay;
    ret->last_debounce_time = 0;
    ret->event_up_lock = 0;
    return ret;
}

void update_button(button_handle *handle)
{
    int reading = digitalRead(handle->pin);
    if(reading != handle->previous_state)
    {
        handle->last_debounce_time = millis();
    }

    if ((millis() - handle->last_debounce_time) > handle->debounce_delay)
    {
        if (reading != handle->current_state)
        {
            if(reading == HIGH && handle->event_up_lock == 0)
            {
                handle->event_up_lock = millis();
            }
            handle->current_state = reading;
        }
    }
    handle->previous_state = reading;
}

void reset_up_event_button(button_handle *handle)
{
    handle->event_up_lock = 0;
}

unsigned long get_last_up_event_time_button(button_handle *handle)
{
    return handle->event_up_lock;
}

int read_button(button_handle *handle)
{
    return handle->current_state;
}

void release_button(button_handle *handle)
{
    free(handle);
}