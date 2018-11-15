import json
import socketserver
from threading import Thread, enumerate
from Player import Player
from RuleChecker import RuleChecker
from CustomExceptions import InvalidCommand, ContractViolation, IllegalPlay
from JsonParser import parse_json
import time


def is_valid_register_command(command):
    """

    :param any command:
    :return: `True` if command is `["Register"]`, `False` otherwise
    :rtype: bool
    """
    return command == ["Register"]


def is_valid_place_command(command):
    """
    Definitions:

    color
        either "blue" or "white"

    initial-board:
        Initial-Board is a valid Board as described in the documentation of `Board` but without any buildings and
        without workers of `color` or without any workers at all.

    :param any command:
    :return: `True` if command is `["Place", color, initial-board]`, `False` otherwise.
    :rtype: bool
    """
    return (isinstance(command, list) and len(command) == 3
            and command[0] == "Place" and command[1] in RuleChecker.COLORS
            and RuleChecker.is_valid_board(command[2]))
    # TODO: might have to do is_legal_board check here too, since InvalidCommand and IllegalPlay may both result in
    # "Santorini is Broken". Discuss.


def is_valid_play_command(command):
    """
    Definitions:

    board:
        Board is a valid Board as described in  as described in the documentation of `Board` but with the
        extra restriction that there can be no workers at levels 3 and 4.

    :param any command:
    :return: `True` if command is `["Play", board]`
    :rtype: bool
    """
    return (isinstance(command, list)
            and len(command) == 2 and command[0] == "Play" and RuleChecker.is_valid_board(command[1]))
    # TODO: might have to do is_legal_board check here too, since InvalidCommand and IllegalPlay may both result in
    # "Santorini is Broken". Discuss


def is_valid_game_over_command(command):
    """
    Definitions:

    Name
        a string denoting the name of a player

    :param any command:
    :return: `True` if command is `["Game Over", Name]`
    :rtype: bool
    """
    return isinstance(command, list) and len(command) == 2 and command[0] == "Game Over" and isinstance(command[1], str)


class PlayerDriverRequestHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        data = self.request.recv(4096).strip()
        data = data.decode('utf-8')
        # print("player driver received: ", data)  # debug
        # print("--------------------------------")  # debug
        json_values = parse_json(data)  # TODO: should only be one element array - what behaviour when not?
        try:
            for json_val in json_values:
                command = json_val["value"]
                if is_valid_register_command(command):
                    name = player.register()  # should raise error since player is already registered
                    self._send_response(name)
                elif is_valid_place_command(command):
                    color, board_list = command[1:]
                    placements = player.place(board_list, color)
                    self._send_response(placements)
                elif is_valid_play_command(command):
                    board_list = command[1]
                    plays = player.play(board_list)
                    self._send_response(plays)
                elif is_valid_game_over_command(command):
                    name = command[1]
                    acknowledgement = player.notify(name)
                    self._send_response(acknowledgement)
                    self._cleanup()

                else:
                    raise InvalidCommand("Invalid command passed to Player! Given:".format(command))

        except InvalidCommand as e:
            self._send_response("InvalidCommand")
        except IllegalPlay as e:
            self._send_response("IllegalPlay")
        except ContractViolation as e:
            self._send_response("ContractViolation")

    def _send_response(self, message):
        data = bytes(json.dumps(message) + "\n", "utf-8")
        self.request.sendall(data)

    def _cleanup(self):
        # stopping the loop. must be called from different thread or will deadlock.
        thread = Thread(target=release_resources, args=(self.server, ))
        thread.start()


def release_resources(server):
    """
    :param socketserver.BaseServer server:
    :return:
    """
    server.shutdown()
    server.server_close()


with open("strategy.config", "r") as f:
    num_looks_ahead = parse_json(f.read())[0]["value"]["look-ahead"]
    player = Player("P1", num_looks_ahead=num_looks_ahead)

HOST, PORT = "localhost", 9999


def main():

    # Create the server, binding to HOST on port PORT
    server = socketserver.TCPServer((HOST, PORT), PlayerDriverRequestHandler)

    # print("Player Driver Server is starting...")
    try:
        server.serve_forever()
        # TODO: Implement a timeout for the real game
    except Exception:
        thread = Thread(target=release_resources, args=(server,))
        thread.start()


if __name__ == "__main__":
    main()
