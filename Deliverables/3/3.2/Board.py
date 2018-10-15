from enum import Enum


# class Direction(Enum):
#     N = "N"
#     NE = "NE"
#     E = "E"
#     SE = "SE"
#     S = "S"
#     SW = "SW"
#     W = "W"
#     NW = "NW"


# class Worker(Enum):
#     blue1 = "blue1"
#     blue2 = "blue2"
#     white1 = "white1"
#     white2 = "white2"


# class Cell:  # TODO
#
#     def __init__(self):
#         self.height = 0
#         self.worker = False
#
#     def occupied(self):
#         return self.worker
#
#     def update_worker(self, on_or_off):
#         self.worker = on_or_off
#
#     def update_height(self):
#         pass


class Board:

    def __init__(self):
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
        :param direction: a string which is either "N", "NE"...
        :return: Boolean stating whether cell adjacent in the specified direction exists or not.
        """
        worker_row, worker_col, worker_height = self._get_worker_position(worker)
        adj_cell_row, adj_cell_col = Board._get_adj_cell(worker_row, worker_col, direction)
        return 0 <= adj_cell_row <= len(self.board) and 0 <= adj_cell_col <= len(self.board[0])

    def get_height(self, worker, direction):
        """

        :param worker: a string which is either "blue1", "blue2", "white1", "white2"
        :param direction:
        :return: positive integer, [0, 4]
        """
        pass

    def is_occupied(self, worker, direction):
        """

        :param worker:
        :param direction:
        :return: True if the adjacent cell in the given direction exists and is occupied, false, if cell is unoccupied.
        """
        worker_row, worker_col, cell_height = self._get_worker_position(worker)
        if not self.neighboring_cell_exists(worker, direction):
            return  # Behaviour unspecified if cell doesn't exist - look at spec.
        adj_cell_row, adj_cell_col = self._get_adj_cell(worker_row, worker_col, direction)
        return type(self.board[adj_cell_row][adj_cell_col]) == list

    def build(self, worker, direction):
        """
        TODO: add a contract after seeing Piazza reply - check whether valid build or not
        :param worker:
        :param direction:
        :return: JSON representation of a Board
        """
        pass

    def move(self, worker, direction):
        """
        TODO: add a contract after seeing Piazza reply - check whether valid move or not
        :param worker:
        :param direction:
        :return: JSON representation of a Board
        """
        pass

    def _get_worker_position(self, worker):
        """
        :param worker: a string which is either "blue1", "blue2", "white1", "white2".
        :return: returns tuple of (row, col, height) where row, col are elem of [0,5] and height is elem [0,4].
        """
        # Note: would use a dictionary for O(1) access if the board wasn't being reset with every command.
        for r, row in enumerate(self.board):
            for c, cell in enumerate(row):
                if type(cell) == list and cell[1] == worker:
                    return r, c, cell[0]

    @staticmethod
    def _get_adj_cell(worker_row, worker_col, direction_string):
        """

        :param worker_row: int specifying worker's x position
        :param worker_col: int specifying worker's y position
        :param direction_string: a string which is either "N", "NW", ...
        :return: Tuple of (row, col) of the adjacent cell in the specified direction.
        """
        if direction_string == "N":
            return worker_row + 1, worker_col
        elif direction_string == "E":
            return worker_row, worker_col + 1
        elif direction_string == "S":
            return worker_row - 1, worker_col
        elif direction_string == "W":
            return worker_row, worker_col - 1
        elif direction_string == "NE":
            return worker_row + 1, worker_col + 1
        elif direction_string == "SE":
            return worker_row - 1, worker_col + 1
        elif direction_string == "NW":
            return worker_row + 1, worker_col - 1
        elif direction_string == "SW":
            return worker_row - 1, worker_col - 1
        else:
            raise ValueError("Invalid direction string!")

    def _is_valid_move(self, worker, direction):
        """

        :param worker:
        :param direction:
        :return: Boolean denoting if move is valid or not
        """
        pass

    def _is_valid_build(self, worker, direction):
        """

        :param worker:
        :param direction:
        :return: Boolean denoting if build is valid or not
        """
        pass

