import socket
import time

import dht
from machine import Pin


def run_slave(master_ip):
    UDP_PORT = 5005
    sensor = dht.DHT22(Pin(4))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            sensor.measure()
            humidity = sensor.humidity()
            msg = str(humidity).encode()
            sock.sendto(msg, (master_ip, UDP_PORT))
            print("Sent humidity:", humidity)
        except Exception as e:
            print("Sensor error:", e)
        time.sleep(5)
