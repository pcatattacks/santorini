class RuleChecker:

    @staticmethod
    def is_valid_move(board, worker, direction):
        if not RuleChecker._is_valid_worker(worker) or not RuleChecker._is_valid_direction(direction):
            raise ValueError("Invalid value(s) provided to function.")
        # TODO: see if you can avoid calling _get_worker_position twice - once in rule checker and once elsewhere
        worker_height = board._get_worker_position(worker)[2]  # TODO: rename _get_worker_position so it's public
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
        return worker in ("blue1", "blue2", "white1", "white2")

    @staticmethod
    def _is_valid_direction(direction):
        return direction in ("N", "NE", "E", "SE", "S", "SW", "W", "NW")
