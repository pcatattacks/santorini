from PlayerInterface import PlayerInterface


class ProxyPlayer(PlayerInterface):

    def register(self, color):
        pass

    def place(self, board):
        pass

    def play(self, board, num_moves_ahead):
        pass

    def notify(self, board, has_won, end_game):
        pass
