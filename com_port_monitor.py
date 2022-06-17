import serial
import pandas as pd
import numpy as np
import math
from math import cos, sin, sqrt, pow, atan2, fmod, atan
import schedule
import time
import csv


serial_port = 'com4'
baud_rate = 9600
write_to_file_path = 'LOG00194.csv'


def read_from_serial():
    try:
        ser = serial.Serial(serial_port, baud_rate)
    except Exception() and serial.serialutil.SerialException:
        print("Ошибка чтения COM - порта.")
        return

    while True:
        line = ser.readline()
        line = line.decode("utf-8")
        line.strip()
        print("------------------------------------------------------------------")
        if line:
            line.replace('\n', '')
            print("Полученная строка: ", line, end='')
            break
    if line[0] != '!':
        print('Не подошла((')
        return
    line = line[1:]
    try:
        with open("LOG00194.csv", mode="a", encoding='utf-8') as w_file:
            print('Поехали записывать')
            data = line.split(',')
            file_writer = csv.writer(w_file, delimiter=",", lineterminator=" \r")
            file_writer.writerow(data)
            w_file.close()
    except Exception() as e:
        print("Ошибка записи.")
        return


def send_data_for_rotation():
    my_raw_latitude = 56.91988
    my_raw_longtitude = 39.00347

    try:
        df = pd.read_csv('LOG00194.csv')
        print(df)
    except Exception():
        print("Ошибка считывания файла. Проверье csv - файл.")
    if df.empty:
        return
    sat_raw_latitude = np.longdouble(df['lattitude'].iloc[-1])
    sat_raw_longtitude = np.longdouble(df['longitude'].iloc[-1])
    sat_height = np.longdouble(df['altitude_GPS'].iloc[-1])
    height_above_the_sea = 170.0
    sat_height -= height_above_the_sea

    k = np.longdouble(math.pi / 180.0)
    earth_radius = np.longdouble(6371.0)

    lat1 = my_raw_latitude * k
    lat2 = sat_raw_latitude * k
    long1 = my_raw_longtitude * k
    long2 = sat_raw_longtitude * k

    cl1 = cos(lat1)
    cl2 = cos(lat2)
    sl1 = sin(lat1)
    sl2 = sin(lat2)

    delta = long2 - long1
    cdelta = cos(delta)
    sdelta = sin(delta)

    y = sqrt(pow(cl2 * sdelta, 2) + pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
    x = sl1 * sl2 + cl1 * cl2 * cdelta
    ad = atan2(y, x)
    dist = ad * 6372795

    y1 = sin(sat_raw_longtitude - my_raw_longtitude) * cos(sat_raw_latitude)
    x1 = cos(my_raw_latitude) * sin(sat_raw_latitude) - sin(my_raw_latitude) * cos(sat_raw_latitude) * \
         cos(sat_raw_longtitude - my_raw_longtitude)
    ang = atan2(y1, x1)
    brng = fmod((ang * 180 / math.pi + 360), 360)
    first = (sat_height * cos(sat_raw_longtitude - my_raw_longtitude) * cos(my_raw_latitude) - earth_radius)
    second = sqrt(pow((sat_height * sin(sat_raw_longtitude - my_raw_longtitude)), 2) + pow(
        (sat_height * cos(sat_raw_longtitude - my_raw_longtitude) * sin(my_raw_latitude)), 2))

    place_angle = atan(first / second)
    place_angle = atan(sat_height / dist) * 57.3

    print("Азимут: ", brng)
    print("Угол места: ", place_angle)
    print("------------------------------------------------------------------")

    try:
        ser = serial.Serial(serial_port, baud_rate)
        ser.write(f"W{brng}!{place_angle}".encode())
    except Exception() and serial.serialutil.SerialException:
        print("Ошибка записи COM - порта.")
        return


schedule.every(10).seconds.do(read_from_serial)
schedule.every(10).seconds.do(send_data_for_rotation)

while True:
    schedule.run_pending()
    time.sleep(1)
