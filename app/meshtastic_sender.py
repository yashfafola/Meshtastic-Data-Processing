import meshtastic
import meshtastic.serial_interface
from pubsub import pub
import datetime, time
import tkinter 
from tkinter import filedialog
from tkinter import *
import random
import string
import os
from pathlib import Path
import csv
from threading import Timer
import subprocess
from subprocess import PIPE, TimeoutExpired

tx_time = []
final_payload = []
total_payload_size = []
serial_number = []
data_lines = []
cnt = 0
payload_length = 0
automatic_test_mode = False     # default test mode
send_interval = 0
increment_bytes = 0

#def onConnection(interface, topic=pub.AUTO_TOPIC): # called when we (re)connect to the radio
    # defaults to broadcast, specify a destination ID if you wish
    #interface.sendText("hello mesh")

#pub.subscribe(onConnection, "meshtastic.connection.established")
# By default will try to find a meshtastic device, otherwise provide a device path like /dev/ttyUSB0
#interface = meshtastic.serial_interface.SerialInterface()

# Create an instance of tkinter frame or window
win = Tk()
win.title("Meshtastic Sender")
win.geometry('500x300')

def getPayloadLength():
        global payload_length
        #payload_length_entry = 0
        payload_length = int(payload_length_entry.get())

def getRandomString(length):
        global result_str
        # choose from all lowercase and uppercase alphabets
        letters = string.ascii_letters
        result_str = ''.join(random.choice(letters) for l in range(length))
        #print("Random string of length", length, "is:", result_str)

def sendText(payload):
    global dt, cnt
    # get date and time to record Tx timestamp
    #final_payload.append(str(cnt) + ": " + payload)
    final_payload.append(payload)
    dt = datetime.datetime.now()
    tx_time.append(dt.strftime("%H:%M:%S"))
    process_sendtext = subprocess.Popen("meshtastic --sendtext \"" + final_payload[cnt] + "\"", stdin=None, \
            stdout=PIPE, universal_newlines=True, shell=True)
    try:
        pipeout, pipeerr = process_sendtext.communicate(timeout=15)
        pipeout_str = str(pipeout)
        pipeerr_str = str(pipeerr)
        print("Output of meshtastic cmd send--> " + pipeout_str)
        if pipeerr_str != "None":
                print("Error running meshtastic --sendtext shell command: " + pipeerr_str)
    except TimeoutExpired:
        process_sendtext.kill()
        pipeout, pipeerr = process_sendtext.communicate()
        pipeout_str = str(pipeout)
        pipeerr_str = str(pipeerr)
        print(pipeout_str)
        if pipeerr_str != None:
                print("Timeout!--> Error running meshtastic --sendtext shell command: " + \
                    pipeerr_str)
        print("Killed the meshtastic --sendtext process, because of timeout")
    #interface.sendText(final_payload[cnt])
    total_payload_size.append(20 + len(final_payload[cnt]))   # preamble length = 20 bytes
    serial_number.append(cnt+1)
    print("counter ", cnt)
    print("total payload Size", total_payload_size[cnt])
    cnt += 1
 
def TxCSV(tx_time, total_payload_size, final_payload, dt):
    workDir = os.getcwd()
    fpath_write = Path(workDir + "/ProcessedLogs")
    fpath_write.mkdir(exist_ok=True)
    header = ["Serial Number" ,"Tx Time (timezone)", "Total Payload Size (bytes)", "Payload"]
    print(len(tx_time))
    with open(str(fpath_write) + "/TxData_IN_" + dt.strftime("%Y%m%d_%H%M%S") + \
            ".csv", mode="w", newline = '\n', encoding="utf-8") as TxDataFile:
        writer = csv.writer(TxDataFile)
        writer.writerow(header)
        for w in range(len(tx_time)):
            data_lines.append([serial_number[w] ,tx_time[w], total_payload_size[w], final_payload[w]]) 
        writer.writerows(data_lines)
    print("counter=", cnt)
    print("___Created CSV___")

