# import Board
# import RuleChecker


class Player:
    """
    A class to maintain the state of a player and allow it to perform player actions within the Santorini game, and get
    notified about the state of the Game after each action.

    Dependencies:
     - Board class. Refer to Board documentation.
     - Strategy class. Refer to Strategy documentation.

    Definitions:

    color
        `string`: either "blue" or "white"

    play
        `tuple`: (worker, direction1, direction2) or (worker, direction1) where direction1 is the direction to move and
        direction2 is the direction to build.

    strategized play
        A play returned by an instance of the Strategy class. See `play` and documentation of `Strategy` class.


    """

    def __init__(self):
        pass

    def register(self, color):
        """
        Sets the `color` member variable to the parameter `color`.

        CONTRACT:
         - Must be the first function to be called after Player is instantiated.
         - Cannot be called more than once.

        :param string color:
        :return:
        :rtype: void
        """
        pass

    def send_play(self):
        """
        Returns the strategized play a player wants to execute on a given turn.

        :return: a play (as defined above)
        :rtype: `tuple`
        """
        pass

    def receive_notification(self, board, has_won, end_game):
        """
        Notifies the player about the updated state of the Santorini Game.

        Ends the game if `end_game` is `True`, else continues the game.
        Notifies the Player if it has won if `has_won` is `True`, else notifies the player otherwise.

        CONTRACT:
         - if `has_won` is `True`, `end_game` must be `True`.

        :param Board board: an instance of Board (refer to documentation of Board class).
        :param bool has_won: `True` if this Player has won the Santorini game, `False` otherwise.
        :param bool end_game: `True` if the Santorini game has ended, `False` otherwise.
        :return:
        :rtype: void
        """
        pass


class Strategy:
    """
    A class that is used by the player to construct plays that a `Player` uses.

    Dependencies:
     - Board class. Refer to Board documentation.
     - RuleChecker class. Refer to RuleChecker documentation.

    Definitions:

    play
        `tuple`: (worker, direction1, direction2) or (worker, direction1) where direction1 is the direction to move and
        direction2 is the direction to build.

    """

    def __init__(self):
        pass

    @staticmethod
    def next_play(board, color):
        """
        Returns the optimal play for a given board and a color that identifies the player.

        :param Board board: an instance of Board (refer to documentation of Board class).
        :param string color: color (as defined above)
        :return: a play (as defined above)
        :rtype: `tuple`
        """
        pass
