import random


class Player(object):

    def __init__(self):
        self.started = False
        self.made_choice = False

    def start_game(self):
        assert not self.started, "Can't call player.start_game() more than once until player.end_game() is called."
        self.started = True
        # return random.randint(0, 11)
        return 9  # only for testing

    def keep_number(self):
        assert self.started, "Can't call player.keep_number() until player.start_game() is called."
        assert not self.made_choice, "Can't call player.keep_number() more than \
                                        once after player.start_game() is called."
        self.made_choice = True
        # return random.choice((True, False))
        return False  # only for testing

    def end_game(self, won):
        assert self.started, "Can't call player.end_game() until player.start_game() is called."
        assert self.made_choice, "Can't call player.end_game() until player.keep_number() is called."
        assert type(won) is bool
        self.started = False
        self.made_choice = False

