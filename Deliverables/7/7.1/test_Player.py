import pytest
from Board import Board
from Player import Player
from RuleChecker import RuleChecker


@pytest.fixture()
def placement_positions(player=None):
    positions = [[0, 0],
                 [0, 4],
                 [4, 4],
                 [4, 0]]
    if player == 1:
        return [positions[0], positions[1]]
    elif player == 2:
        return [positions[2], positions[3]]
    return positions


@pytest.fixture()
def initial_board(num_placements=0):
    board = Board()
    positions = placement_positions()
    for placement in range(num_placements):
        row, col = positions[placement]
        board.place_worker(row, col, RuleChecker.WORKERS[placement])
    return board.board


@pytest.fixture()
def test_board_0():
    board = [[0, [2, "blue2"], 1, 2, 3],
             [3, 2, 1, 0, 4],
             [1, 0, [1, "white2"], 2, 4],
             [0, 0, 0, 0, [2, "white1"]],
             [1, [0, "blue1"], 0, 2, 3]]
    return board


@pytest.fixture()
def test_board_1():
    board = [[4, [0, "blue1"], 0, 3, [2, "white1"]],
             [4, 0, 0, 4, 0],
             [4, 4, 4, 4, 0],
             [4, 4, 4, 4, 4],
             [[0, "blue2"], 4, 4, 4, [0, "white2"]]]
    return board


@pytest.fixture()
def valid_plays(play):
    plays = [[["blue2", ["SW"]]],
             [["blue1", ["E", "E"]], ["blue1", ["SE", "NE"]]]]
    return plays[play]


@pytest.mark.parametrize("name", [
    ("P1"),
    ("P2")
])
def test_register(name):
    player = Player(name, 5)
    assert name == player.register()


@pytest.mark.parametrize("color, expected", [
    (RuleChecker.COLORS[0], RuleChecker.COLORS[0]),
    (RuleChecker.COLORS[1], RuleChecker.COLORS[1])
])
def test_register_color(color, expected):
    player = Player("P1", 5)
    player.register_color(color)
    assert expected == player.color


@pytest.mark.parametrize("board, color, expected", [
    (initial_board(), RuleChecker.COLORS[0], placement_positions(1)),
    (initial_board(2), RuleChecker.COLORS[1], placement_positions(2))
])
def test_place(board, color, expected):
    player = Player("P1", 5)
    player.register_color(color)
    assert expected == player.place(board)


@pytest.mark.parametrize("board, expected", [
    (test_board_0(), valid_plays(0)),
    (test_board_1(), valid_plays(1))
])
def test_play(board, expected):
    player = Player("P1", 5)
    player.register_color(RuleChecker.COLORS[0])
    assert expected == player.play(board)


@pytest.mark.parametrize("", [])
def test_notify():
    pass
