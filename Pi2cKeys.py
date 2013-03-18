#Kellen Manning 2013
#github.com/bmnz
#Interfacing MCP23016 to RPi I2C to uinput/gamepad which will eventually be seen by AdvMAME
import uinput
from Adafruit_MCP230xx import Adafruit_MCP230XX

#Kellen Manning 16 MAR 2013
class MCP_Input:
    """
    Gather, via I2C protocol, the state of buttons hooked up to a MCP23017 IC. Convert it into something useful and pass the state info on to associaton Button objects.
    """
    address = 0
    num_gpios = 0
    mcp = None
    buttons = []
    debug_states = []

    def __init__(self, address = 0x20, num_gpios = 16):
        "Initalize with address=0x20 and num_gpios=16. Second chip is most likely set to 0x21"
        self.address = address
        self.num_gpios = num_gpios
        self.mcp = Adafruit_MCP230XX(address, num_gpios)
        self.pullup_all_pins()

    def pullup_all_pins(self):
        "Set each gpio pin on the MCP23017 to input w/internal pullup enabled."
        for x in range(0,num_gpios):
            self.mcp.pullup(x, 1)

    def readU16(self):
        "Reads both 8-bit registers in the MCP23017, combines them, returns a 16-bit number. Function originally defined in Adafruit_I2C."
        return mcp.readU16()

    def new_button_append( self, button ):
        "Append a new button to this Gamepad device. Returns the new number of total buttons in device."
        self.buttons.append(button)
        return len(self.buttons)

    def remove_button(self, index=-1):
        "Removes a button with the given index (0-15). Defaults to last button added (if during setup process)"
        self.buttons.pop(index)

    def set_all_button_states(self):
        states = self.readU16()
        self.debug_states = [(states>>x)&1 for x in range(0,num_gpios)]
        [ b.set_button_state(s) for (b,s) in zip(self.buttons, self.debug_states) ]


    #TODO: Figure out how to create a lambda/generator function for functions
    #that perform an action over every button in this class. I shouldn't have
    #to repeat "for x in range(0,num_gpios)" so many times.
    #TIL: You can pass functions as objects. Python is objects, duh!

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
            uinput.BTN_FORWARD, 
            uinput.BTN_BACK, 
            uinput.BTN_LEFT, 
            uinput.BTN_RIGHT, 
            )

    eventstr = {}
    eventstr[uinput.BTN_A] = "BTN_A" 
    eventstr[uinput.BTN_B] = "BTN_B" 
    eventstr[uinput.BTN_C] = "BTN_C" 
    eventstr[uinput.BTN_START] = "BTN_START" 
    eventstr[uinput.BTN_FORWARD] = "BTN_FORWARD"  
    eventstr[uinput.BTN_BACK] = "BTN_BACK"  
    eventstr[uinput.BTN_LEFT] = "BTN_LEFT"  
    eventstr[uinput.BTN_RIGHT] = "BTN_RIGHT"  
    
    device = uinput.Device(events)

    def new_button_append( self, button ):
        "Append a new button to this Gamepad device. Returns the new number of total buttons in device."
        self.buttons.append(button)
        return len(self.buttons)

    def remove_button(self, index=-1):
        "Removes a button with the given index (0-15). Defaults to last button added (if during setup process)"
        self.buttons.pop(index)

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

    #MCP_Input-related assignments
    pin =  -1 #zero through fifteen
    
    #gamepad-related assignments
    uinput_key = ()
    key_state_previous = 0

    #Debounce constants
    DEBOUNCE_TIME = 0.3
    SAMPLE_FREQ = 10
    MAXIMUM = (DEBOUNCE_TIME * SAMPLE_FREQ)

    #integrator debouncer info
    integrator = 0

    def set_pin(self, pin):
        "Assign a pin number from an external class. Returns pin for validation."
        if (pin >= 0 and pin <= 15):
            self.pin = pin
        return self.pin

    def get_pin(self):
        return self.pin

    def set_debounce_max( self, MAXIMUM ):
        "Use to change the debounce constant."
        self.MAXIMUM = MAXIMUM
        return self.MAXIMUM

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
        return self.uinput_key

    def get_uinput_key( self ):
        "Returns 2-tuple uinput data such as uinput.BTN_START."
        return self.uinput_key


