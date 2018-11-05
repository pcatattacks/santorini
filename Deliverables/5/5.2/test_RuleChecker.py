import pytest
from RuleChecker import RuleChecker
from CustomExceptions import ContractViolation
from Board import Board


@pytest.fixture()
def legal_board():
    test_board = [[0, [2, "blue2"], 1, 2, 3],
                  [3, 2, 1, 0, 4],
                  [1, 0, [1, "white2"], 2, 4],
                  [0, 0, 0, 0, [2, "white1"]],
                  [1, [0, "blue1"], 0, 2, 3]]
    board = Board()
    board.set_board(test_board)
    return board


@pytest.fixture()
def illegal_extra_workers_board():
    test_board = [[0, [2, "blue2"], 1, 2, 3],
                  [3, 2, 1, 0, 4],
                  [1, 0, [1, "white2"], 2, 4],
                  [0, [0, "blue3"], 0, 0, [2, "white1"]],
                  [1, [0, "blue1"], 0, 2, 3]]
    board = Board()
    board.set_board(test_board)
    return board


@pytest.fixture()
def illegal_less_workers_board():
    test_board = [[0, [2, "blue2"], 1, 2, 3],
                  [3, 2, 1, 0, 4],
                  [1, 0, 1, 2, 4],
                  [0, 0, 0, 0, [2, "white1"]],
                  [1, [0, "blue1"], 0, 2, 3]]
    board = Board()
    board.set_board(test_board)
    return board


@pytest.fixture()
def illegal_num_workers_board():
    test_board = [[0, [2, "blue2"], 1, 2, 3],
                  [3, 2, 1, 0, 4],
                  [1, 0, [1, "blue3"], 2, 4],
                  [0, 0, 0, 0, [2, "white1"]],
                  [1, [0, "blue1"], 0, 2, 3]]
    board = Board()
    board.set_board(test_board)
    return board


@pytest.fixture()
def illegal_heights_board():
    test_board = [[0, [2, "blue2"], 1, 2, 3],
                  [3, 2, 1, 0, 4],
                  [1, 0, [1, "white2"], 2, 5],
                  [0, 0, 0, 0, [2, "white1"]],
                  [1, [0, "blue1"], 0, 2, 3]]
    board = Board()
    board.set_board(test_board)
    return board


@pytest.fixture()
def legal_initial_board():
    test_board = [[0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0]]
    board = Board()
    board.set_board(test_board)
    return board


def legal_initial_board_with_workers(color):
    test_board = [[0, 0, [0, color+"1"], 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, [0, color+"2"], 0, 0],
                  [0, 0, 0, 0, 0]]
    board = Board()
    board.set_board(test_board)
    return board


@pytest.mark.parametrize("worker, direction, expected", [
    ("blue1", "S", False),
    ("blue2", "SW", True),
    ("white1", "N", False),
    ("white2", "E", True)
])
def test_is_valid_move(legal_board, worker, direction, expected):
    assert expected == RuleChecker.is_valid_move(legal_board, worker, direction)


@pytest.mark.parametrize("worker, direction, expected", [
    ("blue1", "S", False),
    ("blue2", "SW", True),
    ("white1", "N", False),
    ("white2", "E", True)
])
def test_is_valid_build(legal_board, worker, direction, expected):
    assert expected == RuleChecker.is_valid_build(legal_board, worker, direction)


@pytest.mark.parametrize("board, color, expected", [
    (legal_initial_board(), "blue", True),
    (legal_initial_board_with_workers("blue"), "blue", False),
    (legal_initial_board_with_workers("white"), "blue", True),
    (legal_initial_board_with_workers("white"), "white", False),
    (legal_initial_board_with_workers("blue"), "white", True),
    (illegal_heights_board(), "blue", False),
    (illegal_heights_board(), "white", False),
    (illegal_extra_workers_board(), "blue", False),
    (illegal_extra_workers_board(), "white", False),
    (illegal_less_workers_board(), "blue", False),
    (illegal_less_workers_board(), "white", False),
    (illegal_num_workers_board(), "blue", False),
    (illegal_num_workers_board(), "white", False)
])
def test_is_legal_initial_board(board, color, expected):
    assert expected == RuleChecker.is_legal_initial_board(board, color)


@pytest.mark.parametrize("board, expected", [
    (legal_board(), True),
    (illegal_heights_board(), False),
    (illegal_heights_board(), False),
    (illegal_extra_workers_board(), False),
    (illegal_extra_workers_board(), False),
    (illegal_less_workers_board(), False),
    (illegal_less_workers_board(), False),
    (illegal_num_workers_board(), False),
    (illegal_num_workers_board(), False)
])
def test_is_legal_board(board, expected):
    assert expected == RuleChecker.is_legal_board(board)


@pytest.mark.parametrize("worker, expected", [
    ("blue1", True),
    ("blue2", True),
    ("white1", True),
    ("blue3", False),
    ("white3", False),
    ("white2", True)
])
def test_is_valid_worker(worker, expected):
    assert expected == RuleChecker.is_valid_worker(worker)


@pytest.mark.parametrize("direction, expected", [
    ("N", True), ("W", True), ("NW", True), ("NE", True), ("E", True), ("SE", True), ("SW", True), ("S", True),
    ("EN", False), ('WS', False)
])
def test_is_valid_direction(direction, expected):
    assert expected == RuleChecker.is_valid_direction(direction)


@pytest.mark.parametrize("color, expected", [
    ("grey", False),
    ("blue", True),
    ("white", True)
])
def test_is_valid_color(color, expected):
    assert expected == RuleChecker.is_valid_color(color)


@pytest.mark.parametrize("worker, direction, expected", [
    ("blue2", "SW", True),
    ("blue2", "S", False),
    ("white1", "S", True),
    ("white2", "N", False)
])
def test_is_winning_move(legal_board, worker, direction, expected):
    assert expected == RuleChecker.is_winning_move(legal_board, worker, direction)


@pytest.mark.parametrize("worker, direction, expected", [])
def test_is_winning_build(legal_board, worker, direction, expected):
    pass


@pytest.mark.parametrize("worker, direction, expected", [])
def test_is_winning_play(legal_board, worker, direction, expected):
    pass