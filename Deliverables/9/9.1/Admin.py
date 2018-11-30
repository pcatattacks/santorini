from Player import Player
from ProxyPlayer import ProxyPlayer
from Referee import Referee
import socket
import time

class Admin:
    """

    """

    # TODO: retrieve data from santorini.config and command line
    IP = 'localhost'
    PORT = 9999
    STYLE = "cup"
    NUM_REMOTE_PLAYERS = 1
    NUM_LOOKS_AHEAD = 2

    def __init__(self):
        self.players = []
        self.player_ranks = []
        self.results = []
        self.stage = 0
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((Admin.IP, Admin.PORT))

    def administer_tournament(self):
        self.populate_players()
        if Admin.STYLE == "league":
            self.round_robin()
        elif Admin.STYLE == "cup":
            self.single_elimination()
        else:
            pass # TODO: raise relevant exception
        self.print_rankings()

    def populate_players(self):
        # wait for connections from remote players
        self.s.listen()
        while len(self.players) < Admin.NUM_REMOTE_PLAYERS:
            conn, addr = self.s.accept()
            player = ProxyPlayer(conn)
            self.players.append(player)
            self.player_ranks.append(None)
        # TODO: refactor into helper function
        # if # of players != 2^n, add default players
        num_players = len(self.players)
        if not (num_players != 0 and not (num_players & (num_players - 1))):
            num = num_players
            count = 0
            while num != 0:
                num = num >> 1
                count = count + 1
            for player in range((1 << count) - num_players):
                self.players.append(Player.Player("Computer" + str(player), Admin.NUM_LOOKS_AHEAD))
                self.player_ranks.append(None)

    def round_robin(self):
        pass

    def single_elimination(self):
        # initialize active players for first round (all players)
        active_players = []
        for count, player in enumerate(self.players):
            active_players.append(count)
        # while there is no tournament winner
        while len(active_players) > 1:
            # TODO: refactor so that local players do not play against each other
            # TODO: refactor to use threading
            # assign opponents, instantiate referees, make play_game() calls
            it = iter(active_players)
            for p1, p2 in zip(it, it):
                referee = Referee.Referee(self.players[p1], self.players[p2], self, p1, p2)
                referee.play_game()
            # wait for results
            while len(self.results) < len(active_players):
                time.sleep(10)
            # TODO: update player_ranks of losing players with current stage

            # remove losing players from active_players
            for player in active_players:
                if self.player_ranks[player] is not None:
                    active_players.remove(player)
            self.stage += 1
        self.player_ranks[active_players[0]] = self.stage

    def update_results(self, winner, loser, cheating):
        if cheating:
            loser_rank = 0
        else:
            loser_rank = self.stage
        self.results.append(loser, loser_rank)

    def print_rankings(self):
        rank = 1
        while self.stage >= 0:
            # every player who dropped out this stage has the same rank
            for count, player in enumerate(self.players):
                if self.player_ranks[count] == self.stage:
                    print(str(rank) + ": " + player.get_name())
            rank += 1
            self.stage -= 1
