#!/usr/bin/python3
import random
from runme import take_input, parse_json

MIN_POSSIBLE_VALUE = 1
MAX_POSSIBLE_VALUE = 10


class GameWorld:
    admin_option = -1
    player_option = -1
    swap_option = -1


def start_game(player_option):
    game_world = GameWorld()
    game_world = admin_option_picker(game_world)
    game_world = set_user_option(game_world, player_option)

    return admin_win_checker(game_world)


def admin_option_picker(game_world):
    face_down_cards = list(range(MIN_POSSIBLE_VALUE, MAX_POSSIBLE_VALUE + 1))
    random.shuffle(face_down_cards)
    game_world.admin_option = face_down_cards.pop()
    game_world.swap_option = face_down_cards.pop()

    # TESTING:  Setting values for testing purposes - Random values works as expected.
    game_world.admin_option = 8
    game_world.swap_option = 6

    return game_world


def set_user_option(game_world, user_option):
    if user_option is -1:
        game_world.player_option = game_world.swap_option
    else:
        game_world.player_option = user_option
    return game_world


def admin_win_checker(game_world):
    if game_world.player_option > game_world.admin_option:
        return "Player Won"
    else:
        return "Player Lost"


def main():
    command_list = parse_json(take_input())
    for command_obj in command_list:
        if command_obj['value']['operation-name'] == "start_game":
            print(start_game(int(command_obj['value']['operation-argument1'])))


if __name__ == "__main__":
    main()