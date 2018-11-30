from abc import ABC, abstractmethod
from Player import Player
from ProxyPlayer import ProxyPlayer
from Referee import Referee
import socket


class BaseAdmin(ABC):

    def __init__(self, host, port, num_remote_players):
        self.num_remote_players = num_remote_players
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((host, port))

    @abstractmethod
    def _populate_players(self):
        pass

    @abstractmethod
    def run_tournament(self):
        pass

    @abstractmethod
    def print_rankings(self):
        pass

    def _players_not_power_of_2(self):
        return not (self.num_remote_players != 0 and not (self.num_remote_players & (self.num_remote_players - 1)))


class SingleEliminationAdmin(BaseAdmin):

    def __init__(self, host, port, num_remote_players):
        super().__init__(host, port, num_remote_players)
        self.players = {}
        self.stage = 1

    def _populate_players(self):
        self.s.listen()
        while len(self.players) < self.num_remote_players:
            conn, addr = self.s.accept()
            player = ProxyPlayer(conn)
            self.players[player] = None

        if self._players_not_power_of_2():
            # add default players if needed
            num = self.num_remote_players
            count = 0
            while num != 0:
                num = num >> 1
                count = count + 1
            for i in range((1 << count) - self.num_remote_players):
                local_player = Player("Computer" + str(i))
                self.players[local_player] = None

    def run_tournament(self):
        # initialize active players for first round (all players)
        active_players = set(self.players.keys())

        # while there is no tournament winner
        while len(active_players) > 1:
            # TODO: refactor to use threading
            # assign opponents, instantiate referees, make play_game() calls, record results
            for i in range(len(active_players) // 2):
                player1, player2 = active_players[i], active_players[len(active_players)-1-i]
                referee = Referee(player1, player2)
                winner, loser_cheated = referee.play_game()
                loser = player2 if winner is player1 else player1

                self.players[loser] = 0 if loser_cheated else self.stage
                active_players.remove(loser)

            self.stage += 1

        self.players[winner] = self.stage

    def print_rankings(self):
        results = [(key, self.players[key]) for key in self.players]
        results.sort(key=lambda x: x[1], reverse=True)
        for player, rank in results:
            print("{rank} : {name}".format(rank=(self.stage-rank+1), name=player.get_name()))


class RoundRobinAdmin(BaseAdmin):

    def __init__(self, host, port, num_remote_players):
        super().__init__(host, port, num_remote_players)
        pass

    def _populate_players(self):
        pass

    def run_tournament(self):
        pass

    def print_rankings(self):
        pass

