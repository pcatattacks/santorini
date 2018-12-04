from Board import Board
from RuleChecker import RuleChecker
from Strategies import BaseStrategy, RandomStrategy
from CustomExceptions import ContractViolation
from PlayerInterface import PlayerInterface


class Player(PlayerInterface):
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

    COUNT = 0  # number of instances of local players. For naming purposes only.

    def __init__(self, name=None, strategy=RandomStrategy()):
        """

        :param str name: the name of the Santorini player.
        :param Strategy strategy: the strategy the player employs.
        :return:
        :rtype: None
        """
        # TODO: Discuss / Document for code walk.
        # Should we have the player store a board object and call the set_board() method within Player,
        # or should we have a Player.set_board() function that simply reassigns self.board to a board object that's
        # already had set_board called on it?
        # Pranav's opinion: I think we should do the first option, because it ensures the clients of player don't have
        # to know about the Board.set_board() function, which is almost a helper, since it doesn't have core
        # functionality that's exposed to users. May as well abstract that using a Player function. If we do option 2,
        # we'll also have to write an extra contract to make sure a board that's been passed in has had set_board()
        # called on it, which will be overly complicated.
        if not name:
            self.name = "LocalPlayer{}".format(Player.COUNT)
        elif not isinstance(name, str):
            raise ContractViolation("Name must be a string!")
        else:
            self.name = name
        if not isinstance(strategy, BaseStrategy):
            raise ContractViolation("Strategy must implement BaseStrategy interface!")
        self.board = Board()
        self.strategy = strategy
        self.color = None
        self.registered = False  # shadow state
        Player.COUNT += 1

    def register(self):
        """
        Returns the name of the player.

        CONTRACT:
         - Must be the first function to be called after Player is instantiated.
         - Cannot be called more than once.

        :return: the name of the player
        :rtype: str
        """
        if self.registered:
            raise ContractViolation("Cannot call Player.register() more than once!")
        self.registered = True
        return self.name

    def place(self, board, color):
        """
        Returns the worker placements for the player.

        CONTRACT:
         - Can only be called after Player.register() has been called.
         - Must be called before Player.play().
         - Cannot be called more than once.
         - `board` must be a valid initial board (a board where all cell's heights are 0, and no workers of `self.color`
         are present any cell.

        :param list board: an instance of Board (refer to documentation of Board class).
        :param str color: A color (as defined in the documentation of Referee).
        :return: `list` of [position1, position2] denoting the position of the player's 1st and 2nd worker respectively.
        See `position`, `worker` in documentation of Board.py.
        :rtype: list
        """
        if not self.registered:
            raise ContractViolation("Function must be called after player.register()!")
        if self.color:
            raise ContractViolation("Cannot call Player.place() again until game ends!")
        if not RuleChecker.is_valid_color(color):
            raise ContractViolation("Invalid color provided: {}".format(color))
        self.color = color
        if not RuleChecker.is_legal_initial_board(board, self.color):
            raise ContractViolation("Invalid initial board provided: {}".format(board))
        self.board.set_board(board)
        # TODO: potential contract needed to ensure set_board is called at start of every turn for player
        return self.strategy.get_placements(self.board, self.color)

    def play(self, board):
        """
        Returns the strategized play a player wants to execute on a given turn.

        :param list board:
        :return: a play (as defined above)
        :rtype: list
        """
        if not self.color:
            raise ContractViolation("Function must be called after player.place()!")
        if not RuleChecker.is_legal_board(board):
            raise ContractViolation("Invalid board provided: {}".format(board))
        self.board.set_board(board)
        play = self.strategy.get_play(self.board, self.color)
        print("sending play", play)  # debug
        return play

    def notify(self, winner_name):
        """
        Notifies the player with the winner of the Santorini game.

        CONTRACT:
         - can only be called once per game
         - must be the last function to be called by an object that implements PlayerInterface.

        :param str winner_name: Name of the winner of the Santorini game
        :return: An acknowledgement string of "OK"
        :rtype: str
        """
        # resetting interaction protocol contracts for future games
        self.board = Board()
        self.color = None
        print("{} has won the game!".format(winner_name))  # debug
        print("------------------------------------------------")  # debug
        return "OK"

    def get_name(self):
        """
        :return: this player's name
        :rtype: str
        """
        return self.name
