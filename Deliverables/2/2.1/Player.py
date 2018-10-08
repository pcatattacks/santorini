#!/usr/bin/python3


class Player(object):

    @staticmethod
    def start_game():
        while True:
            try:
                number = int(input("Please choose an integer between 1 and 10 inclusive:"))
                assert 0 <= number <= 10
                break
            except (ValueError, AssertionError):
                print("Invalid value.")
        return number

    @staticmethod
    def keep_number():
        pick = 'pick'
        keep = 'keep'
        while True:
            try:
                decision = input("""Would you like to keep your number or pick one from the pile?
                Please enter {option1} or {option2}:""".format(option1=pick, option2=keep))
                assert decision.lower() == pick or decision.lower() == keep
                break
            except AssertionError:
                print("Please choose and type either 'pick' or 'keep':")
        return True if decision == keep else False

    @staticmethod
    def end_game(won):
        assert type(won) is bool
        if won:
            print("You, the player, have won!")
        else:
            print("Sorry, you have lost. Better luck next time!")


if __name__ == "__main__":
    # only for initial testing.
    Player.start_game()
    Player.keep_number()
    Player.end_game(True)
