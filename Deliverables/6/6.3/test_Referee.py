import pytest
from Board import Board
from Player import Player
from Referee import Referee
from RuleChecker import RuleChecker


# TODO: avoid manual turn swap in testing functions


@pytest.fixture()
def placement_positions(player=None):
    positions = [[0, 0],
                 [4, 0],
                 [0, 4],
                 [4, 4]]
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
def player_plays(turns=0):
    plays = [[RuleChecker.WORKERS[1], ["E", "W"]],
             [RuleChecker.WORKERS[2], ["S", "SW"]],
             [RuleChecker.WORKERS[1], ["W", "N"]],
             [RuleChecker.WORKERS[3], ["W", "NW"]]]
    for turn in range(4 - turns):
        plays = plays[:-1]
    return plays


@pytest.fixture()
def play_board(num_turns=0):
    board = Board()
    board.set_board(initial_board(4))
    plays = player_plays(num_turns)
    for play in plays:
        worker, directions = play
        board.move(worker, directions[0])
        board.build(worker, directions[1])
    return board.board


@pytest.mark.parametrize("names, expected", [
    (["P1"], RuleChecker.COLORS[:-1]),
    (["P1", "P2"], RuleChecker.COLORS)
])
def test_register_player(names, expected):
    player1 = Player()
    player2 = Player()
    referee = Referee(player1, player2)
    for count, name in enumerate(names):
        assert expected[count] == referee._register_player(name)


@pytest.mark.parametrize("placements, expected", [
    ([placement_positions(1)], [initial_board(2)]),
    ([placement_positions(1), placement_positions(2)], [initial_board(2), initial_board(4)])
])
def test_update_board_with_placements(placements, expected):
    player1 = Player()
    player2 = Player()
    referee = Referee(player1, player2)
    referee._register_player("P1")
    referee._register_player("P2")
    for count, placement in enumerate(placements):
        referee._update_board_with_placements(placement)
        referee.turn = 1 if referee.turn == 0 else 0
        assert expected[count] == referee.board.board


@pytest.mark.parametrize("plays, expected", [
    (player_plays(1), play_board(1)),
    (player_plays(2), play_board(2)),
    (player_plays(3), play_board(3)),
    (player_plays(4), play_board(4))
])
def test_update_board_with_play(plays, expected):
    player1 = Player()
    player2 = Player()
    referee = Referee(player1, player2)
    referee._register_player("P1")
    referee._register_player("P2")
    referee.board.set_board(initial_board(4))
    referee.unplaced_workers = []
    for count, play in enumerate(plays):
        referee._update_board_with_play(play)
        referee.turn = 1 if referee.turn == 0 else 0
    assert expected == referee.board.board
