# from Player import Player
# from RuleChecker import RuleChecker


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
        """
        pass

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

    def check_play(self, color, *play):
        """
        Checks if a play violates the rules of the game.

        :param string color: a Color (as defined above).
        :param list play: A Play (as defined above).
        :return: `True` if the rules of the game are violated, `False` otherwise.
        :rtype: bool
        """
        pass


