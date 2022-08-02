import meshtastic
import meshtastic.serial_interface
from pubsub import pub
import sched, time, datetime
import tkinter 
from tkinter import filedialog
from tkinter import *
import random
import string
import os
from pathlib import Path
import csv

tx_time = []
final_payload = []
total_payload_size = []
data_lines = []
cnt = 0
#def onConnection(interface, topic=pub.AUTO_TOPIC): # called when we (re)connect to the radio
    # defaults to broadcast, specify a destination ID if you wish
    #interface.sendText("hello mesh")

#pub.subscribe(onConnection, "meshtastic.connection.established")
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
        global result_str
        # choose from all ascii letters
        letters = string.printable
        result_str = ''.join(random.choice(letters) for l in range(length))
        #print("Random string of length", length, "is:", result_str)

def sendText(payload):
    global dt, cnt
    # get date and time to record Tx timestamp
    dt = datetime.datetime.now()
    tx_time.append(dt.strftime("%H:%M:%S"))
    final_payload.append(tx_time[cnt] + " " + payload)
    interface.sendText(final_payload[cnt])
    total_payload_size.append(20 + len(final_payload[cnt]))   # preamble length = 20 bytes
    cnt += 1

def TxCSV(tx_time, total_payload_size, final_payload, dt):
    workDir = os.getcwd()
    fpath_write = Path(workDir + "/ProcessedLogs")
    fpath_write.mkdir(exist_ok=True)
    header = ["Tx Time (timezone)", "msg", "Total Payload Size (bytes)"]
    print(len(tx_time))
    with open(str(fpath_write) + "/TxData_IN_" + dt.strftime("%Y%m%d_%H%M%S") + \
            ".csv", mode="w", newline = '\n', encoding="utf-8") as TxDataFile:
        writer = csv.writer(TxDataFile)
        writer.writerow(header)
        for w in range(len(tx_time)):
            print(w)
            data_lines.append([tx_time[w], total_payload_size[w], final_payload[w]]) 
        writer.writerows(data_lines)
    print("counter=", cnt)
    print("***Created CSV***")

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
generatePayloadButton = Button(win, text= "Generate String", activeforeground='white', image = pixel, 
                width = 100, height = 13, compound="c", activebackground='#46403E', 
                command = lambda:getRandomString(payload_length))
generatePayloadButton.place(x = 240, y = 60)

# Send Text using generated string
# Create a Button to send Text over lora mesh via mehstastic
sendTextButton = Button(win, text= "Send Text", activeforeground='white', image = pixel, 
                width = 100, height = 13, compound="c", activebackground='#46403E', 
                command = lambda:sendText(result_str))
sendTextButton.place(x = 145, y = 100)

# Create a Button to create CSV and record Tx Data
CSVButton = Button(win, text= "Create CSV", activeforeground='white', image = pixel, 
                width = 100, height = 13, compound="c", activebackground='#46403E', 
                command = lambda:TxCSV(tx_time, total_payload_size, final_payload, dt))
CSVButton.place(x = 145, y = 150)

# quit gui
QuitButton = Button(win, text="Quit", activeforeground='white', activebackground='#46403E', 
                    command = win.destroy)
QuitButton.place(x = 230, y = 250)


win.mainloop()