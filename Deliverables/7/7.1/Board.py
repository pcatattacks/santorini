import json
from RuleChecker import RuleChecker
from CustomExceptions import ContractViolation
from copy import deepcopy


# TODO: how do we feel about a helper function to return the len of worker_positions, for use in RuleChecker functions


class Board:
    """
    A class to maintain the state of a Santorini board and perform commands to change, or query, the board state.

    Definitions:

    board
        `list` of rows of length 5. See 'row'.

    row
        `list` of cells of length 5. See 'cell'

    cell
        Either:
         - height. See 'height'.
         - `list` of [height, worker]. See 'worker'.

        A cell's position denotes the indices needed to access the cell via `self.board`. See 'position'.

    worker
        `string` which is either "blue1", "blue2", "white1", "white2".

        A worker position denotes the indices needed to access the cell in which the worker is
        contained, via `self.board`.

    height
        `int` in range [0, 4].

    position
        `tuple` of `int`. `(row, col)`. A position is valid if `row` and `col` are in range [0,4].

    direction
        `string` which is either "N", "NE", "E", "SE", "S", "SW", "W", "NW".

        An adjacent cell in a direction relative to a position corresponds to the following positions for each
        direction:
         - "N": position + (-1, 0)
         - "S": position + (1, 0)
         - "E": position + (0, 1)
         - "W": position + (0, -1)
         - "NE": position + (-1, 1)
         - "NW": position + (-1, -1)
         - "SE": position + (1, 1)
         - "SW": position + (1, -1)

    """

    DEFAULT_DIMENSIONS = (5, 5)

    def __init__(self):
        """
        Constructor. Initializes `board` member variable to `None`.
        `board` member variable simply stores the board for other functions to easily access.
        """
        self.board = self._create_empty_board()
        self.worker_positions = {}  # key-value pair of worker : position

    def get_dimensions(self):
        """
        CONTRACT:
         - cannot be called before set_board() has been called.

        :return: The dimensions of the board member variable in format (num_rows, num_cols)
        :rtype: tuple
        """
        if not self.board:
            raise ContractViolation("Cannot get dimensions if Board.board member variable has not been set!")
        return len(self.board), len(self.board[0])

    def set_board(self, board_obj):
        """
        Assigns the passed in board to the `board` member variable.

        :param list board_obj: a board (as defined above).
        :return: No value returned.
        :rtype: void.
        """
        # TODO: use is_valid_board or leave it to board owner
        self.board = board_obj
        for r, row in enumerate(self.board):
            for c, cell in enumerate(row):
                if isinstance(cell, list):
                    worker = cell[1]
                    self.worker_positions[worker] = (r, c, cell[0])

    def neighboring_cell_exists(self, worker, direction):
        """
        Checks if the cell adjacent to the worker's position in the specified direction exists.

        A cell exists if it's position is within the bounds of the board, i.e. it is a valid position as defined above.

        :param string worker: a worker (as defined above).
        :param string direction: a direction (as defined above).
        :return: `True` if cell adjacent in the specified direction exists, else `False`.
        :rtype: bool
        """
        if not RuleChecker.is_valid_worker(worker) or not RuleChecker.is_valid_direction(direction):
            raise ContractViolation("Invalid (or no) worker / direction provided.")
        worker_row, worker_col, worker_height = self.get_worker_position(worker)
        adj_cell_row, adj_cell_col = Board._get_adj_cell(worker_row, worker_col, direction)
        return 0 <= adj_cell_row < len(self.board) and 0 <= adj_cell_col < len(self.board[0])

    def get_height(self, worker, direction):
        """
        Returns the height of the cell adjacent to the worker's position in the specified direction.

        :param string worker: a worker (as defined above).
        :param string direction: a direction (as defined above).
        :return: the height of the cell adjacent to the worker's position in the specified direction.
        :rtype: int
        """
        if not RuleChecker.is_valid_worker(worker) or not RuleChecker.is_valid_direction(direction):
            raise ContractViolation("Invalid (or no) worker / direction provided.")
        if self.neighboring_cell_exists(worker, direction):
            worker_row, worker_col, worker_height = self.get_worker_position(worker)
            adj_cell_row, adj_cell_col = Board._get_adj_cell(worker_row, worker_col, direction)
            cell = self.board[adj_cell_row][adj_cell_col]
            if isinstance(cell, list):
                return cell[0]
            else:
                return cell

    def is_occupied(self, worker, direction):
        """
        Checks if the cell adjacent to the worker's position in the specified direction is occupied.

        A cell is occupied if it is a `list` of [height, worker].

        :param string worker: a worker (as defined above).
        :param string direction: a direction (as defined above).
        :return: `True` if the cell adjacent to the worker's position in the specified direction exists and is occupied,
        `False`, if cell is unoccupied. Behaviour unspecified if cell adjacent cell doesn't exist.
        :rtype: bool, void
        """
        if not RuleChecker.is_valid_worker(worker) or not RuleChecker.is_valid_direction(direction):
            raise ContractViolation("Invalid (or no) worker / direction provided.")
        if self.neighboring_cell_exists(worker, direction):
            worker_row, worker_col, cell_height = self.get_worker_position(worker)
            adj_cell_row, adj_cell_col = self._get_adj_cell(worker_row, worker_col, direction)
            return self.has_worker(adj_cell_row, adj_cell_col)

    def build(self, worker, direction):
        """
        Increases the height of the cell adjacent to the worker's position in the specified direction by 1, if all of
        the following are true:
         - the cell being built on exists
         - the cell being built on is not occupied
         - the height of the cell being built on is not 4.

        :param string worker: a worker (as defined above).
        :param string direction: a direction (as defined above).
        :return: a board (as specified above) edited to reflect the build. Nothing if move is invalid.
        :rtype: list, void
        """
        if not RuleChecker.is_valid_worker(worker) or not RuleChecker.is_valid_direction(direction):
            raise ContractViolation("Invalid (or no) worker / direction provided.")
        worker_row, worker_col, worker_height = self.get_worker_position(worker)
        adj_cell_row, adj_cell_col = self._get_adj_cell(worker_row, worker_col, direction)
        self.board[adj_cell_row][adj_cell_col] += 1
        return self.board

    def undo_build(self, worker, direction):
        """
        Decreases the height of the cell adjacent to the worker's position in the specified direction by 1, if all of
        the following are true:
         - the cell being destroyed on exists
         - the cell being destroyed on is not occupied
         - the height of the cell being built on is not 0.

        Note: should not be used outside the `Strategy` component.

        :param string worker: a worker (as defined above).
        :param string direction: a direction (as defined above).
        :return: a board (as specified above) edited to reflect the undoing of the build. Nothing if move is invalid.
        :rtype: list, void
        """
        if not RuleChecker.is_valid_worker(worker) or not RuleChecker.is_valid_direction(direction):
            raise ContractViolation("Invalid (or no) worker / direction provided.")
        worker_row, worker_col, worker_height = self.get_worker_position(worker)
        adj_cell_row, adj_cell_col = self._get_adj_cell(worker_row, worker_col, direction)
        self.board[adj_cell_row][adj_cell_col] -= 1
        return self.board

    def move(self, worker, direction):
        """
        Moves the specified worker from it's cell to the cell adjacent to the worker's existing position in the
        specified direction, if all of the following are true:
         - the cell being moved to exists
         - the cell being moved to is not occupied
         - the height of the cell being moved to is not 4
         - the height of the cell being moved to - the height of the worker's cell <= 1

        A move entails:
        - editing the specified worker's cell from `[height, worker]` to `height`
        - editing the adjacent cell from it's `height` to `[height, worker]`.

        :param string worker: a worker (as defined above).
        :param string direction: a direction (as defined above).
        :return: a board (as specified above) edited to reflect the build. Nothing if move is invalid.
        :rtype: list, void
        """
        if not RuleChecker.is_valid_worker(worker) or not RuleChecker.is_valid_direction(direction):
            raise ContractViolation("Invalid (or no) worker / direction provided.")
        worker_row, worker_col, worker_height = self.get_worker_position(worker)
        adj_cell_row, adj_cell_col = self._get_adj_cell(worker_row, worker_col, direction)
        adj_cell_height = self.board[adj_cell_row][adj_cell_col]
        self.board[adj_cell_row][adj_cell_col] = [adj_cell_height, worker]
        self.board[worker_row][worker_col] = worker_height
        self.worker_positions[worker] = (adj_cell_row, adj_cell_col, adj_cell_height)
        return self.board

    def get_worker_position(self, worker):
        """
        Returns the position of the given worker and the height at that position as one tuple of
        the form `(row, col, height)` by iterating through the the cells in `self.board`.

        :param string worker: a worker (as defined above).
        :return: the position of the given worker (as specified above) and the height at that position as one tuple of
        the form `(row, col, height)`.
        :rtype: tuple of ints
        """
        if not RuleChecker.is_valid_worker(worker):
            raise ContractViolation("Invalid worker provided: {}".format(worker))
        # Note: would use a dictionary for O(1) access if the board wasn't being reset with every command.
        if worker in self.worker_positions:
            return self.worker_positions[worker]
        else:
            raise ContractViolation("Worker does not exist in worker_dictionary!")

    def get_cell_height(self, row, col):
        if self.has_worker(row, col):
            return self.board[row][col][0]
        return self.board[row][col]

    def get_cell_worker(self, row, col):
        if self.has_worker(row, col):
            return self.board[row][col][1]
        return None

    def has_worker(self, row, col):
        """
        Returns whether a cell has a worker present in it or not.

        :param int row: `row` in a position (as defined above).
        :param int col: `col` in a position (as defined above).
        :return: `True` if self.board[row][col] is instance of `list`, `False` otherwise.
        :rtype: bool
        """
        return isinstance(self.board[row][col], list)

    def place_worker(self, row, col, worker):
        """
        Places a worker at the cell at position (row, col)

        :param int row: `row` in a position (as defined above).
        :param int col: `col` in a position (as defined above).
        :param string worker: a worker (as defined above).
        :rtype: void
        """
        if not RuleChecker.is_valid_worker(worker):
            raise ContractViolation("Invalid worker provided: {}".format(worker))
        if self.has_worker(row, col):
            raise IllegalMove("Cannot place worker in occupied cell!")
        height = self.board[row][col]
        self.board[row][col] = [height, worker]
        self.worker_positions[worker] = (row, col, height)

    @staticmethod
    def _create_empty_board(num_rows=DEFAULT_DIMENSIONS[0], num_cols=DEFAULT_DIMENSIONS[1]):
        """
        :param int num_rows: the number of rows the board should have.
        :param int num_cols: the number of columns the board should have.
        :return: an empty board (as defined above) with the given number of rows and columns.
        :rtype: list
        """
        if num_rows < 1 or num_cols < 1:
            raise ValueError("A board must have dimensions of at least 1x1.")
        board = []
        for row_count in range(num_rows):
            row = []
            for col_count in range(num_cols):
                row.append(0)
            board.append(row)
        return board

    @staticmethod
    def _get_adj_cell(worker_row, worker_col, direction_string):
        """
        :param int worker_row: `row` in the worker's position (as defined above).
        :param int worker_col: `col` in the worker's position (as defined above).
        :param string direction_string: `a direction (as defined above).
        :return: the position adjacent to the position denoted by (worker_row, worker_col) in the specified direction.
        :rtype: tuple of ints
        """
        if not RuleChecker.is_valid_direction(direction_string):
            raise ValueError("Invalid Direction string provided: {}".format(direction_string))
        if "N" in direction_string:
            worker_row -= 1
        elif "S" in direction_string:
            worker_row += 1
        if "E" in direction_string:
            worker_col += 1
        elif "W" in direction_string:
            worker_col -= 1
        return worker_row, worker_col

    @staticmethod
    def get_opposite_direction(direction_string):
        """
        Gets the opposite direction to the direction string.

        :param string direction_string: `a direction (as defined above).
        :return:
        """
        if not RuleChecker.is_valid_direction(direction_string):
            raise ValueError("Invalid Direction string provided: {}".format(direction_string))
        opp_dir = ""
        if "N" in direction_string:
            opp_dir += "S"
        elif "S" in direction_string:
            opp_dir += "N"
        if "E" in direction_string:
            opp_dir += "W"
        elif "W" in direction_string:
            opp_dir += "E"
        return opp_dir

    def extract_json_board(self):
        """
        Returns a JSON representation of the current board state.

        :return: json array
        :rtype: string
        """
        return json.dumps(self.board)


    def extract_board(self):
        """
        Returns a deepcopy of the current board state.

        :return: board list
        :rtype: list
        """
        return deepcopy(self.board)


# TODO: do we still want this defined here
class IllegalMove(Exception):
    pass
