from turtle import left
import meshtastic
import meshtastic.serial_interface
from pubsub import pub
import sched, time
import tkinter 
from tkinter import filedialog
from tkinter import *
import random
import string


def onConnection(interface, topic=pub.AUTO_TOPIC): # called when we (re)connect to the radio
    # defaults to broadcast, specify a destination ID if you wish
    interface.sendText("hello mesh")

pub.subscribe(onConnection, "meshtastic.connection.established")
# By default will try to find a meshtastic device, otherwise provide a device path like /dev/ttyUSB0
interface = meshtastic.serial_interface.SerialInterface()

#s = sched.scheduler(time.time, time.sleep)

#def do_something(sc): 
#    print("Doing stuff...")
#    interface.sendText("hello mesh")
#    # do your stuff
#    sc.enter(60, 1, do_something, (sc,))

#s.enter(60, 1, do_something, (s,))
#s.run()

# Create an instance of tkinter frame or window
win = Tk()
win.title("Meshtastic Sender")
win.geometry('500x300')

def getPayloadLength():
        global payload_length
        #payload_length_entry = 0
        payload_length = int(payload_length_entry.get())
        print(type(payload_length))
        print("User input pyload length is : ", payload_length)

def getRandomString(length):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for l in range(length))
        print("Random string of length", length, "is:", result_str)

# Create an Entry widget to accept User Input
Label(win, text="Enter Payload Length").place(x = 10, y = 10)
payload_length_entry = Entry(win, width = 5)
payload_length_entry.focus_set()
payload_length_entry.place(x = 10, y = 30)
# Create a Button to validate Entry Widget
pixel = tkinter.PhotoImage(width=1, height=1)
payoadSizeButton = Button(win, text= "Set", activeforeground='white', image = pixel, width = 30, 
                height = 13, compound="c", activebackground='#46403E', command = getPayloadLength)
payoadSizeButton.place(x = 50, y = 30)

# Generate random string with size of user input payload length
Label(win, text="Generate random string: ").place(x = 10, y = 60)
# Create a Button to generate string
payoadSizeButton = Button(win, text= "Generate String", activeforeground='white', image = pixel, 
                width = 100, height = 13, compound="c", activebackground='#46403E', 
                command = lambda:getRandomString(payload_length))
payoadSizeButton.place(x = 150, y = 60)

# quit gui
QuitButton = Button(win, text="Quit", activeforeground='white', activebackground='#46403E', 
                    command = win.destroy)
QuitButton.place(x = 230, y = 250)


win.mainloop()

""" 
        

        
        
        
    

    


if __name__ == '__main__':
    app = App()

    #payload_length_entry.set(1)  # default value
    app.mainloop() """