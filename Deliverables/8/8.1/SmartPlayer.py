from Board import Board
from RuleChecker import RuleChecker
from Strategies import GreedyStrategy
from CustomExceptions import ContractViolation, IllegalPlay
from Player import Player
import json


class SmartPlayer(Player):

    def __init__(self, name=None, strategy=GreedyStrategy()):
        super().__init__(name, strategy)
        self.placements = None

    def place(self, board, color):
        placements = super().place(board, color)
        self.placements = placements
        return placements

    def play(self, board):
        if not self.color:
            raise ContractViolation("Function must be called after player.place()!")
        if not RuleChecker.is_legal_board(board):
            raise ContractViolation("Invalid board provided: {}".format(board))
        if not self._check_board(board):
            raise IllegalPlay("Player provided with a cheating board.")
        print("cheater checking...")  # debug
        return super().play(board)

    def _check_board(self, curr_board):  # TODO - there's a bug here, need to test. commenting out usage for now
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
            for count, placement in enumerate(self.placements, 1):
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
            for own_play in self.strategy.get_legal_plays(self.board, self.color):
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
        :param str color: A color (as defined in the documentation of Referee).
        :return: 'True' if the current board can be achieved in one move from the previous board, else 'False'.
        :rtype: bool
        """
        # iterate through a player's plays to check for a matching resulting board
        for play in self.strategy.get_legal_plays(prev_board, color):
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
