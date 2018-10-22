import json
from JsonParser import take_input, parse_json
from Board import Board
from RuleChecker import RuleChecker


def main():
    board = Board()
    json_values = parse_json(take_input())
    for json_val in json_values:
        try:
            given_board, worker, directions = json_val["value"]
            build_dir = None
            if len(directions) == 1:
                move_dir = directions[0]
            elif len(directions) == 2:
                move_dir, build_dir = directions
            else:
                raise ValueError("Too many/few directions provided.")

            board.set_board(given_board)
            if RuleChecker.is_valid_move(board, worker, move_dir):
                if RuleChecker.is_winning_move(board, worker, move_dir) and build_dir is None:  # checking for win
                    print(json.dumps("yes"))
                    continue
                board.move(worker, move_dir)
                if RuleChecker.is_valid_build(worker, build_dir):
                    print(json.dumps("yes"))
                else:
                    print(json.dumps("no"))
            else:
                print(json.dumps("no"))
        except Exception as e:
            print(json.dumps(str(e)))


if __name__ == "__main__":
    main()
