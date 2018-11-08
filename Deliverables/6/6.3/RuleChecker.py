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
    def is_legal_play(board, worker, directions):
        """
        :param Board board:
        :param string worker:
        :param list directions:
        :return: `True` if play is legal, `False` otherwise
        :rtype: bool
        """
        build_dir = None
        if len(directions) == 1:
            move_dir = directions[0]
        elif len(directions) == 2:
            move_dir, build_dir = directions
        else:
            raise ContractViolation("Too many/few directions provided.")

        if RuleChecker.is_valid_move(board, worker, move_dir):
            if RuleChecker.is_winning_move(board, worker, move_dir):
                if build_dir is None:  # checking for win
                    return True
                else:
                    return False
            elif build_dir is None:
                return False
            board.move(worker, move_dir)
            if RuleChecker.is_valid_build(board, worker, build_dir):
                return_val = True
            else:
                return_val = False
            board.move(worker, board.get_opposite_direction(move_dir))  # undo the move
            return return_val
        else:
            return False

    # ADDED FUNCTION
    @staticmethod
    def is_legal_placement(board, placement):
        """
        Checks the validity of a placement.

        :param list board: A board (as defined in the documentation of Board).
        :param list placement: A tuple of integers denoting the row and column for the worker to be placed.
        :return: 'True' if the placement is valid, else 'False'.
        :rtype: bool
        """
        if (not isinstance(placement, list)
                or len(placement) != 2
                or not all(isinstance(index, int) for index in placement)):
            raise ContractViolation("Expected a tuple of integers. Received {}".format(placement))
        row = placement[0]
        col = placement[1]
        if not 0 <= row < len(board) or not 0 <= col < len(board[0]):
            return False
        if isinstance(board[row][col], list):
            return False
        return True

    @staticmethod
    def is_legal_initial_board(board, color):
        """
        Checks the validity of an initial board.

        :param list board: A board (as defined in the documentation of Board).
        :param string color: A color (as defined in the documentation of Referee).
        :return: 'True' if the board is a valid initial board, else 'False'.
        :rtype: bool
        """
        if not RuleChecker.is_valid_color(color):
            raise ContractViolation("Invalid color provided: {}".format(color))
        unset_workers = [color + "1", color + "2"]
        return RuleChecker.is_legal_board(board, unset_workers, 0)

    @staticmethod
    def is_legal_board(board, unset_workers=[], max_height=4):
        """
        Checks the validity of a board.

        :param list board: A board (as defined in the documentation of Board).
        :param list unset_workers: A list of workers (as defined in the documentation of Board) not in the board that
        will be accounted for later (default: empty list).
        :param int max_height: Maximum height (as defined in the documentation of Board) that any cell in the board
        should have (default: 4).
        :return: 'True' if the board is a valid board, else 'False'.
        :rtype: bool
        """
        workers = unset_workers
        for row in range(len(board)):
            for col in range(len(board[0])):
                cell = board[row][col]
                if isinstance(cell, list):
                    cell_height = cell[0]
                    cell_worker = cell[1]
                    max_cell_height = max(max_height, 2)
                    if cell_worker in workers or not RuleChecker.is_valid_worker(cell_worker):
                        return False
                    workers.append(cell_worker)
                else:
                    cell_height = cell
                    max_cell_height = max_height
                if not 0 <=  cell_height <= max_cell_height:
                    return False
        num_workers = len(workers)
        if unset_workers:
            if num_workers != 2 and num_workers != 4:
                return False
        else:
            if num_workers != 4:
                return False
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