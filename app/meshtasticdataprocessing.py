import re
import csv
import tkinter 
from tkinter import filedialog
from tkinter import *
import datetime
import pytz
from pathlib import Path
import os, sys
# lists and arrays declaration
textmsg = []
rxtime = []
num = []
whole_line = []
data_lines = []
log_lines = []
sender = []
id = []

#  Variables definition

# r"" is used to consider path as a raw string. 
# 2nd option use double backslash. Else it gives unicode error
# Define App class 
class App(tkinter.Tk):
    def __init__( self ):
        super().__init__()
        
        # Configure the root window
        self.title("Data Processing")
        self.geometry('500x300')

        # Buttons
        # Select serial logs file
        SerialLogsButton = Button(self, text="Serial Logs", activeforeground='white', 
                            activebackground='#46403E', command=self.selectFile)
        SerialLogsButton.place(x=25, y=50)
        # process serial logs
        PrcSerialLogsButton = Button(self, text="Process Serial Logs", 
                            activeforeground='white', activebackground='#46403E', 
                            command=lambda:self.processSerialLogs(fpath))
        PrcSerialLogsButton.place(x=25, y=100)

    def selectFile(self):
        global fpath
        #defaultSys = os.path.dirname(sys.modules['__main__'].__file__)
        # initialdir=defaultSys
        fpath = filedialog.askopenfilenames(title="Select file", 
                filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        print(len(fpath))

    def processSerialLogs(self, fpath):
        # open file containing logs
        logFile = open(fpath[0], mode="r")
        rawLogs = logFile.readlines()
        logFile.close()
        print("File length is: " + str(len(rawLogs)) + " lines")
        for f in range(len(rawLogs)):
            log_lines.append(re.sub(",", "", rawLogs[f]))
            s1 = re.search("(.*) msg=(.*)", log_lines[f])
            if s1:
                #num.append(re.sub(r'\D', "", s1.group(1)))
                tempstr = s1.group(1)
                textmsg.append(s1.group(2))
                #s2 =  re.search(" ", tempstr)
                #print("Spaces ", tempstr.count(" "))    # number of spaces can be 6 or 7
                #num = re.search("^(.*) ", tempstr)
                rxtime.append(tempstr[:tempstr.find(" ")])
                word_list = log_lines[f].split()
                for w in range(len(word_list)):
                    fromfind = re.search("(.*)from=(.*)", word_list[w])
                    idfind = re.search("(.*)id=(.*)", word_list[w])
                    if fromfind:
                        sender.append(int(fromfind.group(2), 0))
                    if idfind:
                        id.append(int(idfind.group(2), 0))
                whole_line.append(word_list)
                #for i in range(len(word_list)):
                #   all_txmsg[f][i
        header = ['Rx Time', 'Sender', 'id', 'msg']
        dt = datetime.datetime.now(pytz.timezone('Europe/Berlin'))
        workDir = os.getcwd()
        fpath_write = Path(workDir + "/ProcessedLogs")
        fpath_write.mkdir(exist_ok=True)
        with open(str(fpath_write) + "/SerialData_" + dt.strftime("%Y%m%d_%H%M") + ".csv", mode="w", newline = '\n') as dataFile:
            writer = csv.writer(dataFile)
            writer.writerow(header)
            for wr in range(len(rxtime)):
                data_lines.append([rxtime[wr], sender[wr], id[wr], textmsg[wr]])
            writer.writerows(data_lines)

if __name__ == '__main__':
    app = App()
    app.mainloop()


