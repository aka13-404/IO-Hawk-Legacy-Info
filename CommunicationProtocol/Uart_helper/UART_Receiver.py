import serial
from tkinter import *
from tkinter import ttk

ComPort = ""
SerialBuffer = ""
PacketDecoded = []
RunTransfer = 0

root = Tk()
root.title("IoHawk UART helper")

#Root frame filler
mainframe = ttk.Frame(root, padding=5)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#Com port entry row
com_port_name = ttk.Label(mainframe, text=).grid(sticky=W)


com_port = StringVar()
com_port_entry = ttk.Entry(mainframe, width=2, textvariable=com_port).grid(sticky=W)

#rx bytes
lfrx = ttk.LabelFrame(mainframe, text="Reading RX")

for each in range (0,16):
    Label = str(each)
    ttk.Label(lfrx, text=Label, padding=2).grid(column=each+1, row=1)



for child in mainframe.winfo_children(): 
    child.grid_configure(padx=2, pady=2)


root.mainloop()
"""

with serial.Serial() as ser:
    ser.baudrate = 1200
    ser.port = ComPort
    ser.timeout = 5
    ser.open()
    for i in range(50) :
        SerialBuffer = ser.read(15)
        if SerialBuffer == "":
            quit()
        for each in SerialBuffer:
           PacketDecoded.append(each)
        
        crc = 0
        for each in PacketDecoded[:-1]:
            crc = crc ^ each
        if (crc != PacketDecoded[-1]) and (PacketDecoded[1] != 0x01 or PacketDecoded[1] != 0x36) and crc != 0:
            ser.read(1)
        else:
            print([hex(x) for x in PacketDecoded])
        PacketDecoded.clear()
        """

#    if ReadMode == "DISPLAY":
#        while SerialBuffer != "0103":
#            SerialBuffer = ser.read(2).hex()
#        SerialBuffer = ser.read(13)
#    elif ReadMode == "ESC":
#    while 1:
#        SerialBuffer = ser.read(15).hex()
#        print(SerialBuffer)