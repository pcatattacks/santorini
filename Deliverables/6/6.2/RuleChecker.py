# Note: These are the base rules. To add rules with God Powers, Create new class which inherits from RuleChecker and
# override methods to adjust for God Power rule additions.

from CustomExceptions import ContractViolation


class RuleChecker:

    WORKERS = ("blue1", "blue2", "white1", "white2")
    DIRECTIONS = ("N", "NE", "E", "SE", "S", "SW", "W", "NW")
    COLORS = ("blue", "white")

    @staticmethod
    def is_winning_move(board, worker, direction):
        if not RuleChecker.is_valid_worker(worker) or not RuleChecker.is_valid_direction(direction):
            raise ContractViolation("Invalid (or no) worker / direction provided.")
        return board.get_height(worker, direction) == 3

    @staticmethod
    def is_winning_build(board, worker, direction):
        if not RuleChecker.is_valid_worker(worker) or not RuleChecker.is_valid_direction(direction):
            raise ContractViolation("Invalid (or no) worker / direction provided.")
        # TODO
        pass

    @staticmethod
    def is_winning_play(board, worker, direction):
        if not RuleChecker.is_valid_worker(worker) or not RuleChecker.is_valid_direction(direction):
            raise ContractViolation("Invalid (or no) worker / direction provided.")
        # TODO
        pass

    @staticmethod
    def is_valid_move(board, worker, direction):
        if not RuleChecker.is_valid_worker(worker) or not RuleChecker.is_valid_direction(direction):
            raise ContractViolation("Invalid (or no) worker / direction provided.")
        worker_height = board.get_worker_position(worker)[2]
        adj_cell_height = board.get_height(worker, direction)
        return (board.neighboring_cell_exists(worker, direction)
                and not board.is_occupied(worker, direction)
                and adj_cell_height != 4
                and adj_cell_height - worker_height <= 1)

    @staticmethod
    def is_valid_build(board, worker, direction):
        if not RuleChecker.is_valid_worker(worker) or not RuleChecker.is_valid_direction(direction):
            raise ContractViolation("Invalid (or no) worker / direction provided.")
        adj_cell_height = board.get_height(worker, direction)
        return (board.neighboring_cell_exists(worker, direction)
                and not board.is_occupied(worker, direction)
                and adj_cell_height != 4)

    @staticmethod
    def is_legal_initial_board(board, color):
        """

        :param list board:
        :param string color:
        :return:
        """
        if not RuleChecker.is_valid_color(color):
            raise ContractViolation("Invalid color given: {}".format(color))
        # TODO
        return True

    @staticmethod
    def is_legal_board(board):
        """

        :param list board:
        :return:
        """
        # TODO
        return True

    @staticmethod
    def is_valid_worker(worker):
        return worker in RuleChecker.WORKERS

    @staticmethod
    def is_valid_direction(direction):
        return direction in RuleChecker.DIRECTIONS

    @staticmethod
    def is_valid_color(color):
        return color in RuleChecker.COLORS
