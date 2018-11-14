import pytest
from Board import Board


@pytest.fixture()
def empty_board():
    board = [[0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0]]
    board_obj = Board()
    board_obj.set_board(board)
    return board_obj


@pytest.fixture()
def mini_board():
    board = [[0, 1, 1, 0],
             [[1, "white1"], 2, 1, [2, "blue2"]],
             [[1, "white2"], 1, 0, 1],
             [0, 1, 2, [1, "blue1"]]]
    board_obj = Board()
    board_obj.set_board(board)
    return board_obj


@pytest.fixture()
def legal_board():
    board = [[0, [2, "blue2"], 1, 2, 3],
             [3, 2, 1, 0, 4],
             [1, 0, [1, "white2"], 2, 4],
             [0, 0, 0, 0, [2, "white1"]],
             [[0, "blue1"], 1, 0, 2, 3]]
    board_obj = Board()
    board_obj.set_board(board)
    return board_obj


@pytest.fixture()
def congested_board():
    board = [[0, 2, 1, 2, 3],
             [3, 2, 1, 0, 4],
             [1, [2, "blue2"], [1, "white2"], 2, 4],
             [0, 0, 0, [2, "white1"], 0],
             [1, 0, [0, "blue1"], 2, 3]]
    board_obj = Board()
    board_obj.set_board(board)
    return board_obj


@pytest.mark.parametrize("test_board, expected", [
    (empty_board(), (5, 5)),
    (mini_board(), (4, 4)),
    (legal_board(), (5, 5)),
    (congested_board(), (5, 5))
])
def test_get_dimensions(test_board, expected):
    assert expected == test_board.get_dimensions()


@pytest.mark.parametrize("test_board", [
    (empty_board()),
    (mini_board()),
    (legal_board()),
    (congested_board())
])
# TODO: use get_worker_position to test accuracy of worker_positions dict update
def test_set_board(test_board):
    pass


@pytest.mark.parametrize("worker, direction, expected", [
    ("blue1", "SW", False),
    ("white2", "W", True),
    ("white1", "E", False),
    ("blue2", "SE", True)
])
def test_neighboring_cell_exists(legal_board, worker, direction, expected):
    assert expected == legal_board.neighboring_cell_exists(worker, direction)


@pytest.mark.parametrize("worker, direction, expected", [
    ("blue1", "N", 0),
    ("white2", "E", 2),
    ("white1", "N", 4),
    ("blue2", "SW", 3)
])
def test_get_height(legal_board, worker, direction, expected):
    assert expected == legal_board.get_height(worker, direction)


@pytest.mark.parametrize("worker, direction, expected", [
    ("blue1", "N", False),
    ("blue1", "NE", True),
    ("white2", "W", True),
    ("white2", "SW", False)
])
def test_is_occupied(congested_board, worker, direction, expected):
    assert expected == congested_board.is_occupied(worker, direction)


@pytest.mark.parametrize("worker, direction, expected", [
    ("blue1", "E", 2),
    ("blue2", "SW", 4),
    ("white1", "W", 1),
    ("white2", "NE", 1)
])
def test_build(legal_board, worker, direction, expected):
    legal_board.build(worker, direction)
    assert expected == legal_board.get_height(worker, direction)


@pytest.mark.parametrize("worker, direction, expected", [
    ("blue1", "E", 0),
    ("blue2", "S", 1),
    ("white1", "N", 3),
    ("white2", "NW", 1)
])
def test_undo_build(legal_board, worker, direction, expected):
    legal_board.undo_build(worker, direction)
    assert expected == legal_board.get_height(worker, direction)


@pytest.mark.parametrize("worker, direction, expected", [
    ("blue1", "NE", (3, 1, 0)),
    ("blue2", "S", (1, 1, 2)),
    ("white1", "NW", (2, 3, 2)),
    ("white2", "N", (1, 2, 1))
])
def test_move(legal_board, worker, direction, expected):
    legal_board.move(worker, direction)
    assert expected == legal_board.get_worker_position(worker)


@pytest.mark.parametrize("worker, expected", [
    ("blue1", (4, 0, 0)),
    ("blue2", (0, 1, 2)),
    ("white1", (3, 4, 2)),
    ("white2", (2, 2, 1))
])
def test_get_worker_position(legal_board, worker, expected):
    assert expected == legal_board.get_worker_position(worker)


@pytest.mark.parametrize("row, col, expected", [
    (0, 1, True),
    (1, 1, False),
    (2, 2, True),
    (4, 3, False)
])
def test_has_worker(legal_board, row, col, expected):
    assert expected == legal_board.has_worker(row, col)


@pytest.mark.parametrize("row, col, worker, expected", [
    (1, 1, "blue1", (1, 1, 0)),
    (3, 2, "blue2", (3, 2, 0)),
    (0, 4, "white1", (0, 4, 0)),
    (4, 4, "white2", (4, 4, 0))
])
def test_place_worker(empty_board, row, col, worker, expected):
    empty_board.place_worker(row, col, worker)
    assert expected == empty_board.get_worker_position(worker)


@pytest.mark.parametrize("row, col, direction, expected", [
    (3, 2, "N", (2, 2)),
    (0, 4, "SW", (1, 3)),
    (3, 3, "E", (3, 4)),
    (4, 4, "NW", (3, 3))
])
def test_get_adj_cell(row, col, direction, expected):
    assert expected == Board._get_adj_cell(row, col, direction)


@pytest.mark.parametrize("direction, expected", [
    ("N", "S"),
    ("NW", "SE"),
    ("E", "W"),
    ("SW", "NE")
])
def test_get_opposite_direction(direction, expected):
    assert expected == Board.get_opposite_direction(direction)


@pytest.mark.parametrize("", [])  # TODO
def test_get_cell_height():
    pass


@pytest.mark.parametrize("", [])  # TODO
def test_get_cell_worker():
    pass
