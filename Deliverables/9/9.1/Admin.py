from abc import ABC, abstractmethod
from SmartPlayer import SmartPlayer
from ProxyPlayer import ProxyPlayer
from Referee import Referee
from CustomExceptions import InvalidCommand
import socket


class BaseAdmin(ABC):

    def __init__(self, host, port, num_remote_players, fallback_player=SmartPlayer):
        self.num_remote_players = num_remote_players
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((host, port))
        self.fallback_player = fallback_player

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
        if self.num_remote_players == 1:
            return True
        return not (self.num_remote_players != 0 and not (self.num_remote_players & (self.num_remote_players - 1)))


class SingleEliminationAdmin(BaseAdmin):

    def __init__(self, host, port, num_remote_players, fallback_player=SmartPlayer):
        super().__init__(host, port, num_remote_players, fallback_player)
        self.players = {}
        self.stage = 1
        self._populate_players()

    def _populate_players(self):
        self.s.listen(self.num_remote_players)
        while len(self.players) < self.num_remote_players:
            conn, addr = self.s.accept()
            player = ProxyPlayer(conn)

            try:
                player.register()
            except InvalidCommand:
                conn.close()
                player = self.fallback_player()
                player.register()
            self.players[player] = None

        if self._players_not_power_of_2():
            # add default players if needed
            num = self.num_remote_players if self.num_remote_players != 0 else 1
            count = 0
            while num != 0:
                num = num >> 1
                count = count + 1
            for i in range((1 << count) - self.num_remote_players):
                local_player = self.fallback_player()
                local_player.register()
                self.players[local_player] = None

    def run_tournament(self):
        # initialize active players for first round (all players)
        active_players = list(self.players.keys())
        # print(self.players) # debug
        # print(active_players) # debug
        # while there is no tournament winner
        while len(active_players) > 1:
            print("We're at stage {}!".format(self.stage))  # debug
            # TODO: refactor to be concurrent
            # assign opponents, instantiate referees, make play_game() calls, record results
            for i in range(len(active_players) // 2):
                player1, player2 = active_players[i], active_players[len(active_players)-1-i]
                referee = Referee(player1, player2)
                winner, loser_cheated = referee.play_game()
                loser = player2 if winner is player1 else player1
                loser_idx = len(active_players)-1-i if winner is player1 else i

                self.players[loser] = 0 if loser_cheated else self.stage
                active_players[loser_idx] = None

                print(winner.get_name() + " won!", loser.get_name() + " lost!")  # debug
                print("{} current rank: {}".format(winner.get_name(), self.players[winner]))  # debug
                print("{} current rank: {}".format(loser.get_name(), self.players[loser]))  # debug

            active_players = [player for player in active_players if player is not None]
            self.stage += 1

        self.players[winner] = self.stage

        self.s.close()  # cleanup

    def print_rankings(self):
        print("\nFinal Standings:\n----------------------")
        results = [(key, self.players[key]) for key in self.players]
        results.sort(key=lambda x: x[1], reverse=True)
        for player, rank in results:
            print("{rank} : {name}".format(rank=self.stage-rank+1, name=player.get_name()))


class RoundRobinAdmin(BaseAdmin):

    def __init__(self, host, port, num_remote_players, fallback_player=SmartPlayer):
        super().__init__(host, port, num_remote_players, fallback_player)
        self.players = {}
        self._populate_players()

    def _populate_players(self):
        self.s.listen(self.num_remote_players)
        while len(self.players) < self.num_remote_players:
            conn, addr = self.s.accept()
            player = ProxyPlayer(conn)

            try:
                player.register()
            except InvalidCommand:
                conn.close()
                player = self.fallback_player()
                player.register()
            self.players[player] = []

        if self._players_not_power_of_2():
            # add default players if needed
            num = self.num_remote_players if self.num_remote_players != 0 else 1
            count = 0
            while num != 0:
                num = num >> 1
                count = count + 1
            for i in range((1 << count) - self.num_remote_players):
                local_player = self.fallback_player()
                local_player.register()
                self.players[local_player] = []

    def run_tournament(self):
        active_players = list(self.players.keys())
        for i in range(len(active_players)):
            for j in range(i+1, len(active_players)):
                player1, player2 = active_players[i], active_players[j]
                referee = Referee(player1, player2)
                winner, loser_cheated = referee.play_game()
                loser = player2 if winner is player1 else player1
                loser_idx = j if winner is player1 else i
                self.players[winner].append(loser)

                if loser_cheated:
                    for past_opponent in self.players[loser]:
                        self.players[past_opponent].append(loser)
                    self.players[loser] = []
                    sub_player = self.fallback_player()
                    active_players[loser_idx] = sub_player
                    self.players[sub_player] = []

        self.s.close()  # cleanup

    def print_rankings(self):
        print("\nFinal Standings:\n----------------------")
        results = [(key, len(self.players[key])) for key in self.players]
        results.sort(key=lambda x: x[1], reverse=True)
        for player, points in results:
            print("{name} : {points}".format(name=player.get_name(), points=points))

