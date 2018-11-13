from Board import Board
import sys
from JsonParser import take_input, parse_json # For testing, remove later
import json


class StubPlayer:

    messages = list(reversed(parse_json(take_input())))

    def __init__(self):
        self.name = None
        self.board = None

    def get_name(self):
        message = StubPlayer.messages.pop()["value"]
        self.name = message
        return message

    def register(self, color):
        print(json.dumps(color))

    def place(self, board):
        return StubPlayer.messages.pop()["value"]

    def play(self, board, num_moves_ahead):
        if not StubPlayer.messages:
            sys.exit(0)
        return StubPlayer.messages.pop()["value"]

    def notify(self, board, has_won, end_game):  # TODO: end_game keyword argument may be unnecessary
        if has_won:
            print(json.dumps(self.name))
        elif not end_game:
            print(json.dumps(board.board))
