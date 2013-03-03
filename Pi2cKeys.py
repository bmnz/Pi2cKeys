#Kellen Manning 2013
#Interfacing MCP23016 to RPi I2C to uinput/gamepad which will eventually be seen by AdvMAME
import uinput

#Kellen Manning 26 FEB 2013
class Gamepad:
    "Gamepad class keeps track of button states and emits the appropriate key presses."
    pass

    previous_state = 0

    events = (
            #list of keys in /usr/include/linux/input.h
            uinput.BTN_A,
            uinput.BTN_B,
            uinput.BTN_C,
            uinput.BTN_START,
            uinput.BTN_X, #UP
            uinput.BTN_Y, #DOWN
            uinput.BTN_TL, #LEFT
            uinput.BTN_TR, #RIGHT
            )
    
    device = uinput.Device(events)

    #Emit_Keypress
    #Logic to Determine whether we call Emit_Keypress
    #Organize/Contain ALL THE Button objects! Includes logic to assign them.



#Kellen Manning 23 FEB 2013
class Button:
    "Button class holds key and button state info, peforms debounce"

    #state variables
    key_state= 0
    button_state = 0

    #Debounce constants
    DEBOUNCE_TIME = 0.3
    SAMPLE_FREQ = 10
    MAXIMUM = (DEBOUNCE_TIME * SAMPLE_FREQ)

    #integrator debouncer info
    integrator = 0

    def set_debounce_max( self, MAXIMUM ):
        "Use to change the debounce constant."
        self.MAXIMUM = MAXIMUM

    #debounce button, output key
    def debounce(self): 
        "Integrator-based debounce from http://www.kennethkuhn.com/electronics/debounce.c"
        #Step 1 - Update integrator
        if( self.button_state == 0 and self.integrator > 0 ):
            self.integrator = self.integrator - 1
        elif( self.integrator < self.MAXIMUM ):
            self.integrator = self.integrator + 1

        #Step 2 - Update output
        if( self.integrator == 0 ):
            self.key_state = 0
        elif( self.integrator >= self.MAXIMUM ):
            self.integrator = self.MAXIMUM #"Defensive" code (redundant)
            self.key_state = 1

    def set_button_state( self, button_state ):
        "Automatically performs debounce upon set"
        self.button_state = button_state
        self.debounce()

    def get_button_state( self ):
        "This only exists for debug purposes"
        return self.button_state

    def get_key_state( self ):
        return self.key_state

