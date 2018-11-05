from Board import Board
from Player import Player
from RuleChecker import RuleChecker
from CustomExceptions import ContractViolation, MalformedCommand

class Referee:
    """
    A component that manages a game of Santorini between 2 players.

    Definitions:

    color
        `string`: either "blue" or "white"

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
        :param Board board: An instance of the 'Board' class. See documentation for Board.
        :param string player1_name: A string containing the name of the first player.
        :param string player2_name: A string containing the name of the second player.
        """
        self.player1 = player1
        self.player2 = player2
        self.player1_name = ""
        self.player2_name = ""
        self.board = Board()

    def start_game(self):
        """
        Drives the Santorini game and invokes interfaces of the Player and RuleChecker components to notify them of the
        updated game state and prompt them for plays.

        CONTRACT:
         - Cannot be called more than once.

        :return:
        :rtype: void
        """
        pass

    def register_player(self, name):
        """

        :param string name: A string containing the name of the player to be registered.
        :return: The Color (as defined above) of the player that has registered.
        :rtype: string
        """
        if not type(name) is str or not name:
            raise ContractViolation("Expected a non-empty string. Received {}".format(name))
        if not self.player1_name:
            self.player1_name = name
            return "blue"
        if not self.player2_name:
            self.player2_name = name
            return "white"
        raise MalformedCommand("Can only register two players.")

    def check_placements(self, placements):

        if not isinstance(placements, list)\
                or len(placements) != 2\
                or not all(isinstance(placement, list) for placement in placements):
            raise ContractViolation("Expected a list of two lists. Received {}".format(placements))

        pass

    def check_play(self, color, *play):
        """
        Checks if a play violates the rules of the game.

        :param string color: a Color (as defined above).
        :param list play: A Play (as defined above).
        :return: `True` if the rules of the game are violated, `False` otherwise.
        :rtype: bool
        """
        pass