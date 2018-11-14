from abc import ABC, abstractmethod


class PlayerInterface(ABC):
    """
    An interface implemented by a Santorini player component, which allow it to perform player actions within the
    Santorini game, and get notified about the state of the Game after each action.

    Dependencies:
     - Board class. Refer to Board documentation.
     - Strategy class. Refer to Strategy documentation.

    Definitions:

    color
        `string`: either "blue" or "white"

    play
        `list`: [worker, [direction1, direction2]] or [worker, [direction1]] where direction1 is the direction to move
        and direction2 is the direction to build.

    """

    @abstractmethod
    def register(self):
        """
        Returns the name of the player.

        CONTRACT:
         - Must be the first function to be called after Player is instantiated.
         - Cannot be called more than once.

        :return: the name of the player
        :rtype: string
        """
        pass

    @abstractmethod
    def place(self, board, color):
        """
        Sets the `color` member variable to the parameter `color`. Returns the worker placements for the player.

        CONTRACT:
         - Can only be called after Player.register() has been called.
         - Must be called before Player.play().
         - Cannot be called more than once.
         - `board` must be a valid initial board (a board where all cell's heights are 0, and no workers of `self.color`
         are present any cell.

        :param list board: an instance of Board (refer to documentation of Board class).
        :param string color: a color (as defined above)
        :return: `list` of [position1, position2] denoting the position of the player's 1st and 2nd worker respectively.
        See `position`, `worker` in documentation of Board.py.
        :rtype: list
        """
        pass

    @abstractmethod
    def play(self, board):
        """
        Returns the play a player wants to execute on a given turn.

        :param list board:
        :return: a play (as defined above)
        :rtype: list
        """
        pass

    @abstractmethod
    def notify(self, winner_name):
        """
        Notifies the player with the winner of the Santorini game.

        CONTRACT:
         - can only be called once per game
         - must be the last function to be called by an object that implements PlayerInterface.

        :param string winner_name: Name of the winner of the Santorini game
        :return: An acknowledgement string of "OK"
        :rtype: string
        """
        pass
