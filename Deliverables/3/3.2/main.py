import json
from JsonParser import take_input, parse_json
from Board import Board


def main():
    board = Board()
    json_values = parse_json(take_input())
    for json_val in json_values:
        try:
            given_board, statement = json_val["value"]
            board.set_board(given_board)
            command, worker, direction = statement
            if command == "move":
                print(json.dumps(
                    board.move(worker, direction)))
            elif command == "build":
                print(json.dumps(
                    board.build(worker, direction)))
            elif command == "get-height":
                print(json.dumps(
                    board.get_height(worker, direction)))
            elif command == "occupied?":
                print(json.dumps(
                    board.is_occupied(worker, direction)))
            elif command == "neighboring-cell-exists?":
                print(json.dumps(
                    board.neighboring_cell_exists(worker, direction)))
            else:
                raise ValueError("Command not supported: {}".format(statement[0]))
        except Exception as e:
            print(json.dumps(str(e)))


if __name__ == "__main__":
    main()
