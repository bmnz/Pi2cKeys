#Kellen Manning 2013
#Interfacing MCP23016 to RPi I2C to uinput/gamepad which will eventually be seen by AdvMAME
#import uinput
#import 

#Kellen Manning 26 FEB 2013
#class Gamepad:
#    "Gamepad class keeps track of button states and emits the appropriate key presses."


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