def getPayloadIncrement():
    global increment_bytes, payload_length
    global increment_flag
    increment_bytes = int(payload_increment_entry.get())
    if increment_bytes != 0:
        payload_length = increment_bytes
        increment_flag = True

def getSendInterval():
    global send_interval    # seconds
    send_interval = int(send_interval_entry.get())

def setAutomaticTestFlag():
    global automatic_test_mode
    automatic_test_mode = True
    doAutomaticTest()
    
def clearAutomaticTestFlag():
    global automatic_test_mode
    automatic_test_mode = False

def doAutomaticTest():
    global payload_length
    if not automatic_test_mode:
        Timer(send_interval, doAutomaticTest).cancel()
        print("stoppped timer")
        return
    print("send Interval", send_interval)
    # choose from all lowercase and uppercase alphabets
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for l in range(payload_length))
    print("payload length: ", payload_length)
    # prevent increment next payload size when the limit is reached
    if (payload_length + increment_bytes) < 232:      # max 237, -4 bytes ("10: ")
                                                      # -1  for safe tx
        payload_length = payload_length + increment_bytes
    else:
        clearAutomaticTestFlag()
    sendText(result_str)
    print("sent")
    Timer(send_interval, doAutomaticTest).start()
        
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
generatePayloadButton.place(x = 150, y = 60)

# Send Text using generated string
# Create a Button to send Text over lora mesh via mehstastic
sendTextButton = Button(win, text= "Send Text", activeforeground='white', image = pixel, 
                width = 100, height = 13, compound="c", activebackground='#46403E', 
                command = lambda:sendText(result_str))
sendTextButton.place(x = 10, y = 100)

# Create a Button to create CSV and record Tx Data
CSVButton = Button(win, text= "Create CSV", bg='#1DF12A', activeforeground='white', image = pixel, 
                width = 100, height = 13, compound="c", activebackground='#46403E', 
                command = lambda:TxCSV(tx_time, total_payload_size, final_payload, dt))
CSVButton.place(x = 10, y = 130)

# Create an payload increment Entry widget to accept User Input
Label(win, text="Enter payload increment bytes").place(x = 320, y = 10)
payload_increment_entry = Entry(win, width = 5)
payload_increment_entry.place(x = 400, y = 30)
# Create a Button to validate Entry Widget
payoadIncrementButton = Button(win, text= "Set", activeforeground='white', image = pixel, width = 30, 
                height = 13, compound="c", activebackground='#46403E', command = getPayloadIncrement)
payoadIncrementButton.place(x = 440, y = 30)

# Create an payload increment Entry widget to accept User Input
Label(win, text="Enter Send Interval (sec)").place(x = 350, y = 60)
send_interval_entry = Entry(win, width = 5)
send_interval_entry.place(x = 400, y = 90)
# Create a Button to validate Entry Widget
sendIntervalButton = Button(win, text= "Set", activeforeground='white', image = pixel, width = 30, 
                height = 13, compound="c", activebackground='#46403E', command = getSendInterval)
sendIntervalButton.place(x = 440, y = 90)

# Create a Button to send Text in Automatic Test Mode over lora mesh via mehstastic
startTestButton = Button(win, text= "Start Automatic Test", activeforeground='white', image = pixel, 
                width = 150, height = 13, compound="c", activebackground='#46403E', 
                command = setAutomaticTestFlag)
startTestButton.place(x = 320, y = 120)

# Create a Button to stop Automatic Test Mode 
stopTestButton = Button(win, text= "Stop Automatic Test", activeforeground='white', image = pixel, 
                width = 150, height = 13, compound="c", activebackground='#46403E', 
                command = clearAutomaticTestFlag)
stopTestButton.place(x = 320, y = 150)

Label(win, text="---OR---").place(x = 230, y = 10)

# quit gui
QuitButton = Button(win, text="Quit", activeforeground='white', activebackground='#46403E', 
                    command = win.destroy)
QuitButton.place(x = 230, y = 250)


win.mainloop()
