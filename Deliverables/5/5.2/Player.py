from Board import Board
from RuleChecker import RuleChecker


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
        Sets the `color` member variable to the parameter `color`.

        CONTRACT:
         - Must be the first function to be called after Player is instantiated.
         - Cannot be called more than once.

        :param string color: a color (as defined above)
        :return:
        :rtype: void
        """
        if not RuleChecker.is_valid_color(color):
            raise ValueError("Invalid color provided: {}".format(color))
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

        :param Board board: an instance of Board (refer to documentation of Board class).
        :return: `list` of [position1, position2] denoting the position of the player's 1st and 2nd worker respectively.
        See `position`, `worker` in documentation of Board.py.
        :rtype: list
        """
        if not self.color:
            raise ContractViolation("Function must be called after player.register()!")
        if not RuleChecker.is_valid_initial_board(board, self.color):
            raise ContractViolation("Invalid initial board provided: {board}".format(board))
        self.board.set_board(board)
        # TODO: potential contract needed to ensure set_board is called at start of every turn for player
        return Strategy.get_placements(self.board, self.color)

    def play(self, board):
        """
        Returns the strategized play a player wants to execute on a given turn.

        :return: a play (as defined above)
        :rtype: list
        """
        self.board.set_board(board)
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
        `list`: [worker, [direction1, direction2]] or [worker, [direction1]] where direction1 is the direction to move
        and direction2 is the direction to build.

    """
    # TODO: Discuss
    # Should each player have it's own instance of the strategy class? By having both players use static methods of
    # the strategy class (and passing in color as a parameter), we'll have to write a lot of if-statements and
    # additional logic in the strategy class so it can make conditional plays based on for which color it outputs a
    # strategy. But we'll have to do this anyway.
    # This also means that an opposing player can get another player's strategy, by just passing in the other color.
    # This enables cheating.
    # If we make Strategy a member variable of Player, and instantiate it with the color passed into player, we can add
    # functionality for god powers etc later. We're probably going to extend the Strategy class if we create God powers,
    # for each God power. if so, we'll have to always find which GodPowerStrategy class to find and use, rather than
    # just finding it once and storing it. Not sure.

    # TODO: Discuss
    # by making Strategy a public class with static member functions, we aren't enabling any cheating are we? or should
    # strategy be a private class within player? that doesn't make sense to me. having some of Strategy's function's
    # exposed doesn't allow any manipulation to variables that represent the game state, so it should be fine (I think).

    @staticmethod
    def get_placements(board, color):
        """
        Returns worker placements of given color, by scheme of choosing the first two unoccupied corner cells, starting
        from top left, in the clockwise direction.

        :param Board board: an instance of Board (refer to documentation of Board class).
        :param string color: color (as defined above)
        :return: `list` of [position1, position2] where position1 and position2 are positions of the first and second
        worker respectively. See `worker` and `position` in Board.py documentation.
        :rtype: list
        """
        if not RuleChecker.is_valid_initial_board(board, color):
            raise ContractViolation("Invalid initial board provided to Strategy class: {board}".format(board))
        corners = ([0, 0], [0, len(board[0])-1], [len(board)-1, len(board[0])-1], [len(board)-1, 0])
        placements = []
        for corner in corners:
            if not board.has_worker(*corner):
                placements.append(corner)
            if len(placements) == 2:
                break
        assert len(placements) == 2  # shouldn't needed since we're checking that the board is valid at the start, but
        # may as well
        return placements

    @staticmethod
    def get_play(board, color):
        """
        Returns the optimal play for a given board and a color that identifies the player.

        :param Board board: an instance of Board (refer to documentation of Board class).
        :param string color: color (as defined above)
        :return: a play (as defined above)
        :rtype: list
        """
        pass

    @staticmethod
    def get_plays(board, color):
        """
        Returns a list of all possible legal plays that cannot not result in the opposing player winning with the next
        move.

        :param Board board: an instance of Board (refer to documentation of Board class).
        :param string color: color (as defined above)
        :return: a `list` of legal plays (as defined above)
        :rtype: `list`
        """
        # algorithm - a basic DFS
        #
        # R <- []
        # P <- get legal plays for current player
        # for p in P:
        #   simulate play - so edit the board
        #   Q <- get legal plays for opposing player
        #   for q in Q:
        #       if q not is winning_play: # TODO - will have to write a function in RuleChecker for this
        #           R.append(p)
        #   undo play (if you're using the same board - don't need if we're deepcopy-ing the board for each play)
        pass

    @staticmethod
    def _get_legal_plays(board, color):
        """
        Returns a list of all possible legal plays for a player of the given color.

        :param Board board: an instance of Board (refer to documentation of Board class).
        :param string color: color (as defined above)
        :return: a `list` of legal plays (as defined above)
        :rtype: list
        """
        # TODO
        pass


class ContractViolation(Exception):
    pass
