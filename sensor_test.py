from threading import Thread
import serial
import os

def open_serial(port, baudrate=115200):
    ser = serial.Serial()
    ser.baudrate = baudrate
    ser.port = port
    ser.open()
    return ser

def read_data(ser):
    ser.write(str.encode("\n"))
    txt_array = ser.readline().decode("utf-8").strip().split(",")
    if len(txt_array) < 6:
        return None, None
    distance1 = txt_array[1]
    distance2 = txt_array[4]
    if txt_array[2] in ['2', '4', '7']:
        distance1 = 2000
    if txt_array[5] in ['2', '4', '7']:
        distance2 = 2000
    return distance1, distance2

def close_serial(ser):
    ser.close()

def collect_data(arduino_board_port, arduino_board_number, collect_data):
    ser = open_serial(arduino_board_port)
    while True:
        distance1, distance2 = read_data(ser)
        if distance1 is not None and distance2 is not None:
            if arduino_board_number == 0: 
                #print(f"Arduino board number: {arduino_board_number}\n")
                print(f"C1: {distance1},A1: {distance2}\n")
            #if arduino_board_number == 1: 
                #print(f"Arduino board number: {arduino_board_number}\n")
                #print(f"A2: {distance1},C2: {distance2}\n")
            #if arduino_board_number == 2: 
                #print(f"Arduino board number: {arduino_board_number}\n")
                #print(f"D2: {distance1},B2: {distance2}\n")
            #if arduino_board_number == 3: 
                #print(f"Arduino board number: {arduino_board_number}\n")
                #print(f"D1: {distance1},B1: {distance2}\n")
    close_serial(ser)

def main():
    ARDUINO_BOARD_PORT_ARRAY = ["COM3", "COM4", "COM5", "COM6"]
    collect_data_flag = True
    threads = []
    for i, port in enumerate(ARDUINO_BOARD_PORT_ARRAY):
        thread = Thread(target=collect_data, args=[port, i, collect_data_flag])
        thread.start()
        threads.append(thread)
    # Do other stuff
    # When done, stop the threads
    collect_data_flag = False
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()