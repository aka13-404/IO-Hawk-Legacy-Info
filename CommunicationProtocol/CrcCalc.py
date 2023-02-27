import numpy
Packet = "36	13	00	51	51	52	00	51	51	51	51	51	51	51	26"
print(Packet)
Packet = Packet.split()
Packet.pop(-1)
Packet = [int(str(each), 16) for each in Packet]
print("crc")
print(hex(numpy.bitwise_xor.reduce(Packet)))