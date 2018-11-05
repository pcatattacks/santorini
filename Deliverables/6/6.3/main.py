import json
import traceback

from Player import Player
from Referee import Referee
from JsonParser import take_input, parse_json
from CustomExceptions import ContractViolation, InvalidInput, InvalidCommand, MalformedCommand


def main():
    player1 = Player()
    player2 = Player()
    referee = Referee(player1, player2)
    json_values = parse_json(take_input())
    if len(json_values) < 4:
        raise InvalidInput("Input required to begin with two Name and then two [Placement, Placement] commands.")
    for json_val in json_values:
        val = json_val["value"]
        try:
            if isinstance(val, str):
                print(json.dumps(referee.register_player(val)))
            elif not isinstance(val, list) or not val:
                raise MalformedCommand\
                    ("Incorrect JSON value. Expected non-empty JSON list, given {}".format(type(val)))
            elif isinstance(val[0], list):
                print(json.dumps(referee.check_placements(val)))
            elif isinstance(val[0], str):
                print(json.dumps(referee.check_play(val)))
            else:
                raise MalformedCommand("Unrecognized command: {}".format(val))
        except (ContractViolation, InvalidCommand):  # unspecified behaviour for invalid input
            pass
        except Exception as e:
            print(json.dumps(str(e)))
            # print(json.dumps(traceback.format_exc()))


if __name__ == "__main__":
    main()