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
        `tuple` of `int`. `(row, col)`. A position is valid if `row` and `col` are in range [0,5].

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

    def __init__(self):
        """
        Constructor. Initializes `board` member variable to `None`.
        `board` member variable simply stores the board for other functions to easily access.
        """
        pass

    def set_board(self, board_obj):
        """
        Assigns the passed in board to the `board` member variable.

        :param list board_obj: a board (as defined above).
        :return: No value returned.
        :rtype: void.
        """
        pass

    def neighboring_cell_exists(self, worker, direction):
        """
        Checks if the cell adjacent to the worker's position in the specified direction exists.

        A cell exists if it's position is within the bounds of the board, i.e. it is a valid position as defined above.

        :param string worker: a worker (as defined above).
        :param string direction: a direction (as defined above).
        :return: `True` if cell adjacent in the specified direction exists, else `False`.
        :rtype: bool
        """
        pass

    def get_height(self, worker, direction):
        """
        Returns the height of the cell adjacent to the worker's position in the specified direction.

        :param string worker: a worker (as defined above).
        :param string direction: a direction (as defined above).
        :return: the height of the cell adjacent to the worker's position in the specified direction.
        :rtype: int
        """
        pass

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
        pass

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
        pass

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
        pass

    def _get_worker_position(self, worker):
        """
        Returns the position of the given worker and the height at that position as one tuple of
        the form `(row, col, height)` by iterating through the the cells in `self.board`.

        :param string worker: a worker (as defined above).
        :return: the position of the given worker (as specified above) and the height at that position as one tuple of
        the form `(row, col, height)`.
        :rtype: tuple of ints
        """
        pass

    @staticmethod
    def _get_adj_cell(worker_row, worker_col, direction_string):
        """
        :param int worker_row: `row` in the worker's position (as defined above).
        :param int worker_col: `col` in the worker's position (as defined above).
        :param string direction_string: `a direction (as defined above).
        :return: the position adjacent to the position denoted by (worker_row, worker_col) in the specified direction.
        :rtype: tuple of ints
        """
        pass

    def _is_valid_move(self, worker, direction):
        """
        Checks if a move to the cell adjacent to the given worker's cell in the specified direction is valid.
        A move is valid if the following are true:
         - the cell being moved to exists
         - the cell being moved to is not occupied
         - the height of the cell being moved to is not 4
         - the height of the cell being moved to - the height of the worker's cell <= 1


        :param string worker: a worker (as defined above).
        :param string direction: a direction (as defined above).
        :return: Boolean denoting if move is valid or not
        :rtype: bool
        """
        pass

    def _is_valid_build(self, worker, direction):
        """
        Checks if a build in the cell adjacent to the given worker's cell in the specified direction is valid.
        A build is valid if the following are true:
         - the cell being built on exists
         - the cell being built on is not occupied
         - the height of the cell being built on is not 4.

        :param string worker: a worker (as defined above).
        :param string direction: a direction (as defined above).
        :return: `True` if build is valid, else `False`
        :rtype: bool
        """
        pass
