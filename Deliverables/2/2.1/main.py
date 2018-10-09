from .Player import Player
from .JsonParser import take_input, parse_json


def main():
    command_list = parse_json(take_input())
    for command_obj in command_list:
        operation = getattr(Player, command_obj['value']['operation-name'])
        arguments = []
        for i in range(1, len(command_obj['value'])):
            arguments.append(command_obj['value']['operation-argument{}'.format(i)])
        print(operation(*arguments))


if __name__ == '__main__':
    main()
