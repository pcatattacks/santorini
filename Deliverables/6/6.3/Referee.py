import json
from Board import Board
from RuleChecker import RuleChecker
from JsonParser import parse_json, take_input
from CustomExceptions import ContractViolation, InvalidCommand, IllegalPlay


class Referee:
    """
    A component that manages a game of Santorini between 2 players.

    Definitions:

    color
        `string`: either "blue" or "white"
        # TODO: should this description refer to the static variable RuleChecker.COLORS

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
        self.board = Board()
        self.turn = None

        # shadow state
        self.unplaced_workers = list(RuleChecker.WORKERS)

    def play_game(self):
        """
        Drives the Santorini game and invokes interfaces of the Player and RuleChecker components to notify them of the
        updated game state and prompt them for plays. Returns the name of the winning player.

        CONTRACT:
         - Cannot be called more than once.

        :return: the name of the winning player.
        :rtype: string
        """

        for player in self.players:
            name = player.register(RuleChecker.COLORS[self.turn]) # the ProxyPlayer will wait for an incoming connection
            # - till then, this method will block
            self._register_player(name)

        for player in self.players:
            placements = player.place(self.board)
            self._update_board_with_placements(placements)

        won = False
        winner = None
        while not winner:
            player = self.players[self.turn]
            try:
                play = player.play()
                won = self._update_board_with_play(play)
                if won:
                    winner = self.player_names[self.turn]
                    player.notify(self.board, has_won=True, end_game=True)
                else:
                    for p in self.players:
                        p.notify(self.board, has_won=False, end_game=False)

            except IllegalPlay:
                winner = self.player_names[self.turn * -1 + 1]
                player.notify(self.board, has_won=won, end_game=True)
            except InvalidCommand:
                # TODO - unspecified behaviour since we never expect this in assignment 6
                pass
            except ContractViolation:
                # TODO - unspecified behaviour since we never expect this in assignment 6
                pass

            self.turn = 1 if self.turn == 0 else 0  # swapping turn

        self.players[self.turn].notify(self.board, has_won=(not won), end_game=True)  # notify other player
        return winner

        # messages = list(reversed(parse_json(take_input())))  # only for testing
        #
        # while True:
        #     # mocking server receiving message
        #     if not messages:
        #         break
        #     message = messages.pop()["value"]
        #
        #     try:
        #         message_type = Referee._get_message_type(message)
        #         if message_type == "name":
        #             assigned_color = self._register_player(message)
        #             print(json.dumps(assigned_color))
        #         else:
        #
        #             if message_type == "place":
        #                 self._update_board_with_placements(message)
        #             elif message_type == "play":
        #                 won = self._update_board_with_play(message)
        #                 if won:
        #                     return self.player_names[self.turn]
        #
        #             self.board.display()
        #             self.turn = 1 if self.turn == 0 else 0  # swapping turn
        #
        #     except IllegalPlay:
        #         return self.player_names[self.turn * -1 + 1]
        #     except InvalidCommand:
        #         # TODO - unspecified behaviour since we never expect this
        #         pass
        #     except ContractViolation:
        #         # TODO - unspecified behaviour since we never expect this
        #         pass
        #
        # return None  # placeholder for testing

    def _register_player(self, name):
        """
        Registers a player's name and assigns them a color.

        CONTRACT:
         - Can only be called once per distinct player per game (two players).

        :param string name: The name of the player to be registered.
        :return: The Color (as defined above) assigned to the player that has registered.
        :rtype: string
        """
        if not name or not isinstance(name, str):
            raise ContractViolation("Expected a non-empty string. Received {}".format(name))
        if not self.player_names:
            self.players[0].register(RuleChecker.COLORS[0])
            self.player_names.append(name)
            return RuleChecker.COLORS[0]
        if len(self.player_names) == 1:
            self.players[1].register(RuleChecker.COLORS[1])
            self.player_names.append(name)
            self.turn = 0
            return RuleChecker.COLORS[1]
        raise InvalidCommand("Can only register two players.")

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
        if self.turn is None:
            # TODO: use InvalidCommand or IllegalPlay?
            raise InvalidCommand("Both players must be registered before making other commands.")
        if not self.unplaced_workers:
            # TODO: use InvalidCommand or IllegalPlay?
            raise InvalidCommand("Cannot place workers on this board.")
        for placement in placements:
            if not RuleChecker.is_legal_placement(self.board, placement):
                raise IllegalPlay("Invalid placement position given: {}".format(placement))
        for worker_num, placement in enumerate(placements, 1):
            row, col = placement
            worker = RuleChecker.COLORS[self.turn] + str(worker_num)
            self.board.place_worker(row, col, worker)
            self.unplaced_workers.remove(worker)

    def _update_board_with_play(self, play):
        """
        Updates the board state with the play and returns `True` if the given play resulted in a win. `False` otherwise.

        CONTRACT:
         - Can only be called after _update_board_with_placements has been called for every player.

        :param list play: a play (as defined above)
        :return: Boolean indicating whether the play resulted in the player winning on that turn
        :rtype: bool
        """
        # TODO
        if self.unplaced_workers:
            raise InvalidCommand("Both players must have placed workers before making other commands.")
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

    @staticmethod
    def _get_message_type(message):
        """
        Checks if a message is correctly formatted and returns the type of message.

        Message types may be:
        - name
        - place
        - play

        :param any message:
        :return: the type of the message received
        :rtype: string
        """
        if isinstance(message, str):
            return "name"
        if isinstance(message, list):
            # TODO: add more stringent checking for items within the command
            if len(message) == 2:
                item1, item2 = message
                if (isinstance(item1, str) and isinstance(item2, list)
                        and all(RuleChecker.is_valid_direction(direction) for direction in item2)):
                    return "play"
                elif all(isinstance(item, list) and all(isinstance(x, int) for x in item) for item in message):
                    return "place"
        raise InvalidCommand("Message format not supported: {}".format(message))
