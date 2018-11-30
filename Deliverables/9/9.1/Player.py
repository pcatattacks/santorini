from Board import Board
from RuleChecker import RuleChecker
from Strategy import Strategy
from CustomExceptions import ContractViolation, IllegalPlay
from PlayerInterface import PlayerInterface
import json


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
        self.registered = False  # shadow state

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
        :param string color: A color (as defined in the documentation of Referee).
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
        if not self._check_board(board):
            raise IllegalPlay("Player provided with a cheating board.")
        self.board.set_board(board)
        return self._select_play(Strategy.get_plays(self.board, self.color, self.num_looks_ahead))

    # TODO: has to reset member variables for next game
    def notify(self, winner_name):  # TODO: remove unnecessary parameter?
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

    def _check_board(self, curr_board):
        """
        Ensures that a received board is within 2 plays of the board currently stored in the Player.

        :param list curr_board: A board (as defined in the documentation of Board).
        :return: 'True' if board is valid given previous board, else 'False'.
        :type: bool
        """
        opp_color = RuleChecker.COLORS[0] if self.color == RuleChecker.COLORS[1] else RuleChecker.COLORS[1]
        # if player's last turn was a placement
        # TODO: can't use json.dumps data without json.loads first, so either we use that or a deepcopy function
        if RuleChecker.is_legal_initial_board(json.loads(self.board.extract_json_board()), self.color):
            # apply placements to currently stored board
            placements = Strategy.get_placements(self.board, self.color)
            for count, placement in enumerate(placements, 1):
                row, col = placement
                self.board.place_worker(row, col, self.color + str(count))
            # if player placed workers second, check possible opponent plays
            if RuleChecker.is_legal_board(json.loads(self.board.extract_json_board())):
                return self._check_turn(self.board, curr_board, opp_color)
            # else expect a 4-worker initial board with our workers in the same place
            else:
                unset_workers = [opp_color + "1", opp_color + "2"]
                rows, cols = self.board.get_dimensions()
                # iterate through the boards to find differences
                for row_count in range(rows):
                    for col_count in range(cols):
                        # TODO: maybe create a get_cell function that's just a wrapper for get_cell_height and
                        # get_cell_worker? it would be the 3 lines of code below except the last would be returned
                        cell_height = self.board.get_cell_height(row_count, col_count)
                        cell_worker = self.board.get_cell_worker(row_count, col_count)
                        prev_cell = [cell_height, cell_worker] if cell_worker else cell_height
                        curr_cell = curr_board[row_count][col_count]
                        if prev_cell != curr_cell:
                            # if the cell used to have a worker but changed, or if the cell's height changed,
                            # or if the worker in the new cell is not one of the opponent's valid workers, return False
                            if ((isinstance(prev_cell, list)
                                 or isinstance(curr_cell, int)
                                 or curr_cell[1] not in unset_workers)):
                                return False
                            # remove seen opponent worker for unset_workers
                            unset_workers.remove(curr_cell[1])
                return True
        # else if player has already placed, checks possible sets of two turns
        else:
            # iterate through possible own plays, then for each check possible opponent plays for a board match
            for own_play in Strategy.get_legal_plays(self.board, self.color):
                own_worker, own_directions = own_play
                # ignore wins as they did not occur
                if len(own_directions) == 1:
                    continue
                own_move_dir, own_build_dir = own_directions
                # apply play to self.board
                self.board.move(own_worker, own_move_dir)
                self.board.build(own_worker, own_build_dir)
                # check opponent plays on modified board
                if self._check_turn(self.board, curr_board, opp_color):
                    return True
                # reverse play
                self.board.undo_build(own_worker, own_build_dir)
                self.board.move(own_worker, Board.get_opposite_direction(own_move_dir))
            return False

    # TODO: possibly make this function return a set of plays so that check_board can call it twice and apply and
    # reverse the plays itself, may possibly reduce some code redundancy
    def _check_turn(self, prev_board, curr_board, color):
        """
        Ensures that a previous board is within 1 play of a given board.

        :param Board prev_board: A Board object (see documentation for Board).
        :param list curr_board: A board (as defined in the documentation of Board).
        :param string color: A color (as defined in the documentation of Referee).
        :return: 'True' if the current board can be achieved in one move from the previous board, else 'False'.
        :rtype: bool
        """
        # iterate through a player's plays to check for a matching resulting board
        for play in Strategy.get_legal_plays(prev_board, color):
            worker, directions = play
            # ignore wins as they did not occur
            if len(directions) == 1:
                continue
            move_dir, build_dir = directions
            # apply play to prev_board
            prev_board.move(worker, move_dir)
            prev_board.build(worker, build_dir)
            # check for board uniformity
            if json.loads(prev_board.extract_json_board()) == curr_board:
                return True
            # reverse play
            prev_board.undo_build(worker, build_dir)
            prev_board.move(worker, Board.get_opposite_direction(move_dir))
        return False

    def _select_play(self, plays):
        """

        :param list plays:
        :return:
        :rtype: list
        """
        best_score = 0
        best_play = [self.color + "1", ["N"]]
        for play in plays:
            worker, directions = play
            if len(directions) == 1:
                return play
            move_dir, build_dir = directions
            self.board.move(worker, move_dir)
            self.board.build(worker, build_dir)
            score = self._score_board()
            if score > best_score:
                best_score = score
                best_play = play
            self.board.undo_build(worker, build_dir)
            self.board.move(worker, Board.get_opposite_direction(move_dir))
        return best_play

    def _score_board(self):
        """

        :return:
        :rtype: list
        """
        score = 0
        workers = [self.color + "1", self.color + "2"]
        for worker in workers:
            row, col, height = self.board.get_worker_position(worker)
            score += height * 2
            for direction in RuleChecker.DIRECTIONS:
                adj_height = self.board.get_height(worker, direction)
                if adj_height:
                    score += adj_height
        return score

    def get_name(self):
        """

        :return:
        :rtype: string
        """
        return self.name
