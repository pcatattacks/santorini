import json
from ProxyPlayer import ProxyPlayer
from JsonParser import parse_json, take_input
from CustomExceptions import InvalidCommand, ContractViolation, IllegalPlay
from player_driver import is_valid_register_command,\
    is_valid_place_command, is_valid_play_command, is_valid_game_over_command


def main():

    with open("strategy.config") as f:
        # TODO: may need /n appended to data
        data = parse_json(f.read())[0]["value"]
        num_looks_ahead = data["look-ahead"]

    player = ProxyPlayer("P1", num_looks_ahead)
    json.dumps(player.register())
    json_values = parse_json(take_input())
    for json_val in json_values:
        command = json_val["value"]
        try:
            if is_valid_register_command(command):
                name = player.register() # should raise error since player is already registered
                json.dumps(name)
            elif is_valid_place_command(command):
                color, board_list = command[1:]
                player.register_color(color)
                placements = player.place(board_list)
                print(json.dumps(placements))
            elif is_valid_play_command(command):
                board_list = command[1]
                plays = player.play(board_list)
                print(json.dumps(plays))
            elif is_valid_game_over_command(command):
                name = command[1]
                acknowledgement = player.notify(name)
                print(json.dumps(acknowledgement))
            else:
                raise InvalidCommand("Invalid command passed to Player! Given:".format(command))

        except InvalidCommand:
            print(json.dumps("Santorini is broken! Too many tourists in such a small place..."))
        except IllegalPlay: # TODO: donno the behaviour yet
            pass
        except ContractViolation:  # TODO: unspecified behaviour for invalid input
            pass
        except Exception as e:
            print(json.dumps(str(e)))
            # print(json.dumps(traceback.format_exc()))


if __name__ == "__main__":
    main()
