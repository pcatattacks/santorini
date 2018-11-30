from Board import Board
from RuleChecker import RuleChecker
from CustomExceptions import ContractViolation, InvalidCommand, IllegalPlay, IllegalResponse


class Referee:
    """
    A component that manages a game of Santorini between 2 players.

    Definitions:

    color
        `string`: either of the two strings stored in RuleChecker.COLORS

    placement
        `list`: [position1, position2] where position1 and position2 are the position of a player's workers 1 and 2
        respectively. See `worker`, `position` in documentation of `Board`.

    play
        `list`: [worker, [direction1, direction2]] or [worker, [direction1]] where direction1 is the direction to move
        and direction2 is the direction to build relative to the worker's position.
        See `direction`,`worker`, `position` in documentation of `Board`.

    """
    def __init__(self, player1, player2):
        """
        :param Player player1: An instance of the `Player` class. See documentation for Player.
        :param Player player2: An instance of the `Player` class. See documentation for Player.
        """
        self.players = [player1, player2]
        self.player_names = []
        self.turn = 0
        self.board = Board()

    def play_game(self):
        """
        Drives the Santorini game and invokes interfaces of the Player and RuleChecker components to notify them of the
        updated game state and prompt them for plays. Returns the name of the winning player.

        CONTRACT:
         - Cannot be called more than once.

        :return: the winning player.
        :rtype: Player
        """
        for player in self.players:
            name = player.register()
            print(name)  # debug
            self._register_player(name)
            self._swap_turn()

        for player in self.players:
            placements = player.place(self.board.extract_board(), RuleChecker.COLORS[self.turn])
            print(placements)  # debug
            self._update_board_with_placements(placements)
            self._swap_turn()

        winner = None
        cheating = False
        while not winner:
            player = self.players[self.turn]
            try:
                play = player.play(self.board.extract_board())
                print(play)  # debug
                won = self._update_board_with_play(play)
                if won:
                    winner = self.player_names[self.turn]
                    for p in self.players:
                        p.notify(self.player_names[self.turn])

            # TODO - this needs to be bundled just into IllegalResponse while refactoring ProxyPlayer._examine_for_error
            except (IllegalPlay, InvalidCommand, IllegalResponse):
                winner = self.players[self.turn * -1 + 1]
                cheating = True
                for p in self.players:
                    p.notify(self.player_names[self.turn * -1 + 1])
            except InvalidCommand:
                # TODO - unspecified behaviour
                pass
            except ContractViolation:
                # TODO - unspecified behaviour
                pass

            self._swap_turn()

        print(self.board.board)  # debug
        return winner, cheating

    def _register_player(self, name):
        """
        Registers a player's name and assigns them a color.

        CONTRACT:
         - Can only be called once per distinct player per game (two players).

        :param string name: The name of the player to be registered.
        :return:
        :rtype: void
        """
        if not name or not isinstance(name, str):
            raise ContractViolation("Expected a non-empty string. Received {}".format(name))
        if len(self.player_names) > 2:
            raise InvalidCommand("Can only register two players.")
        self.player_names.append(name)

    def _update_board_with_placements(self, placements):
        """
        Updates the board with the given placements.

        CONTRACT:
         - Can only be called after _register_player has been called for every player.
         - Can only be called once per distinct player per game (two players).

        :param list placements: a list of placements (as defined above)
        :return:
        :rtype: void
        """
        if not RuleChecker.is_valid_placement(placements):
            raise ContractViolation("Placements not in correct format.")
        for placement in placements:
            if not RuleChecker.is_legal_placement(self.board, placement):
                raise IllegalPlay("Invalid placement position given: {}".format(placement))
        for worker_num, placement in enumerate(placements, 1):
            row, col = placement
            worker = RuleChecker.COLORS[self.turn] + str(worker_num)
            self.board.place_worker(row, col, worker)

    def _update_board_with_play(self, play):
        """
        Updates the board state with the play and returns `True` if the given play resulted in a win. `False` otherwise.

        CONTRACT:
         - Can only be called after _update_board_with_placements has been called for every player.

        :param list play: a play (as defined above)
        :return: Boolean indicating whether the play resulted in the player winning on that turn
        :rtype: bool
        """
        if not RuleChecker.is_valid_play(play):
            raise ContractViolation("Play not in correct format.")
        worker, directions = play
        if (worker[:-1] != RuleChecker.COLORS[self.turn]
                or not RuleChecker.is_legal_play(self.board, worker, directions)):
            raise IllegalPlay("Illegal play made by {player}: {play}".format(player=self.players[self.turn], play=play))

        if len(directions) == 1:
            return True

        move_dir, build_dir = directions
        self.board.move(worker, move_dir)
        self.board.build(worker, build_dir)

        return False

    def _swap_turn(self):
        self.turn = 1 if self.turn == 0 else 0

