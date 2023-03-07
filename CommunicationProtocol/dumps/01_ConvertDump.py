from pathlib import PurePath
#from openpyxl import Workbook


FileToConvert = PurePath(__file__).parent / "dump.txt"
FileOutput = PurePath(__file__).parent / "ConvertedDump.txt"
BytesToSkip = 0
FrameSize = 15
OutputBuffer = []
LineBuffer = []
DecryptEscData = 0

BytesToSkip = input("Bytes to skip: ")
if BytesToSkip == '':
    print("Not skipping any bytes")
    BytesToSkip = 0
else:
    try:
        BytesToSkip = int(BytesToSkip)
        print("Skipping " + str(BytesToSkip) + " bytes")
    except:
        BytesToSkip = 0
        print("Iput error, not skipping any bytes")

DecryptEscData = input("Dump from ESC, decode? (y/N): ")
if DecryptEscData == 'y':
    print("Bytes 3, 4, 5, 7, 8, 9, 10, 11, 12 will be decoded")
    DecryptEscData = 1
else: 
    print("No decoding will be performed")
    DecryptEscData = 0




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
                if DecryptEscData == 1:
                    OutputBuffer = [int(each, 16) for each in OutputBuffer] #convert to hex int
                    for each in [3, 4, 5, 7, 8, 9, 10, 11, 12]:
                        OutputBuffer[each] -= OutputBuffer[13] #Substract byte 13 from encoded bytes
                        OutputBuffer[each] = OutputBuffer[each] % 256 #we only have 1 byte, so remove everything over 255
                    OutputBuffer = [str(hex(each)[2:]) for each in OutputBuffer] #rewrite to hex form for printing to file
                with open (FileOutput, "a") as ConvFile:
                    for each in OutputBuffer:
                        ConvFile.write(each.upper().zfill(2) + "\t")                 
                    ConvFile.write("\n")
                    for each in OutputBuffer:
                        ConvFile.write(str(bin(int(each, 16)))[2:].zfill(8) + "\t")
                    ConvFile.write("\n")
                OutputBuffer=[]