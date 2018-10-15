from JsonParser import take_input, parse_json
from Board import Board


def main():
    board = Board()
    json_values = parse_json(take_input())
    for json_val in json_values:
        given_board, statement = json_val["value"]
        board.set_board(given_board)
        command, worker, direction = statement
        if command == "move":
            board.move(worker, direction)
        elif command == "build":
            board.build(worker, direction)
        elif command == "get-height":
            board.get_height(worker, direction)
        elif command == "occupied?":
            board.is_occupied(worker, direction)
        elif command == "neighboring-cell-exists?":
            board.neighboring_cell_exists(worker, direction)
        else:
            raise ValueError("Command not supported: {}".format(statement[0]))


if __name__ == "__main__":
    main()