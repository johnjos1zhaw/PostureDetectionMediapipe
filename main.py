from sense_hat import SenseHat 
from pomodoro import pomodoro
import time
sense = SenseHat()


# Define a variable to track whether the button is currently pressed
button_pressed = False

# Callback function for button press event
def button_pressed_callback(event):
    global button_pressed
    if event.action == "pressed":
        if not button_pressed:
            time.sleep(5)
            sense.clear(0,255,0)
            pomodoro()
            button_pressed = True
    elif event.action == "released":
        button_pressed = False

# Assign the callback function to the down direction
sense.stick.direction_middle = button_pressed_callback

# Keep the program running to listen for stick events
while True:
    pass
