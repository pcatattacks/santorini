import json

from Board import Board
from RuleChecker import RuleChecker
from Player import Player
from JsonParser import take_input, parse_json


class MalformedCommand(Exception):
    pass


def main():
    player = Player()
    json_values = parse_json(take_input())
    for val in json_values:
        try:
            if not isinstance(val, list):
                raise MalformedCommand("Incorrect JSON value. Expected JSON list, given {}".format(type(val)))
            if len(val) == 3:
                command, color, given_board = val
            elif len(val) == 2:
                command, given_board = val
            else:
                raise MalformedCommand("Invalid number of arguments in JSON list.")

            # TODO: add validity checks for board. Different checks for boards given for the 'place' and 'play' command.
            if command == "Place":
                pass
            elif command == "Play":
                pass
            else:
                raise MalformedCommand("Unrecognized command argument: {}".format(command))

        except Exception as e:
            print(json.dumps(str(e)))


if __name__ == "__main__":
    main()
