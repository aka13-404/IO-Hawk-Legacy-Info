import uasyncio as asyncio
from machine import UART
import gc

uart1 = UART(2, tx=32, rx=33)
uart1.init(baudrate=1200, bits=8, parity=None, stop=1, timeout=0)

packet_from_display = []
packet_to_display = [0x36, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

enc_key_list = [
    0x5e, 0x23, 0x5c, 0x21, 0x2a, 0x2f, 0x28, 0x2d, 0x26, 0x2b, 0x24, 0x29, 0x52, 0x57, 0x50, 0x55,
    0x4e, 0x53, 0x4c, 0x51, 0x5a, 0x5f, 0x58, 0x5d, 0x56, 0x5b, 0x54, 0x59, 0x02, 0x07, 0x00, 0x05,
    0x3e, 0x03, 0x3c, 0x01, 0x0a, 0x0f, 0x08, 0x0d, 0x06, 0x0b, 0x04, 0x09, 0x32, 0x37, 0x30, 0x35,
    0x2e, 0x33, 0x2c, 0x31, 0x3a, 0x3f, 0x38, 0x3d, 0x36, 0x3b, 0x34, 0x39, 0x62, 0x67, 0x60, 0x65,
    0x1e, 0x63, 0x1c, 0x61, 0x6a, 0x6f, 0x68, 0x6d, 0x66, 0x6b, 0x64, 0x69, 0x12, 0x17, 0x10, 0x15,
    0x0e, 0x13, 0x0c, 0x11, 0x1a, 0x1f, 0x18, 0x1d, 0x16, 0x1b, 0x14, 0x19, 0x42, 0x47, 0x40, 0x45,
    0x7e, 0x43, 0x7c, 0x41, 0x4a, 0x4f, 0x48, 0x4d, 0x46, 0x4b, 0x44, 0x49, 0x72, 0x77, 0x70, 0x75,
    0x6e, 0x73, 0x6c, 0x71, 0x7a, 0x7f, 0x78, 0x7d, 0x76, 0x7b, 0x74, 0x79, 0x22, 0x27, 0x20, 0x25]



async def receiver():
    global packet_from_display
    sreader = asyncio.StreamReader(uart1)
    while True:
        received_byte = await sreader.readexactly(15)
        for each in received_byte:
            packet_from_display.append(each)
        crc = 0
        for each in packet_from_display[:-1]:
            crc = crc ^ each
        if (crc == packet_from_display[-1]) and (crc != 0) and ((packet_from_display[0] == 0x01) or (packet_from_display[0] == 0x36)):
            pass
            # print(packet_from_display) #add some processing of data from screen
        else:
            await sreader.readexactly(1)
        packet_from_display.clear()


async def sender():
    global packet_to_display
    swriter = asyncio.StreamWriter(uart1, {})
    while True:

        # counter in Byte 1
        if packet_to_display[1] < 255:
            packet_to_display[1] += 1
        else:
            packet_to_display[1] = 0

        # Byte 3
        if False:
            packet_to_display[3] = 0b00000000

        # Byte 4
        if False:
            packet_to_display[4] = 0b00000000

        # Byte 5
        if False:
            packet_to_display[5] = 0b00000000

        # Byte 7-8, Speed
        # Speed tester
        if False:  # false to disable test
            speed_tester = 0  # var for speed test
            if False:  # false to disable automated test
                if speed_tester < 2950:
                    speed_tester += 15
                else:
                    speed_tester = 0
                speed_tester_b = speed_tester.to_bytes(2, "big")
                packet_to_display[7] = speed_tester_b[0]
                packet_to_display[8] = speed_tester_b[1]
            else:
                packet_to_display[8] = 200

        # Byte 9-10, Current
        if False:
            packet_to_display[9] = 0b11111111
            packet_to_display[10] = 0b11111111

        # Byte 11
        if False:
            packet_to_display[11] = 0b00000000

        # Byte 12
        if False:
            packet_to_display[12] = 0b00000000

        # Byte 13
        if False:
            packet_to_display[13] = 0b00000000

        # encoding
        # get encoding key from table mined from data dumps
        if packet_to_display[1] < 128:
            enc_key = enc_key_list[packet_to_display[1]]
        else:
            enc_key = enc_key_list[packet_to_display[1] - 128]
        # create local encoded packet
        packet_to_display_enc = packet_to_display.copy()
        # apply key to encoded values
        for each in [3, 4, 5, 7, 8, 9, 10, 11, 12, 13]:
            packet_to_display_enc[each] += enc_key
            packet_to_display_enc[each] = packet_to_display_enc[each] % 256  # we only have 1 byte, so remove everything over 255

        # crc on the encoded packet
        crc = 0
        for each in packet_to_display_enc[:-1]:
            crc = crc ^ each
        packet_to_display_enc[14] = crc

        #print(packet_to_display)
        swriter.write(bytes(packet_to_display_enc))
        await swriter.drain()
        gc.collect()
        await asyncio.sleep_ms(450)



loop = asyncio.get_event_loop()
asyncio.create_task(receiver())
asyncio.create_task(sender())
loop.run_forever()
