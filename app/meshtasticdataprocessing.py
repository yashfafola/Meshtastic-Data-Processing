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
id = []
mode = []
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
        # quit gui
        QuitButton = Button(self, text="Quit", activeforeground='white', activebackground='#46403E', 
                    command=self.destroy)
        QuitButton.place(x=230, y=250)

    def selectFile(self):
        global fpath
        #defaultSys = os.path.dirname(sys.modules['__main__'].__file__)
        # initialdir=defaultSys
        fpath = filedialog.askopenfilenames(title="Select file", 
                filetypes=(("text files", "*.txt"), ("all files", "*.*")))

    def processSerialLogs(self, fpath):
        # open file containing logs
        logFile = open(fpath[0], mode="r")
        rawLogs = logFile.readlines()
        logFile.close()
        print("File length is: " + str(len(rawLogs)) + " lines")
        append_count = 0
        dc = 0
        for f in range(len(rawLogs)):
            log_lines.append(rawLogs[f].replace(",", "", 2))
            pos_msg = rawLogs[f].find("msg=")
            if pos_msg > 65:
                # get the data points from a line
                sub_wordlist = log_lines[f].split()
                #print(sub_wordlist)
                id.append(int(sub_wordlist[1]))
                sender.append(sub_wordlist[6].replace("from=", ""))
                requestid.append(int(sub_wordlist[7].replace("id=", ""), 0))
                #nlist = " ".join([sub_wordlist[x].replace("msg=", "") for x in range(7, len(sub_wordlist), 1)])
                textmsg.append(" ".join([sub_wordlist[x].replace("msg=", "") \
                                for x in range(8, len(sub_wordlist), 1)]))
                
                # get other data points via tracking the same id
                for f2 in range(4):
                    if log_lines[f-f2].find("decoded message") > 0 and \
                    log_lines[f-f2].find(str(id[append_count])):  
                        sub_wordlist2 = log_lines[f-f2].replace("(", "").replace(")", "").split()
                        receiver.append(sub_wordlist2[7])
                        hoplimit.append(int(sub_wordlist2[9].replace("HopLim", "")))
                        channelid.append(int(sub_wordlist2[10].replace("Ch", ""), 0))
                        rxtimestampunix.append(int(sub_wordlist2[12].replace("rxtime=", "")))
                        # "\" operator indicates that the statement is continued in next line
                        rxdatetime.append(datetime.datetime.fromtimestamp\
                                    (rxtimestampunix[append_count], datetime.timezone.utc))
                        rxSNR.append(float(sub_wordlist2[13].replace("rxSNR=", "")))
                    
                for f3 in range(15):
                    if log_lines[f-f3].find("bw=") > 0 and \
                    log_lines[f-f3].find(str(id[append_count])): 
                        sub_wordlist3 = log_lines[f-f3].replace("(", "").replace(")", "").\
                                        replace(",", "").split()  
                        bw.append(int(sub_wordlist3[3].replace("bw=", "")))
                        sf.append(int(sub_wordlist3[4].replace("sf=", "")))
                        cr.append(int(sub_wordlist3[5].replace("cr=", ""))) 
                        symLen.append(sub_wordlist3[7].replace("symLen=", ""))
                        totalpayloadSize.append(int(sub_wordlist3[9].replace("payloadSize=", "")))
                        airtime.append(int(sub_wordlist3[11]))
                    
                append_count += 1
            # elif pos_msg < 65 and pos_msg > 50:
            #     dc += 1       
        print(append_count)
        print(textmsg)
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


