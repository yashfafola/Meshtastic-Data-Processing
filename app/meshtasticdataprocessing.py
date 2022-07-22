import re
import csv
from sqlite3 import Timestamp
import tkinter 
from tkinter import filedialog
from tkinter import *
import datetime
from pathlib import Path
import os, sys
# lists and arrays declaration
textmsg = []
rxtimestampunix = []
rxdatetime = []
num = []
whole_line = []
data_lines = []
log_lines = []
sender = []
receiver = []
requestid = []
hoplimit = []
channelid = []
rxSNR = []
bw = []
sf = []
cr = []
symLen = []
totalpayloadSize = []
airtime = []

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
        append_count = 0
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
                #rxtime.append(tempstr[:tempstr.find(" ")])
                word_list = log_lines[f].split()
                for w in range(len(word_list)):
                    fromfind = re.search("(.*)from=(.*)", word_list[w])
                    idfind = re.search("(.*)id=(.*)", word_list[w])
                    if fromfind:
                        sender.append(int(fromfind.group(2), 0))
                    if idfind:
                        requestid.append(int(idfind.group(2), 0))
                whole_line.append(word_list)
                for f2 in range(12):    # withn above 12th line of detected msg, 
                                        # all info is is obtained
                    if f-f2 < 0:
                        print("Starting lines of serial data don't contain enough info")
                    else:
                        s2 = re.search("decoded message", log_lines[f-f2])
                        s3 = re.search("payloadSize", log_lines[f-f2])
                        if s2:
                            # get the data points from a line
                            sub_wordlist = log_lines[f-f2].replace("(", "").replace(")", "").split()
                            receiver.append(sub_wordlist[7])
                            hoplimit.append(int(sub_wordlist[9].replace("HopLim", "")))
                            channelid.append(int(sub_wordlist[10].replace("Ch", ""), 0))
                            rxtimestampunix.append(int(sub_wordlist[12].replace("rxtime=", "")))
                            # "\" operator indicates that the statement is continued in next line
                            print(rxtimestampunix)
                            print(append_count)
                            rxdatetime.append(datetime.datetime.fromtimestamp\
                                        (rxtimestampunix[append_count], datetime.timezone.utc))
                            rxSNR.append(float(sub_wordlist[13].replace("rxSNR=", "")))
                        if s3:
                            sub_wordlist2 = log_lines[f-f2].replace\
                                            ("(", "").replace(")", "").replace(",", "").split()
                            bw.append(int(sub_wordlist2[3].replace("bw=", "")))
                            sf.append(int(sub_wordlist2[4].replace("sf=", "")))
                            cr.append(sub_wordlist2[5].replace("cr=", "")) 
                            symLen.append(int(sub_wordlist2[7].replace("symLen=", "")))
                            totalpayloadSize.append(int(sub_wordlist2[9].replace("payloadSize=", "")))
                            airtime.append(int(sub_wordlist2[11]))

                # increament append counter to keep count of added data points
                append_count += 1
                
        header = ['Request ID','Rx Time UTC' , 'Rx Timestamp', 'Sender', 'msg',\
             'Total Payload Size (bytes)', 'Air Time (ms)', 'Hop Limit', 'Channel ID',\
                 'Bandwidth (khZ)', 'Spreading Factor', 'Coding Rate', 'symLen (ms)']
        # dt = datetime.datetime.now(pytz.timezone('Europe/Berlin'))    # import pytz for this
        dt = datetime.datetime.now()
        workDir = os.getcwd()
        fpath_write = Path(workDir + "/ProcessedLogs")
        fpath_write.mkdir(exist_ok=True)
        with open(str(fpath_write) + "/SerialData_" + dt.strftime("%Y%m%d_%H%M") + ".csv", mode="w", newline = '\n') as dataFile:
            writer = csv.writer(dataFile)
            writer.writerow(header)
            for wr in range(len(requestid)):
                data_lines.append([requestid[wr], rxdatetime[wr], rxtimestampunix[wr], \
                sender[wr], textmsg[wr], totalpayloadSize[wr], airtime[wr], hoplimit[wr], \
                channelid[wr], bw[wr], sf[wr], cr[wr], symLen[wr]])
            writer.writerows(data_lines)

if __name__ == '__main__':
    app = App()
    app.mainloop()


