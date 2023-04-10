packet = "36 1D 00 07 07 07 00 07 24 07 07 07 07 07 36"
packet = packet.split()
packet = [int(str(each), 16) for each in packet]
print(bytes(packet).hex("_",1))
print(bytes(packet[:-1]).hex("_",1))
print("crc")
crc = 0
for each in packet[:-1]:
    crc ^= each
print(hex(crc))