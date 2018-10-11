import random
import json
import socketserver
from JsonParser import parse_json

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
        data = data.decode('utf-8')
        commands = parse_json(data)
        # print("{} wrote:".format(self.client_address[0]), self.data)

        # handle commands
        for command_obj in commands:
            print(command_obj)


class Administrator(object):

    def __init__(self):
        self.admin_option = -1
        self.player_option = -1
        self.face_down_cards = list(range(MIN_POSSIBLE_VALUE, MAX_POSSIBLE_VALUE + 1))
        random.shuffle(self.face_down_cards)

        # Create the server, binding to HOST on port PORT
        self.server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
        print("Admin server has started!")
        print("---------------------------------------")
        self.server.serve_forever()

    def start_game(self):
        self.pick_card()
        self.send_player_message("pick_number_or_card")
        self.set_player_option(int(input()))  # handles players choice
        self.send_player_message("notify_of_verdict", not self.admin_win())
        self.end_game()

    def pick_card(self):
        # self.admin_option = face_down_cards.pop()
        self.admin_option = 8  # TESTING:  Setting values for testing purposes - Random value works as expected.

    def admin_win(self):
        """checks if admin has won (player has lost)."""
        return self.admin_option >= self.player_option

    def set_player_option(self, value):
        if type(value) is not int:
            raise TypeError("Administrator.set_player_option() only excepts one integer argument.")
        elif (value > MAX_POSSIBLE_VALUE or value < MIN_POSSIBLE_VALUE) and value != -1:
            raise ValueError("""Administrator.set_player_option() value argument
            must be between {min} and {max} inclusive, or -1."""
                             .format(min=MIN_POSSIBLE_VALUE, max=MAX_POSSIBLE_VALUE))
        if value == -1:
            self.player_option = self.face_down_cards.pop()
        else:
            self.player_option = value

    @staticmethod
    def send_player_message(operation_name, *args):
        message = {"operation-name": operation_name}
        for i, arg in enumerate(args):
            message["operation-argument{}".format(i+1)] = arg
        print(json.dumps(message))

    def end_game(self):
        """Resets the game state so it can be played again."""
        self.admin_option = -1
        self.player_option = -1
        self.face_down_cards = random.shuffle(list(range(MIN_POSSIBLE_VALUE, MAX_POSSIBLE_VALUE + 1)))
        self.server.shutdown()