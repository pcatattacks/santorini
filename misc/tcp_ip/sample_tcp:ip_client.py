import socket
import socketserver
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
    print(data)

# ------------------------ Admin --------------------------- #

MIN_POSSIBLE_VALUE = 1
MAX_POSSIBLE_VALUE = 10
HOST, PORT = "10.105.111.228", 10000


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        data = self.request.recv(1024).strip()
        # data = data.decode('utf-8')
        # commands = parse_json(data)
        print("{} wrote:".format(self.client_address[0]), self.data)

        # handle commands
        for command_obj in commands:
            print(command_obj)


# Create the server, binding to HOST on port PORT
server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
print("Admin server has started!")
print("---------------------------------------")
server.serve_forever()
