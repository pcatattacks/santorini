import json
from ProxyPlayer import ProxyPlayer
from JsonParser import parse_json, take_input
from CustomExceptions import InvalidCommand, ContractViolation, IllegalPlay, IllegalResponse
from player_driver import is_valid_register_command,\
    is_valid_place_command, is_valid_play_command, is_valid_game_over_command


def main():

    host, port = "127.0.0.1", 9999
    player = ProxyPlayer(host, port)
    player.register()  # we don't have to print it for this assignment.
    json_values = parse_json(take_input())
    acknowledgement = None
    for json_val in json_values:
        command = json_val["value"]
        try:
            if is_valid_register_command(command):
                name = player.register()  # should raise error since player is already registered
                json.dumps(name)
            elif is_valid_place_command(command):
                color, board_list = command[1:]
                placements = player.place(board_list, color)
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
            break
        except IllegalPlay:  # TODO: donno the behaviour yet
            pass
        except IllegalResponse as e:  # TODO: Defined for Proxy receiving incorrectly formatted responses. what behaviour?
            # could we possibly use ContractViolation instead, since giving an incorrect response is the same as
            # violating a function contract.
            raise e  # debug
        except ContractViolation as e:  # TODO: unspecified behaviour for invalid input
            print(json.dumps("Santorini is broken! Too many tourists in such a small place..."))
            break
        # except Exception as e:
        #     print(json.dumps(str(e)))
        #     # print(json.dumps(traceback.format_exc()))

    # ensures that player_driver server terminates if EOF is reached in std in, but Game Over isn't called.
    if not acknowledgement:
        player.notify("placeholder")


if __name__ == "__main__":
    main()
