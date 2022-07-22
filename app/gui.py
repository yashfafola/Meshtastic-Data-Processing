import tkinter
from tkinter import filedialog
from tkinter import *

# root = tkinter.Tk()
# root.geometry('500x500')
# root.title('Data Processing')
# frame1 = Frame(root, bg="white")
# frame1.pack(expand=True, fill=BOTH)
# SerialLogsButton = Button(frame1, text="Serial Logs", command=openFile)
# SerialLogsButton.place(x=25, y=100)
# root.mainloop()

# greeting = tkinter.Label(text="Hello, Tkinter")
# greeting.pack()
#root.withdraw()
# serial_log_file_path = filedialog.askopenfilename()
#print(file_path)
fpath = None

class App(tkinter.Tk):
    def __init__( self ):
        super().__init__()

        # Configure the root window
        self.title("Data Processing")
        self.geometry('500x300')

        # Buttons
        SerialLogsButton = Button(self, text="Serial Logs", activeforeground='white', activebackground='#46403E', command=self.openFile)
        SerialLogsButton.place(x=25, y=100)
#         SerialLogsButton = Button(self, text = "Serial Logs", command = self.openFile())
#         SerialLogsButton.place(x=80, y=100)
    
    def openFile(self):
        global fpath
        fpath = filedialog.askopenfilenames(title="Select file", 
                filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        print(fpath)    

# def main():
#     mainWindow().mainloop()
if __name__ == '__main__':
    app = App()
    app.mainloop()