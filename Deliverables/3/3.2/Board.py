class Board:

    def __init__(self):
        """
        # TODO: define all terms and board class
        """
        self.board = None

    def set_board(self, board_obj):
        """
        Sets board member variable to the passed in board object.
        :param board_obj:
        :return: Void.
        """
        self.board = board_obj

    def neighboring_cell_exists(self, worker, direction):
        """

        :param worker: a string which is either "blue1", "blue2", "white1", "white2"
        :param direction: a string which is either "N", "NE", "E", "SE", "S", "SW", "W", "NW".
        :return: Boolean stating whether cell adjacent in the specified direction exists or not.
        """
        worker_row, worker_col, worker_height = self._get_worker_position(worker)
        adj_cell_row, adj_cell_col = Board._get_adj_cell(worker_row, worker_col, direction)
        return 0 <= adj_cell_row < len(self.board) and 0 <= adj_cell_col < len(self.board[0])

    def get_height(self, worker, direction):
        """
        :param worker: a string which is either "blue1", "blue2", "white1", "white2"
        :param direction: a string which is either "N", "NE", "E", "SE", "S", "SW", "W", "NW".
        :return: positive integer, [0, 4] - The Height of the cell on the Board adjacent to the Worker in this Direction
                if a such a cell exists
        """

        if self.neighboring_cell_exists(worker, direction):
            worker_row, worker_col, worker_height = self._get_worker_position(worker)
            adj_cell_row, adj_cell_col = Board._get_adj_cell(worker_row, worker_col, direction)
            cell = self.board[adj_cell_row][adj_cell_col]
            if isinstance(cell, list):
                return cell[0]
            else:
                return cell
        # behaviour unspecified if cell doesn't exist
                
    def is_occupied(self, worker, direction):
        """

        :param worker: a string which is either "blue1", "blue2", "white1", "white2".
        :param direction: a string which is either "N", "NE", "E", "SE", "S", "SW", "W", "NW".
        :return: True if the adjacent cell in the given direction exists and is occupied, false, if cell is unoccupied.
        """
        if self.neighboring_cell_exists(worker, direction):
            worker_row, worker_col, cell_height = self._get_worker_position(worker)
            adj_cell_row, adj_cell_col = self._get_adj_cell(worker_row, worker_col, direction)
            return isinstance(self.board[adj_cell_row][adj_cell_col], list)
        # behaviour unspecified if cell doesn't exist

    def build(self, worker, direction):
        """
        TODO: add a contract after seeing Piazza reply - check whether valid build or not
        :param worker: a string which is either "blue1", "blue2", "white1", "white2".
        :param direction: a string which is either "N", "NE", "E", "SE", "S", "SW", "W", "NW".
        :return: Object representation of a Board
        """
        if self._is_valid_build(worker, direction):
            worker_row, worker_col, worker_height = self._get_worker_position(worker)
            adj_cell_row, adj_cell_col = self._get_adj_cell(worker_row, worker_col, direction)
            self.board[adj_cell_row][adj_cell_col] += 1
            return self.board
        # behaviour unspecified if invalid build

    def move(self, worker, direction):
        """
        TODO: add a contract after seeing Piazza reply - check whether valid move or not
        :param worker: a string which is either "blue1", "blue2", "white1", "white2".
        :param direction: a string which is either "N", "NE", "E", "SE", "S", "SW", "W", "NW".
        :return: Object representation of a Board
        """
        if self._is_valid_move(worker, direction):
            worker_row, worker_col, worker_height = self._get_worker_position(worker)
            adj_cell_row, adj_cell_col = self._get_adj_cell(worker_row, worker_col, direction)
            adj_cell_height = self.board[adj_cell_row][adj_cell_col]
            self.board[adj_cell_row][adj_cell_col] = [adj_cell_height, worker]
            self.board[worker_row][worker_col] = worker_height
            return self.board
        # behaviour unspecified if invalid build

    def _get_worker_position(self, worker):
        """
        :param worker: `string` which is either "blue1", "blue2", "white1", "white2".
        :return: returns tuple of (row, col, height) where row, col are elem of [0,5] and height is elem [0,4].
        """
        # Note: would use a dictionary for O(1) access if the board wasn't being reset with every command.
        for r, row in enumerate(self.board):
            for c, cell in enumerate(row):
                if isinstance(cell, list) and cell[1] == worker:
                    return r, c, cell[0]

    @staticmethod
    def _get_adj_cell(worker_row, worker_col, direction_string):
        """

        :param worker_row: `int` specifying worker's x position.
        :param worker_col: `int` specifying worker's y position.
        :param direction_string: `string` which is either "N", "NW", ...
        :return: Tuple of (row, col) of the adjacent cell in the specified direction.
        """
        if direction_string == "N":
            return worker_row - 1, worker_col
        elif direction_string == "E":
            return worker_row, worker_col + 1
        elif direction_string == "S":
            return worker_row + 1, worker_col
        elif direction_string == "W":
            return worker_row, worker_col - 1
        elif direction_string == "NE":
            return worker_row - 1, worker_col + 1
        elif direction_string == "SE":
            return worker_row + 1, worker_col + 1
        elif direction_string == "NW":
            return worker_row - 1, worker_col - 1
        elif direction_string == "SW":
            return worker_row + 1, worker_col - 1
        else:
            raise ValueError("Invalid direction string!")

    def _is_valid_move(self, worker, direction):
        """

        :param worker: a string which is either "blue1", "blue2", "white1", "white2".
        :param direction: a string which is either "N", "NE", "E", "SE", "S", "SW", "W", "NW".
        :return: Boolean denoting if move is valid or not
        """
        worker_height = self._get_worker_position(worker)[2]
        adj_cell_height = self.get_height(worker, direction)
        return self.neighboring_cell_exists(worker, direction) \
            and not self.is_occupied(worker, direction) \
            and adj_cell_height != 4 \
            and adj_cell_height - worker_height <= 1

    def _is_valid_build(self, worker, direction):
        """

        :param worker: a string which is either "blue1", "blue2", "white1", "white2".
        :param direction: a string which is either "N", "NE", "E", "SE", "S", "SW", "W", "NW".
        :return: Boolean denoting if build is valid or not
        """
        adj_cell_height = self.get_height(worker, direction)
        return self.neighboring_cell_exists(worker, direction) \
            and not self.is_occupied(worker, direction) \
            and adj_cell_height != 4
