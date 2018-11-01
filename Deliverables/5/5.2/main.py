import json

from Player import Player
from JsonParser import take_input, parse_json
from CustomExceptions import MalformedCommand


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

            if command == "Place":
                player.register(color)
                placements = player.place(given_board)
                print(json.dumps(placements))
            elif command == "Play":
                plays = player.play(given_board)
                print(json.dumps(plays))
            else:
                raise MalformedCommand("Unrecognized command argument: {}".format(command))

        except Exception as e:  # TODO: add a separate `except` statement for ContractViolation, so we do nothing for
            #  violated contracts since behaviour is unspecified
            print(json.dumps(str(e)))


if __name__ == "__main__":
    main()
