from Board import Board
from RuleChecker import RuleChecker
from Strategy import Strategy
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

    def __init__(self, name, num_looks_ahead=1):
        """

        :param string name: the name of the Santorini player.
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
        if not isinstance(name, str):
            raise ContractViolation("Name must be a string!")
        if not isinstance(num_looks_ahead, int) or num_looks_ahead < 1:
            raise ContractViolation("num_looks_ahead must be a positive integer! Given: {}".format(num_looks_ahead))
        self.name = name
        self.board = Board()
        self.num_looks_ahead = num_looks_ahead
        self.color = None

        # shadow state
        self.registered = False

    def register(self):
        """
        Returns the name of the player.

        CONTRACT:
         - Must be the first function to be called after Player is instantiated.
         - Cannot be called more than once.

        :return: the name of the player
        :rtype: string
        """
        if self.registered:
            raise ContractViolation("Cannot call Player.register() again until game ends!")
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
        return Strategy.get_placements(self.board, self.color)

    def play(self, board):
        """
        Returns the strategized play a player wants to execute on a given turn.

        :param list board:
        :param int num_moves_ahead:
        :return: a play (as defined above)
        :rtype: list
        """
        if not self.color:
            raise ContractViolation("Function must be called after player.place()!")
        if not RuleChecker.is_legal_board(board):
            raise ContractViolation("Invalid board provided: {}".format(board))
        self.board.set_board(board)
        return Strategy.get_plays(self.board, self.color, self.num_looks_ahead)

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
        return "OK"

    def check_board(self, board):
        """

        :param board:
        :return:
        :type: bool
        """
        for color in RuleChecker.COLORS:
            if color != self.color:
                opp_color = color

        if RuleChecker.is_legal_initial_board(self.board.board, self.color):

            placements = Strategy.get_placements(self.board, self.color)
            for count, placement in enumerate(placements, 1):
                row, col = placement
                self.board.place_worker(row, col, self.color + str(count))

            if RuleChecker.is_legal_board(self.board.board):

                for opp_play in Strategy.get_legal_plays(self.board, opp_color):
                    worker, directions = opp_play
                    move_dir, build_dir = directions
                    self.board.move(worker, move_dir)
                    self.board.build(worker, build_dir)

                    if board == self.board.board:
                        return True

                    self.board.undo_build(worker, build_dir)
                    self.board.move(worker, Board.get_opposite_direction(move_dir))

                return False

            else:

                rows, cols = self.board.get_dimensions()
                for row_count in range(rows):
                    for col_count in range(cols):
                        prev_cell = self.board.board[row_count][col_count]
                        curr_cell = board[row_count][col_count]
                        if prev_cell != curr_cell:
                            if isinstance(prev_cell, list):
                                return False
                            if prev_cell != curr_cell[0]:
                                return False

                return True

        else:

            for play in Strategy.get_legal_plays(self.board, self.color):
                worker, directions = play
                move_dir, build_dir = directions
                self.board.move(worker, move_dir)
                self.board.build(worker, build_dir)

                for opp_play in Strategy.get_legal_plays(self.board, opp_color):
                    opp_worker, opp_directions = opp_play
                    opp_move_dir, opp_build_dir = opp_directions
                    self.board.move(opp_worker, opp_move_dir)
                    self.board.build(opp_worker, opp_build_dir)

                    if board == self.board.board:
                        return True

                    self.board.undo_build(opp_worker, opp_build_dir)
                    self.board.move(opp_worker, Board.get_opposite_direction(opp_move_dir))

                self.board.undo_build(worker, build_dir)
                self.board.move(worker, Board.get_opposite_direction(move_dir))

            return False
