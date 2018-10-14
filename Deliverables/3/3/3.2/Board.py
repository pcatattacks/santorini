# from enum import Enum
#
# class Direction(Enum):
#     N = "N"
#     NE = "NE"
#     E = "E"
#     SE = "SE"
#     S = "S"
#     SW = "SW"
#     W = "W"
#     NW = "NW"
#
#
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

    def parse_board(self, json_board):
        """
        Parses a JSON representation of a board, converts it to a Python object and assigns to member variable.
        :param json_board:
        :return: Void
        """
        pass

    def neighbouring_cell_exists(self, worker, direction):
        """

        :param worker:
        :param direction:
        :return: Boolean stating whether cell is occupied or not
        """
        pass

    def get_height(self, worker, direction):
        """

        :param worker:
        :param direction:
        :return: positive integer, [0, 4]
        """
        pass

    def is_occupied(self, worker, direction):
        """

        :param worker:
        :param direction:
        :return: Boolean that tells us whether a cell is occupied or not
        """
        pass

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

        :param worker:
        :return: returns tuple of (row, col, height) where row, col are elem of [0,5] and height is elem [0,4].
        """
        pass

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

