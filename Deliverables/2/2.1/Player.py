import random


class ContractError(Exception):
    """Custom exception for violating contracts."""
    pass


class Player(object):

    def __init__(self):
        self.started = False
        self.made_choice = False

    def start_game(self):
        if self.started:
            raise ContractError("Can't call player.start_game() more than once until player.end_game() is called.")
        self.started = True
        # return random.randint(0, 11)
        return 9  # only for testing

    def keep_number(self):
        if not self.started:
            raise ContractError("Can't call player.keep_number() until player.start_game() is called.")
        elif self.made_choice:
            raise ContractError("Can't call player.keep_number() more than \
                                        once after player.start_game() is called.")
        self.made_choice = True
        # return random.choice((True, False))
        return False  # only for testing

    def end_game(self, won):
        if not self.started:
            raise ContractError("Can't call player.end_game() until player.start_game() is called.")
        elif not self.made_choice:
            raise ContractError("Can't call player.end_game() until player.keep_number() is called.")
        elif type(won) is not bool:
            raise TypeError("Player.end_game() only accepts one boolean argument.")
        self.started = False
        self.made_choice = False

