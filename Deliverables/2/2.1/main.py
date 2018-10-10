import json
from Player import Player
from JsonParser import take_input, parse_json


def main():
    player = Player()
    command_list = parse_json(take_input())
    for command_obj in command_list:
        operation = getattr(player, command_obj['value']['operation-name'])
        arguments = []
        for i in range(1, len(command_obj['value'])):
            arguments.append(command_obj['value']['operation-argument{}'.format(i)])
        result = operation(*arguments)
        print(json.dumps([result])[1:-1])


if __name__ == '__main__':
    main()
