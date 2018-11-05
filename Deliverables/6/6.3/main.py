import json
import traceback

from Player import Player
from Referee import Referee
from JsonParser import take_input, parse_json
from CustomExceptions import MalformedCommand, ContractViolation


def main():
    player1 = Player()
    player2 = Player()
    referee = Referee(player1, player2)
    json_values = parse_json(take_input())
    if len(json_values) < 4:
        raise MalformedCommand("Input required to begin with two Name and then two [Placement, Placement] commands.")
    player1_name = json_values.pop()
    print(referee.register_player(player1_name))
    player2_name = json_values.pop()
    print(referee.register_player(player2_name))
    player1_placements = json_values.pop()
    print(referee.check_placements(player1_placements))
    player2_placements = json_values.pop()
    print(referee.check_placements(player2_placements))

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
                placements = player.place(given_board)
                print(json.dumps(placements))
            elif command == "Play":
                plays = player.play(given_board)
                print(json.dumps(plays))
            else:
                raise MalformedCommand("Unrecognized command argument: {}".format(command))
        except ContractViolation:  # unspecified behaviour for invalid input
            pass
        except Exception as e:
            print(json.dumps(str(e)))
            # print(json.dumps(traceback.format_exc()))


if __name__ == "__main__":
    main()
