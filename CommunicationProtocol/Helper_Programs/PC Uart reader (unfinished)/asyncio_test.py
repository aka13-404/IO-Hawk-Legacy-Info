import asyncio
import serial


port = "COM11"
baudrate = 1200
timeout = 1

serial_buffer = ""
packet_decoded = []
packet_length = 15


async def main():
    serial_open()
    asyncio.create_task(sender())
    asyncio.create_task(receiver())
    while True:
        await asyncio.sleep(1)


def serial_open():
    global uart
    try:
        uart = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
    except Exception as e:
        print(e)


async def sender():
    swriter = asyncio.StreamWriter(uart)
    while True:
        print("Test")
        await asyncio.sleep(2)


async def receiver():
    sreader = asyncio.StreamReader(uart)
    while True:
        res = await sreader.readline()
        print('Received', res)


if __name__ == "__main__":
    asyncio.run(main())