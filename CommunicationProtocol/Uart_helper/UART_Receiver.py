import serial
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

Port = "COM11"
SerialBuffer = ""
PacketDecoded = []
RunTransfer = 0
PacketLength = 15

running = False

def StartSerial():
    global running
    global ser
    try:
        ser = serial.Serial(PortEntry.get(), 1200, timeout=1)
        StopSerialButton.config(state=NORMAL)
        StartSerialButton.config(state=DISABLED)
        running = True
    except:
        messagebox.showerror(message="Wrong port or already in use by other program")
        

def StopSerial():
    global running
    global ser
    try:
        ser.close()
        StopSerialButton.config(state=DISABLED)
        StartSerialButton.config(state=NORMAL)
    except:
        messagebox.showerror(message="Could not close serial port")
    running = False

def MainLoopFunction():
    global running
    if running:
        SerialBuffer = ser.read(15)
        if SerialBuffer != "":
            for each in SerialBuffer:
               PacketDecoded.append(each)
            crc = 0
            for each in PacketDecoded[:-1]:
                crc = crc ^ each
            if crc == PacketDecoded[-1] and crc != 0 and ((PacketDecoded[0] == 0x01) or (PacketDecoded[0] == 0x36)):
                for position, each in enumerate(PacketDecoded):
                    ByteGUI[position][1].delete(0, END)
                    ByteGUI[position][1].insert(0, str(hex(each)[2:]).zfill(2).upper())
                    ByteGUI[position][2].delete(0, END)
                    ByteGUI[position][2].insert(0, str(bin(each))[2:].zfill(8).upper())
            else:
                ser.read(1)
            PacketDecoded.clear()
        else:
            running = False
            messagebox.showerror(message="No data received from port")
    root.after(50, MainLoopFunction)




############################################################################################
#Tkinter GUI

root = Tk()
root.title("IoHawk UART helper")

#Root frame filler
mainframe = ttk.Frame(root, padding=5)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

####Port entry row
#Port label
PortName = ttk.Label(mainframe, text="COM Port:")
PortName.grid(sticky=E, row=1, column=1)

#Com port entry field
PortEntry = ttk.Entry(mainframe, width=8)
PortEntry.grid( row=1, column=2)
PortEntry.insert(0, Port)

#Start reading button
StartSerialButton = ttk.Button(mainframe, text="Start", command=StartSerial)
StartSerialButton.grid(row=1, column=3, columnspan=1)

#Stop reading button
StopSerialButton = ttk.Button(mainframe, text="Stop", command=StopSerial, state=DISABLED)
StopSerialButton.grid(row=1, column=4, columnspan=1)

### RX OUTPUT
#Main Label
UartRX_name = ttk.Label(mainframe, text="UART RX", justify=CENTER)
UartRX_name.grid(row=2, column=1, columnspan=PacketLength)
#Byte Labels and Entries
ByteGUI = []

for each in range(PacketLength):
    ByteGUI.append([ttk.Label(mainframe, text="Byte " + str(each)), None, None]) # add first label and placeholders for other labels/entriues
    ByteGUI[each][0].grid(row=3, column=each+1, padx=10, pady=2)
    ByteGUI[each][1] = ttk.Entry(mainframe, justify=CENTER, width=4) # Fields for RX in hex
    ByteGUI[each][1].grid(row=4, column=each+1)
    ByteGUI[each][2] = ttk.Entry(mainframe, justify=CENTER, width=8) # fields for RX in byte
    ByteGUI[each][2].grid(row=5, column=each+1, padx=10, pady=2)

root.after(500, MainLoopFunction)
root.mainloop()

#Tkinter GUI End
############################################################################################