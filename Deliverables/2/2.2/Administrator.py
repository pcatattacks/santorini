import random
import json

MIN_POSSIBLE_VALUE = 1
MAX_POSSIBLE_VALUE = 10


class ContractError(Exception):
    """Custom exception for violating contracts."""
    pass


class Administrator(object):

    def __init__(self):
        self.admin_option = -1
        self.player_option = -1
        self.face_down_cards = random.shuffle(list(range(MIN_POSSIBLE_VALUE, MAX_POSSIBLE_VALUE + 1)))

    def start_game(self):
        self.pick_card()
        self.send_player_message("pick_number_or_card")
        self.set_player_option(int(input()))  # handles players choice
        self.send_player_message("notify_of_verdict", self.admin_win())
        self.end_game()

    def pick_card(self):
        # self.admin_option = face_down_cards.pop()
        self.admin_option = 8  # TESTING:  Setting values for testing purposes - Random value works as expected.

    def admin_win(self):
        return self.admin_option >= self.player_option

    def set_player_option(self, value):
        if type(value) is not int:
            raise TypeError("Administrator.set_player_option() only excepts one integer argument.")
        elif value > MAX_POSSIBLE_VALUE or value < MIN_POSSIBLE_VALUE:
            raise ValueError("Administrator.set_player_option() value argument \
                                must be between {min} and {max} inclusive."
                             .format(min=MIN_POSSIBLE_VALUE, max=MAX_POSSIBLE_VALUE))
        if value == -1:
            self.player_option = self.face_down_cards.pop()
        else:
            self.player_option = value

    @staticmethod
    def send_player_message(operation_name, *args):
        message = {"operation-name": operation_name}
        for i, arg in enumerate(args):
            message["operation-argument{}".format(i)] = arg
        print(json.dumps(message))

    def end_game(self):
        """Resets the game state so it can be played again."""
        self.admin_option = -1
        self.player_option = -1
        self.face_down_cards = random.shuffle(list(range(MIN_POSSIBLE_VALUE, MAX_POSSIBLE_VALUE + 1)))
