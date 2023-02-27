from pathlib import PurePath
#from openpyxl import Workbook


FileToConvert = PurePath(__file__).parent / "dump.txt"
FileOutput = PurePath(__file__).parent / "ConvertedDump.txt"
BytesToSkip = 0
FrameSize = 0
OutputBuffer = []
LineBuffer = []

BytesToSkip = input("Bytes to skip: ")
try:
    BytesToSkip = int(BytesToSkip)
    print("Skipping " + str(BytesToSkip) + " bytes")
except:
    BytesToSkip = 0
    print("Iput error, not skipping any bytes")

FrameSize = input("Frame size (default 15): ")
if FrameSize == '':
    print("Frame size set to 15")
    FrameSize = 15
else:
    try:
        FrameSize = int(FrameSize)
        print("Frame size set to " + str(FrameSize))
    except:
        FrameSize = 15
        print("Iput error, frame size set to 15")
    
#Clear file contents
with open (FileOutput, "w") as ConvFile:
    ConvFile.write('')

with open (FileToConvert, "r") as File:
    for Line in File:
        LineBuffer.extend(Line.split())
        while LineBuffer != []:
            while (BytesToSkip != 0) and (LineBuffer != []):
                LineBuffer == LineBuffer.pop(0)
                BytesToSkip -= 1
            while (len(OutputBuffer) < FrameSize) and (LineBuffer != []):
                OutputBuffer.append(LineBuffer[0])
                LineBuffer == LineBuffer.pop(0)
            if len(OutputBuffer) == FrameSize:
                with open (FileOutput, "a") as ConvFile:
                    for each in OutputBuffer:
                        ConvFile.write(str(each).zfill(2) + "\t")                 
                    ConvFile.write("\n")
                    for each in OutputBuffer:
                        ConvFile.write(str(bin(int(each, 16)))[2:].zfill(8) + "\t")
                    ConvFile.write("\n")
                OutputBuffer=[]