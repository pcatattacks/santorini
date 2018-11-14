import socket
import json
from RuleChecker import RuleChecker
from PlayerInterface import PlayerInterface
from CustomExceptions import ContractViolation, IllegalResponse, InvalidCommand, IllegalPlay
from JsonParser import parse_json


class ProxyPlayer(PlayerInterface):  # TODO: change docstrings and implement interaction protocol contract

    def __init__(self, host, port):
        # TODO: contract checks for host and port
        self.host = host
        self.port = port
        # self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket.connect((self.host, self.port))

    def register(self):
        """
        Returns the name of the player.

        CONTRACT:
         - Must be the first function to be called after Player is instantiated.
         - Cannot be called more than once.

        :return: the name of the player
        :rtype: string
        """
        # print("player.register() called.")  # debug
        # TODO: contract checks
        message = ["Register"]
        response = self._send_message_and_recv_response(message)
        self._examine_for_error(response)
        if not isinstance(response, str):  # checking if is_valid_name. Potentially create well named micro-function?
            # self.socket.close()
            raise IllegalResponse("ProxyPlayer didn't receive string for name. Received: {}".format(response))
        return response

    def place(self, board, color):
        """
        Sets the `color` member variable to the parameter `color`. Returns the worker placements for the player.

        CONTRACT:
         - Can only be called after Player.register() has been called.
         - Must be called before Player.play().
         - Cannot be called more than once.
         - `board` must be a valid initial board (a board where all cell's heights are 0, and no workers of `self.color`
         are present any cell.

        :param list board: an instance of Board (refer to documentation of Board class).
        :param string color: a color (as defined above)
        :return: `list` of [position1, position2] denoting the position of the player's 1st and 2nd worker respectively.
        See `position`, `worker` in documentation of Board.py.
        :rtype: list
        """
        # print("player.place() called.")  # debug
        message = ["Place", color, board]
        response = self._send_message_and_recv_response(message)
        self._examine_for_error(response)
        if not RuleChecker.is_valid_placement(response):
            # self.socket.close()
            raise IllegalResponse("ProxyPlayer didn't receive correctly formatted placement. Received {}"
                                  .format(response))
        return response

    def play(self, board):
        """
        Returns the play a player wants to execute on a given turn.

        :param list board:
        :return: a play (as defined above)
        :rtype: list
        """
        # print("player.play() called.")  # debug
        message = ["Play", board]
        response = self._send_message_and_recv_response(message)
        self._examine_for_error(response)
        if not isinstance(response, list) or not all(RuleChecker.is_valid_play(play) for play in response):
            # self.socket.close()
            raise IllegalResponse("ProxyPlayer didn't receive correctly formatted play. Received {}"
                                  .format(response))
        return response

    def notify(self, winner_name):
        """
        Notifies the player with the winner of the Santorini game.

        CONTRACT:
         - can only be called once per game
         - must be the last function to be called by an object that implements PlayerInterface.

        :param string winner_name: Name of the winner of the Santorini game
        :return: An acknowledgement string of "OK"
        :rtype: string
        """
        # print("player.notify() called.")  # debug
        message = ["Game Over", winner_name]
        response = self._send_message_and_recv_response(message)
        self._examine_for_error(response)
        # self.socket.close()
        if not response == "OK":
            raise IllegalResponse('ProxyPlayer didn\'t receive correctly formatted "OK". Received {}'
                                  .format(response))
        return response

    def _send_message_and_recv_response(self, message):
        """

        :param any message: an object that can be converted to json via json.dumps() .
        :return: an object that can be converted to json via json.dumps()
        :rtype: any
        """
        data = bytes(json.dumps(message) + "\n", "utf-8")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        sock.sendall(data)
        response = str(sock.recv(4096), "utf-8")  # Receive data from the server
        sock.close()
        # self.socket.sendall(data)
        # response = str(self.socket.recv(4096), "utf-8")  # Receive data from the server
        # print("response is", response)  # debug
        if not response:
            raise IllegalResponse("Response was empty!")
        response = parse_json(response)[0]["value"]
        return response

    @staticmethod
    def _examine_for_error(response):
        if response == "InvalidCommand":
            raise InvalidCommand()
        if response == "IllegalPlay":
            raise IllegalPlay()
        if response == "ContractViolation":
            raise ContractViolation()
