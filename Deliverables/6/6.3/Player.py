from Board import Board
from RuleChecker import RuleChecker, Strategy
from CustomExceptions import ContractViolation
from JsonParser import take_input, parse_json # For testing, remove later


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
        `list`: [worker, [direction1, direction2]] or [worker, [direction1]] where direction1 is the direction to move
        and direction2 is the direction to build.

    strategized play
        A play returned by an instance of the Strategy class. See `play` and documentation of `Strategy` class.


    """

    def __init__(self):
        # TODO: Discuss / Document for code walk.
        # Should we have the player store a board object and call the set_board() method within Player,
        # or should we have a Player.set_board() function that simply reassigns self.board to a board object that's
        # already had set_board called on it?
        # Pranav's opinion: I think we should do the first option, because it ensures the clients of player don't have
        # to know about the Board.set_board() function, which is almost a helper, since it doesn't have core
        # functionality that's exposed to users. May as well abstract that using a Player function. If we do option 2,
        # we'll also have to write an extra contract to make sure a board that's been passed in has had set_board()
        # called on it, which will be overly complicated.
        self.board = Board()
        self.color = None

    def register(self, color):
        """
        Sets the `color` member variable to the parameter `color`. Returns the name of the player.

        CONTRACT:
         - Must be the first function to be called after Player is instantiated.
         - Cannot be called more than once.

        :param string color: a color (as defined above)
        :return: the name of the player
        :rtype: string
        """
        if not RuleChecker.is_valid_color(color):
            raise ContractViolation("Invalid color provided: {}".format(color))
        if self.color:
            raise ContractViolation("Cannot call Player.register() again until game ends!")
        self.color = color

    def place(self, board):
        """
        Returns the worker placements for the player.

        CONTRACT:
         - Can only be called after Player.register() has been called.
         - Must be called before Player.play().
         - Cannot be called more than once.
         - `board` must be a valid initial board (a board where all cell's heights are 0, and no workers of `self.color`
         are present any cell.

        :param list board: an instance of Board (refer to documentation of Board class).
        :return: `list` of [position1, position2] denoting the position of the player's 1st and 2nd worker respectively.
        See `position`, `worker` in documentation of Board.py.
        :rtype: list
        """
        if not self.color:
            raise ContractViolation("Function must be called after player.register()!")
        if not RuleChecker.is_legal_initial_board(board, self.color):
            raise ContractViolation("Invalid initial board provided: {}".format(board))
        self.board.set_board(board)
        # TODO: potential contract needed to ensure set_board is called at start of every turn for player
        return Strategy.get_placements(self.board, self.color)

    def play(self, board, num_moves_ahead):   # TODO: get rid of num_look_ahead parameter, just take from file
        """
        Returns the strategized play a player wants to execute on a given turn.

        :param list board:
        :param int num_moves_ahead:
        :return: a play (as defined above)
        :rtype: list
        """
        if not self.color:
            raise ContractViolation("Function must be called after player.register()!")
        if not RuleChecker.is_legal_board(board):
            raise ContractViolation("Invalid board provided: {}".format(board))
        self.board.set_board(board)
        return Strategy.get_plays(self.board, self.color, num_moves_ahead)

    def notify(self, board, has_won, end_game):  # TODO: end_game keyword argument may be unnecessary
        """
        Notifies the player about the updated state of the Santorini Game.

        Ends the game if `end_game` is `True`, else continues the game.
        Notifies the Player if it has won if `has_won` is `True`, else notifies the player otherwise.

        CONTRACT:
         - if `has_won` is `True`, `end_game` must be `True`.

        :param Board board: an instance of Board (refer to documentation of Board class).
        :param bool has_won: `True` if this Player has won the Santorini game, `False` otherwise.
        :param bool end_game: `True` if the Santorini game has ended, `False` otherwise.
        :return: An acknowledgement string of "OK" # TODO - not always true - could be void as well, when the game doesn't end
        :rtype: string
        """
        pass




