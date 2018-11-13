import json
# import traceback

from StubPlayer import StubPlayer
from Referee import Referee


def main():
    player1 = StubPlayer()
    player2 = StubPlayer()
    referee = Referee(player1, player2)
    referee.play_game()


if __name__ == "__main__":
    main()
