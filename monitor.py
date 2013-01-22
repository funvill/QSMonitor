#!/path/to/python 
"""
Learning python from 
https://developers.google.com/edu/python/introduction


"""


import win32gui
import pythoncom, pyHook, sys, logging
import http.client, urllib.parse
import string

# Settings 
# -------------------------------------
SETTING_SERVER_DOMAIN               = 'www.abluestar.com' 
SETTING_SERVER_PATH                 = '/utilities/monitor/server.php' 

# How offten to call home with the key logger information. Number of keys 
SETTING_POLL_FREQUENCY_KEYLOGGER    = 10 

# Constance 
APP_VERSION         = "0.01"
APP_LAST_UPDATED    = "Jan 20, 2013"

# Global 
keyDatabase = {} 
keyLoggerCount = 0 

# http://docs.python.org/3.3/library/http.client.html?highlight=http.client#http.client 
def CallHome( user, prameters ):
    # shorten the prameters so that it only sends back the values that are non zero. 
    # http://stackoverflow.com/questions/6307394/removing-dictonary-entries-with-no-values-python
    for p in list(prameters.keys()):
        if prameters[p] == 0 :
            del prameters[ p] 

    # Add the user to the prameter list 
    prameters['user'] = user 
    prameters['pass'] = '1234'
    
    # Convert the prameters in to a url string 
    urlParams = urllib.parse.urlencode( prameters )
    
    # Generate the http header 
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    
    # Sent the message to the server. 
    conn  = http.client.HTTPConnection('www.abluestar.com') 
    conn.request("POST", "/utilities/monitor/server.php", urlParams, headers)
    response = conn.getresponse()
    if( response.status != 200 ) :
        print("Http Error")
        print(r1.status, r1.reason)
        return False 
       
    print( response.read() ) 
    return True  
    
def OnKeyboardEvent(event):
    global keyDatabase
    global keyLoggerCount 
    keyLoggerCount += 1 
    
    # http://code.activestate.com/recipes/553270-using-pyhook-to-block-windows-keys/ 
    print ('MessageName:',event.MessageName )
    print ('Message:',event.Message)
    print ('Time:',event.Time)
    print ('Window:',event.Window)
    print ('WindowName:',event.WindowName)
    print ('Ascii:', event.Ascii, chr(event.Ascii) )
    print ('Key:', event.Key)
    print ('KeyID:', event.KeyID)
    print ('ScanCode:', event.ScanCode)
    print ('Extended:', event.Extended)
    print ('Injected:', event.Injected)
    print ('Alt', event.Alt)
    print ('Transition', event.Transition)
    print ('---')    
        
    # check to see if this key has ever been pressed before 
    # if it has not then add it and set its start value to zero. 
    if event.Key not in keyDatabase:
        keyDatabase[ event.Key ] = 0 ; 
    
    # Incurment the key value 
    keyDatabase[ event.Key ] += 1 ; 
    return True
    
def SetUp():
    
    global keyDatabase
    global keyLoggerCount 
    keyLoggerCount = 0  

    # When the user presses a key down anywhere on their system 
    # the hook manager will call OnKeyboardEvent function.     
    hm = pyHook.HookManager()
    hm.KeyDown = OnKeyboardEvent
    hm.HookKeyboard()
    
def Update() :
    global keyLoggerCount 
    global keyDatabase
    
    # Check the message cue to see if there are any keys waiting for us. 
    # http://stackoverflow.com/questions/10004658/how-do-i-use-my-own-loop-with-pyhook-instead-of-pumpmessages
    pythoncom.PumpWaitingMessages()
    
    # if we have recived more then the poll frequency amount of keys then 
    # call home and tell someone about it. 
    if keyLoggerCount > SETTING_POLL_FREQUENCY_KEYLOGGER :
        if CallHome( 'test', keyDatabase ) :
            # Reset the database and the key count on contact with home 
            keyLoggerCount = 0 
            keyDatabase = {} 
        else :
            print ("Error could not call home")
       

# Display information about the program and what its suppose to do. 
def About():
   print( '-'*80 ) 
   print( "This application was built to monitor your keys pressed and report back to abluestar.com web server for logging. The keys will be grouped by letter to obfuscate the sequence that they are written\n" ); 
   print( 'Version: \t' + APP_VERSION ) 
   print( 'Last Updated: \t' + APP_LAST_UPDATED ) 
   print( '-'*80 ) 



def main() :
    # Display the program information 
    About()      
    
    # Setup the system to monior key presses 
    SetUp() 
    
    # Main process loop. 
    while( True ) : 
        Update() ; 

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()