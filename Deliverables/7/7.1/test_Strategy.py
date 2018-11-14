import pytest
from Board import Board
from RuleChecker import RuleChecker
from Strategy import Strategy
from CustomExceptions import ContractViolation

# TODO: modify tests to reflect that the strategy component no longer does a check for a valid (initial) board


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
    test_board = [[[0, color+"1"], 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, [0, color+"2"]]]
    board = Board()
    board.set_board(test_board)
    return board


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


@pytest.mark.parametrize("board, color, expected", [
    (legal_initial_board(), "blue", [[0, 0], [0, 4]]),
    (legal_initial_board(), "white", [[0, 0], [0, 4]]),
    (legal_initial_board_with_workers("white"), "blue", [[0, 4], [4, 0]]),
    (legal_initial_board_with_workers("blue"), "white", [[0, 4], [4, 0]]),
])
def test_get_placements(board, color, expected):
    assert expected == Strategy.get_placements(board, color)


def test_get_play():
    pass


def test_get_plays():
    pass


def test_loses_in_n_moves():
    pass


@pytest.mark.parametrize("color", ["blue", "white"])
def test_get_legal_plays(legal_board, color):
    # Not a complete test, only tests for legality of plays output. Getting all possible move/build combos would be a
    # pain by hand, so this will do for now
    for play in Strategy.get_legal_plays(legal_board, color):
        assert RuleChecker.is_legal_play(legal_board, *play)

