import socket
import sys
import json


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = "10.105.111.228"
    #host="localhost"
    port = 10000
    s.connect((host, port))
    val = '{"operation-name":\n "pick_number_or_card"}'
    test = bytearray( val.encode('utf-8'))
    s.sendall(test)

    data = s.recv(1024)
    print (data)
