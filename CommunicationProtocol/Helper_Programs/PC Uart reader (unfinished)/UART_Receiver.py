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


def startserial():
    global running
    global ser
    try:
        ser = serial.Serial(PortEntry.get(), 1200, timeout=1)
        StopSerialButton.config(state=NORMAL)
        StartSerialButton.config(state=DISABLED)
        running = True
    except:
        messagebox.showerror(message="Wrong port or already in use by other program")
        

def stopserial():
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
                if PacketDecoded[0] == 0x36:
                    for each in [3, 4, 5, 7, 8, 9, 10, 11, 12]:
                        PacketDecoded[each] -= PacketDecoded[13]  # Subtract byte 13 from encoded bytes
                        PacketDecoded[each] = PacketDecoded[each] % 256  # only have 1 byte, so remove over 255
                for position, each in enumerate(PacketDecoded):
                    ByteGUI_RX[position][1].delete(0, END)
                    ByteGUI_RX[position][1].insert(0, str(hex(each)[2:]).zfill(2).upper())
                    ByteGUI_RX[position][2].delete(0, END)
                    ByteGUI_RX[position][2].insert(0, str(bin(each))[2:].zfill(8).upper())
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
StartSerialButton = ttk.Button(mainframe, text="Start", command=startserial)
StartSerialButton.grid(row=1, column=3, columnspan=1)

#Stop reading button
StopSerialButton = ttk.Button(mainframe, text="Stop", command=stopserial, state=DISABLED)
StopSerialButton.grid(row=1, column=4, columnspan=1)

### RX OUTPUT
#Main Label
UartRX_name = ttk.Label(mainframe, text="UART RX", justify=CENTER)
UartRX_name.grid(row=2, column=1, columnspan=PacketLength)
#Byte Labels and Entries
ByteGUI_RX = []

for each in range(PacketLength):
    ByteGUI_RX.append([ttk.Label(mainframe, text="Byte " + str(each)), None, None]) # add first label and placeholders for other labels/entriues
    ByteGUI_RX[each][0].grid(row=3, column=each+1, padx=10, pady=2)
    ByteGUI_RX[each][1] = ttk.Entry(mainframe, justify=CENTER, width=4) # Fields for RX in hex
    ByteGUI_RX[each][1].grid(row=4, column=each+1)
    ByteGUI_RX[each][2] = ttk.Entry(mainframe, justify=CENTER, width=8) # fields for RX in byte
    ByteGUI_RX[each][2].grid(row=5, column=each+1, padx=10, pady=2)

### TX INPUT
UartTX_name = ttk.Label(mainframe, text="UART TX", justify=CENTER)
UartTX_name.grid(row=6, column=1, columnspan=PacketLength)

ByteGUI_TX =[]

for each in range(PacketLength):
    ByteGUI_TX.append([ttk.Label(mainframe, text="Byte " + str(each)), None, None]) # add first label and placeholders for other labels/entriues
    ByteGUI_TX[each][0].grid(row=7, column=each+1, padx=10, pady=2)
    ByteGUI_TX[each][1] = ttk.Entry(mainframe, justify=CENTER, width=4) # Fields for RX in hex
    ByteGUI_TX[each][1].grid(row=8, column=each+1)
    ByteGUI_TX[each][2] = ttk.Entry(mainframe, justify=CENTER, width=8) # fields for RX in byte
    ByteGUI_TX[each][2].grid(row=9, column=each+1, padx=10, pady=2)



root.after(500, MainLoopFunction)
root.mainloop()

#Tkinter GUI End
############################################################################################