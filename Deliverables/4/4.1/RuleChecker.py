# Note: These are the base rules. To add rules with God Powers, Create new class which inherits from RuleChecker and
# override methods to adjust for God Power rule additions.


class RuleChecker:

    WORKERS = ("blue1", "blue2", "white1", "white2")
    DIRECTIONS = ("N", "NE", "E", "SE", "S", "SW", "W", "NW")

    @staticmethod
    def is_valid_move(board, worker, direction):
        if not RuleChecker._is_valid_worker(worker) or not RuleChecker._is_valid_direction(direction):
            raise ValueError("Invalid value(s) provided to function.")
        worker_height = board.get_worker_position(worker)[2]
        adj_cell_height = board.get_height(worker, direction)
        return (board.neighboring_cell_exists(worker, direction)
                and not board.is_occupied(worker, direction)
                and adj_cell_height != 4
                and adj_cell_height - worker_height <= 1)

    @staticmethod
    def is_valid_build(board, worker, direction):
        if not RuleChecker._is_valid_worker(worker) or not RuleChecker._is_valid_direction(direction):
            raise ValueError("Invalid value(s) provided to function.")
        adj_cell_height = board.get_height(worker, direction)
        return (board.neighboring_cell_exists(worker, direction)
                and not board.is_occupied(worker, direction)
                and adj_cell_height != 4)

    @staticmethod
    def _is_valid_worker(worker):
        return worker in RuleChecker.WORKERS

    @staticmethod
    def _is_valid_direction(direction):
        return direction in RuleChecker.DIRECTIONS
