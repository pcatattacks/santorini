import json
import traceback

from Player import Player
from JsonParser import take_input, parse_json
from CustomExceptions import MalformedCommand, ContractViolation


def main():
    player = Player()
    json_values = parse_json(take_input())
    with open("strategy.config") as f:
        data = f.read() + '\n'
        num_moves_ahead = parse_json(data)[0]["value"]["look-ahead"]

    for json_val in json_values:
        val = json_val["value"]
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
                placements = player.place(given_board) # TODO - check the place function
                print(json.dumps(placements))
            elif command == "Play":
                plays = player.play(given_board, num_moves_ahead)
                print(json.dumps(plays))
            else:
                raise MalformedCommand("Unrecognized command argument: {}".format(command))
        except ContractViolation:  # unspecified behaviour for invalid input
            pass
        except Exception as e:
            # print(json.dumps(str(e)))
            # print(json.dumps(traceback.format_exc()))
            print(traceback.format_exc())


if __name__ == "__main__":
    main()