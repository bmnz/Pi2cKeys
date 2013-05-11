#Kellen Manning 2013
#github.com/bmnz
#Control logic for Pi2cKeys.py classes. May need to include timing for polling as well.
import Pi2cKeys.py
#Setup - 2 MCP_Input chips, 4 Gamepads, 32 Buttons.
addr = 0x20
gamepads = []
mcps = []
buttons = []
_debug_flag = 0

def automatic_setup(self):
    pass

def guided_setup(self):
    #This is going to go step-by-step w/user input.. add control flow msgs here.
    print "Setup file (.buttons) not found. Beginning guided setup. The successful completion of this process will output a new .buttons file."

    for x in range(0,32):
        button = Pi2cKeys.Button()
        gamepad = None
        mcp = None

        if(x%16 == 0):
            mcp = Pi2cKeys.MCP_Input( address = ( addr + len(mcps) ) )
            self.mcps.append(mcp)
        if(x%8 == 0):
            gamepad = Pi2cKeys.Gamepad()
            self.gamepads.append(gamepad)

        #Add the button to both gamepad and mcp
        mcp.new_button_append(button)
        gamepad.new_button_append(button)

        #Set pin, Set uinput_key. The strategy is to ask user to press the correct uinput_key, and determine the relevant pin.
        #Which uinput are we on? (events[x%8])
        #Ask user to press this key (evenstr[events[x%8])
	print("Player " + str(x%8+1) + ", press " + gamepad.eventstr[events[x%8]])

	tmp = mcp.readU16()
        #Figure out which bit is set (loop, no 'hack' for this)
	bits = [x for x in range(0,16) if (1<<x) == tmp]
	if( len(bits) == 1):
	    #Only one bit set
	    #Set that bit-number as the right one
        #Assign the pin
        #User test/verify
        #Next button
