#Kellen Manning 2013
#Interfacing MCP23016 to RPi I2C to uinput/gamepad which will eventually be seen by AdvMAME
import uinput

#Kellen Manning 26 FEB 2013
class Gamepad:
    """
    Gamepad class represents one uinput gamepad device. Button objects are assigned to keys, and this class performs the logic to determine when to send/change keypresses. The gamepad has 8 buttons as designed: A,B,C,START,FORWARD,BACK,LEFT,RIGHT.

    Methods include:
    def update_all_the_keys( self ):
    def update_key( self, button ):


    """

    buttons = []

    events = (
            #list of keys in /usr/include/linux/input.h
            uinput.BTN_A,
            uinput.BTN_B,
            uinput.BTN_C,
            uinput.BTN_START,
            uinput.BTN_FORWARD, #UP
            uinput.BTN_BACK, #DOWN
            uinput.BTN_LEFT, 
            uinput.BTN_RIGHT, 
            )
    
    device = uinput.Device(events)

    def new_button_append( self, button ):
        "Append a new button to this Gamepad device. Returns the new number of total buttons in device."
        self.buttons.append(button)
        return len(self.buttons)

    #Logic to Determine whether we call device.emit
    def update_key( self, button ):
        "Contains logic for using uinput to update state of device.emit. Single button use suggested for debug purposes, use update_all_the_keys() during normal polling use instead."
        previous = button.get_key_state_previous()
        current = button.get_key_state()

        if( previous != current ):
            self.device.emit(button.get_uinput_key(), current) #Arg1 is uinput tuple, Arg2 is boolean state for press/release (1/0)



    def update_all_the_keys( self ):
        "Contains logic for using uinput to update state of device.emit for all buttons in gamepad"
        for b in self.buttons:
            self.update_key(b)
#End of Gamepad Class

#Kellen Manning 23 FEB 2013
class Button:
    """
    Button class holds key and button state info, peforms debounce internally. The following are methods that were intended to be called externally. Please consult the source for internal methods/data.
    
    Manipulating Internal State:
    def set_debounce_max( self, MAXIMUM )

    Gamepad-related Methods:
    def set_uinput_key( self, uinput_key ):
    def get_uinput_key( self ):
    def get_key_state_previous( self ):
    def get_key_state( self ):

    """

    #state variables
    key_state= 0
    button_state = 0
    
    #gamepad-related assignments
    uinput_key = ()
    key_state_previous = 0

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

    def set_button_state( self, booly ):
        "Automatically performs debounce upon set"
        self.button_state = booly
        self.debounce()

    def get_button_state( self ):
        "This only exists for debug purposes"
        return self.button_state

    def get_key_state( self ):
        "Return key's boolean state post-debounce"
        self.key_state_previous = self.key_state
        return self.key_state

    def get_key_state_previous( self ):
        "Returns key's boolean state from previous check. Updated from get_key_state, so call this FIRST!"
        return self.key_state_previous

    def set_uinput_key( self, uinput_key ):
        "Pass a uinput data tuple such as set_uinput_key( uinput.BTN_START )"
        self.uinput_key = uinput_key

    def get_uinput_key( self ):
        "Returns 2-tuple uinput data such as uinput.BTN_START."
        return self.uinput_key


