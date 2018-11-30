# Note: These are the base rules. To add rules with God Powers, Create new class which inherits from RuleChecker and
# override methods to adjust for God Power rule additions.

from CustomExceptions import ContractViolation


class RuleChecker:

    """
    A class that contains methods to check if the rules of the Santorini game are being followed.

    Definitions:

    play
        `list`: [worker, [direction1, direction2]] or [worker, [direction1]] where direction1 is the direction to move
        and direction2 is the direction to build.
    """

    DIRECTIONS = ("N", "NE", "E", "SE", "S", "SW", "W", "NW")
    COLORS = ("blue", "white")
    WORKERS = (COLORS[0]+"1", COLORS[0]+"2", COLORS[1]+"1", COLORS[1]+"2")

    @staticmethod
    def is_winning_move(board, worker, direction):
        if not RuleChecker.is_valid_worker(worker) or not RuleChecker.is_valid_direction(direction):
            raise ContractViolation("Invalid (or no) worker / direction provided.")
        return board.get_height(worker, direction) == 3

    @staticmethod
    def is_winning_play(board, worker, directions):
        """
        Takes in a play (as specified above) and checks if it's a winning play.

        This entails checking if the `worker` is moving up to height 3, or if the play blocks the opposition player from
        making any moves or builds.

        CONTRACT:
         - `[worker, directions]` must be a legal play.

        :param Board board:
        :param string worker:
        :param list directions:
        :return:
        :rtype: bool
        """
        if not RuleChecker.is_valid_worker(worker):
            raise ContractViolation("Invalid (or no) worker provided.")
        if not all(map(RuleChecker.is_valid_direction, directions)):
            raise ContractViolation("Invalid (or no) directions provided.")
        if not RuleChecker.is_legal_play(board, worker, directions):
            raise ContractViolation("Illegal play passed into is_winning_play: {}".format([worker, directions]))

        color = worker[:-1]
        available_colors = list(RuleChecker.COLORS)
        available_colors.remove(color)
        opp_color = available_colors[0]

        if len(directions) == 1:  # must be winning, since one direction is only legal in the winning case
            return True
        else:
            opp_cannot_play = False
            move_dir, build_dir = directions

            # simulate play
            board.move(worker, move_dir)
            board.build(worker, build_dir)

            # commented out to avoid circular imports
            # opposition_player_legal_plays = Strategy.get_legal_plays(board, opp_color)

            # if not opposition_player_legal_plays:
            #     opp_cannot_play = True

            # undo play
            board.undo_build(worker, build_dir)
            board.move(worker, board.get_opposite_direction(move_dir))

            return opp_cannot_play

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
    def is_valid_placement(placements):
        """
        Checks the format of a set of placements.

        :param list placements: A tuple of placements.
        :return: 'True' if the placement format is valid, else 'False'.
        :rtype: bool
        """
        if isinstance(placements, list) and len(placements) == 2:
            for placement in placements:
                if (not isinstance(placement, list)
                        or len(placement) != 2
                        or not all(isinstance(i, int) for i in placement)):
                    return False
            return True
        return False

    @staticmethod
    def is_valid_play(play):
        """
        Checks the format of a play.

        :param list play: A tuple of a string and a list of directions denoting a play.
        :return: 'True' if the play format is valid, else 'False'.
        :rtype: bool
        """
        if isinstance(play, list) and len(play) == 2:
            worker, directions = play
            if ((isinstance(worker, str) and
                 isinstance(directions, list) and
                 0 < len(directions) < 3 and
                 all(RuleChecker.is_valid_direction(direction) for direction in directions))):
                return True
        return False

    @staticmethod
    def is_legal_placement(board, placement):
        """
        Checks the validity of a placement.

        :param Board board: A board object.
        :param list placement: A tuple of integers denoting the row and column for the worker to be placed.
        :return: 'True' if the placement is valid, else 'False'.
        :rtype: bool
        """
        row, col = placement
        board_height, board_width = board.get_dimensions()
        if not 0 <= row < board_height or not 0 <= col < board_width or board.has_worker(row, col):
            return False
        return True

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

    @staticmethod
    def is_valid_board(board):
        """
        Checks the format of a board.

        :param list board: A board (as defined in the documentation of Board).
        :return: 'True' if the board format is valid, else 'False'.
        :rtype: bool
        """
        if ((not isinstance(board, list) or
             not all(isinstance(row, list) and len(board) == len(row) for row in board))):
            return False
        for row_count in range(len(board)):
            for col_count in range(len(board[0])):
                cell = board[row_count][col_count]
                if not isinstance(cell, int):
                    if ((not isinstance(cell, list) or
                         len(cell) != 2 or
                         not isinstance(cell[0], int) or
                         not isinstance(cell[1], str))):
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
    def is_legal_board(board, unset_workers=None, max_height=4):
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
        if not unset_workers:
            workers = []
        else:
            workers = unset_workers
        for row in range(len(board)):
            for col in range(len(board[0])):
                cell = board[row][col]
                if isinstance(cell, list):
                    cell_height, cell_worker = cell
                    max_cell_height = min(max_height, 2)
                    if cell_worker in workers or not RuleChecker.is_valid_worker(cell_worker):
                        return False
                    workers.append(cell_worker)
                else:
                    cell_height = cell
                    max_cell_height = max_height
                if not 0 <= cell_height <= max_cell_height:
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
