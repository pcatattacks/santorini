from Board import Board
from Player import Player
from RuleChecker import RuleChecker
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
        self.player_turn = None
        self.board = Board()

    def play_game(self):
        """
        Drives the Santorini game and invokes interfaces of the Player and RuleChecker components to notify them of the
        updated game state and prompt them for plays. Returns the name of the winning player.

        CONTRACT:
         - Cannot be called more than once.

        :return: the name of the winning player.
        :rtype: string
        """
        turn = 0
        while True:
            # mocking server receiving message
            message = self.players[turn].get_message()
            if not message:
                break

            try:
                message_type = Referee._get_message_type(message)
                if message_type == "name":
                    self._register_player(message)
                elif message_type == "place":
                    self._update_board_with_placements(message)
                elif message_type == "play":
                    won = self._update_board_with_play(message)
                    if won:
                        return self.player_names[turn]

                self.board.display()  # display current state of board
                turn = 1 if turn == 0 else 0  # swapping turn

            except IllegalPlay:
                return self.player_names[turn * -1 + 1]
            except InvalidCommand:
                # TODO - unspecified behaviour since we never expect this
                pass
            except ContractViolation:
                # TODO - unspecified behaviour since we never expect this
                pass

    def _register_player(self, name):
        """
        Registers a player's name and assigns them a color.

        :param string name: The name of the player to be registered.
        :return: The Color (as defined above) assigned to the player that has registered.
        :rtype: string
        """
        if not name or not isinstance(name, str):
            raise ContractViolation("Expected a non-empty string. Received {}".format(name))
        if not self.player_names:
            self.players[0].register(RuleChecker.COLORS[0])
            self.player_names.append(name)
        if len(self.player_names) == 1:
            self.players[1].register(RuleChecker.COLORS[1])
            self.player_names.append(name)
        raise InvalidCommand("Can only register two players.")

    def _update_board_with_placements(self, placements):
        """
        Updates the board with the given placements.

        :param list placements: a list of placements (as defined above)
        :return:
        :rtype: void
        """
        # TODO
        pass

    def _update_board_with_play(self, play):
        """
        Updates the board state with the play and returns `True` if the given play resulted in a win. `False` otherwise.

        :param list play: a play (as defined above)
        :return: Boolean indicating whether the play resulted in the player winning on that turn
        :rtype: bool
        """
        # TODO
        pass

    def check_placements(self, placements):
        """
        Checks the validity of worker placements.

        CONTRACT:
         - Both players must be registered.

        :param list placements: A Placement (as defined above).
        :return: A Board (as defined in the documentation for Board).
        :rtype: list
        """
        if not isinstance(placements, list) or len(placements) != 2 or placements[0] == placements[1]:  # TODO - raise error or lose game?
            raise ContractViolation("Expected a tuple of distinct values. Received {}".format(placements))
        if self.player_turn is None:
            raise InvalidCommand("Both players must be registered before making other commands.")
        # TODO: should we store a boolean indicating whether or not a player has placed their workers or just check the board member variable directly
        # TODO: a way to pass the board member variable of self.board to RuleChecker functions without accessing it directly
        if not RuleChecker.is_legal_initial_board(self.board.board, RuleChecker.COLORS[self.player_turn]):
            raise InvalidCommand("Cannot place workers on this board.")
        for placement in placements:
            # SEE ABOVE: argument modification required
            if not RuleChecker.is_legal_placement(self.board.board, placement):
                raise IllegalPlay(self.player_names[self.player_turn * -1 + 1],
                                  "Invalid placement position given: {}".format(placement))
        for worker_num, placement in enumerate(placements, 1):
            self.board.place_worker(placement[0], placement[1], RuleChecker.COLORS[self.player_turn] + str(worker_num))
        self.swap_turn()
        # TODO: a way to return the board member variable of self.board without accessing it directly, so that it can be provided to the players
        return self.board.board

    def check_play(self, play):
        """
        Checks if a play violates the rules of the game.

        CONTRACT:
         - Both players must be registered.

        :param list play: A Play (as defined above).
        :return: `True` if the rules of the game are violated, `False` otherwise.
        :rtype: bool
        """
        if not isinstance(play, list) or len(play) != 2:
            raise ContractViolation("Expected a tuple. Received {}".format(play))
        if not isinstance(play[0], str):
            raise ContractViolation("Expected a string for worker name. Received {}".format(play[0]))
        if (not isinstance(play[1], list)
                or not 0 < len(play[1]) <= 2
                or not all(isinstance(direction, str) for direction in play[1])):
            raise (ContractViolation
                   ("Expected a non-empty list (max length = 2) of strings for directions. Received {}"
                    .format(play[1])))
        if self.player_turn is None:
            raise InvalidCommand("Both players must be registered before making other commands.")
        if play[0][:-1] != RuleChecker.COLORS[self.player_turn]\
                or not RuleChecker.is_legal_play(self.board, play[0], play[1]):
            raise IllegalPlay(self.player_names[self.player_turn * -1 + 1],
                              "Illegal play made by {player}: {play}".format(player=self.players[self.player_turn],
                                                                             play=play))
        if RuleChecker.is_winning_move(self.board, play[0], play[1][0]):
            # TODO - don't raise a fucking exception
            raise IllegalPlay(self.player_names[self.player_turn])
            # return self.player_names[self.player_turn]
        self.board.move(play[0], play[1][0])
        self.board.build(play[0], play[1][1])
        self.swap_turn()
        # SEE ABOVE: return value modification required
        return self.board.board

    def swap_turn(self):
        if self.player_turn == 0:
            self.player_turn = 1
        else:
            self.player_turn = 0

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
                if isinstance(item1, str) and isinstance(item2, list):  # play command
                    return "play"
                elif all(isinstance(item, list) and all(isinstance(x, int) for x in item) for item in message):
                    return "place"
        raise InvalidCommand("Message format not supported: {}".format(message))
