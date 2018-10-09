import random


class Player(object):

    @staticmethod
    def start_game():
        return random.randint(0, 11)

    @staticmethod
    def keep_number():
        return random.choice((True, False))

    @staticmethod
    def end_game(won):
        assert type(won) is bool

