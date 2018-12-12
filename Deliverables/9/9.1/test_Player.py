import pytest
from Board import Board
from Player import Player
from SmartPlayer import SmartPlayer
from RuleChecker import RuleChecker
from CustomExceptions import ContractViolation


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
def test_board_0_prev():
    board = [[[1, "blue2"], 2, 1, 2, 3],
             [2, 2, 1, 0, 4],
             [1, 0, 1, 1, 4],
             [0, 0, [0, "white2"], 0, [2, "white1"]],
             [1, [0, "blue1"], 0, 2, 3]]
    return board


@pytest.fixture()
def test_board_0():
    board = [[1, [2, "blue2"], 1, 2, 3],
             [3, 2, 1, 0, 4],
             [1, 0, [1, "white2"], 2, 4],
             [0, 0, 0, 0, [2, "white1"]],
             [1, [0, "blue1"], 0, 2, 3]]
    return board


@pytest.fixture()
def test_board_1_prev():
    board = [[[3, "blue1"], 0, 0, [2, "white1"], 2],
             [4, 0, 0, 4, 0],
             [4, 4, 4, 4, 0],
             [4, 4, 4, 4, 4],
             [[0, "blue2"], 4, 4, 4, [0, "white2"]]]
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
def test_board_2():
    board = [[1, [0, "blue1"], 0, 0, [0, "blue2"]],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [[0, "white2"], 0, 0, 0, [0, "white1"]]]
    return board


@pytest.fixture()
def test_board_3():
    board = [[1, 1, 0, 0, [0, "blue2"]],
             [0, [0, "blue1"], 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [[0, "white2"], 0, 0, 0, [0, "white1"]]]
    return board


@pytest.fixture()
def test_board_4():
    board = [[1, [0, "blue1"], 0, 0, [0, "blue2"]],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 1, [0, "white1"]],
             [[0, "white2"], 0, 0, 0, 0]]
    return board


@pytest.fixture()
def test_board_5():
    board = [[1, 1, 0, 0, [0, "blue2"]],
             [0, [0, "blue1"], 0, 0, 0],
             [0, 0, 0, 0, 0],
             [[0, "white2"], 0, 0, 0, 0],
             [1, 0, 0, 0, [0, "white1"]]]
    return board


@pytest.fixture()
def valid_plays(play):
    plays = [[["blue2", ["SW"]]],
             [["blue1", ["E", "E"]], ["blue1", ["SE", "NE"]]]]
    return plays[play]


@pytest.mark.parametrize("name", ["P1", "P2"])
def test_register(name):
    player = Player(name)
    assert name == player.register()
    with pytest.raises(ContractViolation): # testing if player can register twice
        player.register()


@pytest.mark.parametrize("board, color, expected", [
    (initial_board(), RuleChecker.COLORS[0], RuleChecker.COLORS[0]),
    (initial_board(2), RuleChecker.COLORS[1], RuleChecker.COLORS[1])
])
def test_place(board, color, expected):
    player = Player("P1")
    player.register()
    random_placements = player.place(board, color)
    assert RuleChecker.is_valid_placement(random_placements)
    assert expected == player.color
    with pytest.raises(ContractViolation):  # checking if place can be called again (shouldn't)
        player.place(board, color)


# # no longer needed since it is randomized now.
# @pytest.mark.parametrize("prev_board, curr_board, expected", [
#     (test_board_0_prev(), test_board_0(), valid_plays(0)),
#     (test_board_1_prev(), test_board_1(), valid_plays(1))
# ])
# def test_play(prev_board, curr_board, expected):
#     player = Player("P1")
#     player.register()
#     player.place(initial_board(), RuleChecker.COLORS[0])
#     player.board.set_board(prev_board)
#     assert expected == player.play(curr_board)


def test_notify():
    player = Player("P1")
    with pytest.raises(ContractViolation):
        player.notify("P2")
    player.register()
    assert "OK" == player.notify("P2")
    assert player.color is None
    assert Board().board == player.board.board
    player.place(initial_board(), RuleChecker.COLORS[0])  # player should be able to place again now


@pytest.mark.parametrize("prev_board, curr_board, color, expected", [
    (initial_board(), initial_board(4), RuleChecker.COLORS[0], True),
    (initial_board(), test_board_0(), RuleChecker.COLORS[0], False),
    (initial_board(), test_board_1(), RuleChecker.COLORS[1], False),
    (initial_board(2), test_board_2(), RuleChecker.COLORS[1], True),
    (initial_board(2), test_board_3(), RuleChecker.COLORS[1], False),
    (initial_board(4), test_board_4(), RuleChecker.COLORS[0], True),
    (test_board_3(), test_board_5(), RuleChecker.COLORS[0], False)
])
def test_check_board(prev_board, curr_board, color, expected):
    player = SmartPlayer("P1")
    player.register()
    player.place(initial_board(), color)
    player.board.set_board(prev_board)
    assert expected == player._check_board(curr_board)
