#!/usr/bin/python3
import random


MIN_POSSIBLE_VALUE = 1
MAX_POSSIBLE_VALUE = 10


class GameWorld:

    new_game = True
    system_option = -1
    player_option = -1
    swap_option = -1


def start_game(game_world):

    if game_world.new_game is True:
        game_world.new_game = False
    else:
        print("Game already in Progress. Cannot start new game")
    return game_world


def admin_option_picker(game_world):

    if game_world.new_game is True:

        face_down_cards = list(range(MIN_POSSIBLE_VALUE, MAX_POSSIBLE_VALUE + 1))
        random.shuffle(face_down_cards)

        game_world.system_option = face_down_cards.pop()
        game_world.swap_option = face_down_cards.pop()
    else:
        print("Cannot modify in-between game!!")
    return game_world


# Set User Option by calling player_option_picker() which would return the player's option.
def set_user_option(game_world):
    # TODO:  Should be replaced with PlayerModule.player_option_picker() - If boolean then use admin.swap_option
    if game_world.new_game is False:
        # TODO: Remove this line of code after player module is implemented.
        game_world.player_option = game_world.swap_option
        ''' 
            player_option = player_module.player_option_picker()
            if type(player_option) is boolean:
                game_world.player_option = game_world.swap_option
            else:
                game_world.player_option = player_option
    
        '''
    else:
        print("Cannot Modify in-between game")
    return game_world


def admin_win_checker(game_world):
    if game_world.new_game is False:

        if game_world.player_option > game_world.system_option:
            return True
        else:
            return False


def admin_game_driver():
    game_world = GameWorld()

    game_world = admin_option_picker(game_world)
    game_world = start_game(game_world)
    game_world = set_user_option(game_world)

    return admin_win_checker(game_world)


def main():
    admin_game_driver()


if __name__ == "__main__":
    main()