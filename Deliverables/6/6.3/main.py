import json
import traceback

from Player import Player
from Referee import Referee


def main():
    player1 = Player()
    player2 = Player()
    referee = Referee(player1, player2)
    winner = referee.play_game()
    if winner:
        print(json.dumps(winner))


if __name__ == "__main__":
    main()
