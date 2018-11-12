import pytest
from Player import Player
from Referee import Referee


@pytest.mark.parametrize("names, expected", [
    (["P1"], ["blue"]),
    (["P1", "P2"], ["blue", "white"])
])
def test_register_player(names, expected):
    player1 = Player()
    player2 = Player()
    referee = Referee(player1, player2)
    for count, name in enumerate(names):
        assert expected[count] == referee._register_player(name)


@pytest.mark.parametrize("placements, expected", [
    ([[[0, 0], [4, 0]]], [[[[0, "blue1"], 0, 0, 0, 0],
                           [0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0],
                           [[0, "blue2"], 0, 0, 0, 0]]]),
    ([[[0, 0], [4, 0]], [[4, 4], [0, 4]]], [[[[0, "blue1"], 0, 0, 0, 0],
                                             [0, 0, 0, 0, 0],
                                             [0, 0, 0, 0, 0],
                                             [0, 0, 0, 0, 0],
                                             [[0, "blue2"], 0, 0, 0, 0]],
                                            [[[0, "blue1"], 0, 0, 0, [0, "white2"]],
                                             [0, 0, 0, 0, 0],
                                             [0, 0, 0, 0, 0],
                                             [0, 0, 0, 0, 0],
                                             [[0, "blue2"], 0, 0, 0, [0, "white1"]]]])
])
def test_update_board_with_placements(placements, expected):  # TODO - turn into fixtures
    player1 = Player()
    player2 = Player()
    referee = Referee(player1, player2)
    referee._register_player("P1")
    referee._register_player("P2")
    for count, placement in enumerate(placements):
        referee._update_board_with_placements(placement)
        referee.turn = 1 if referee.turn == 0 else 0  # TODO - get rid of hacky fix
        assert expected[count] == referee.board.board


@pytest.mark.parametrize("plays, expected", [
    ([["blue1", ["E", "W"]]], [[[1, [0, "blue1"], 0, 0, [0, "white2"]],
                                [0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0],
                                [[0, "blue2"], 0, 0, 0, [0, "white1"]]]])
])
def test_update_board_with_play(plays, expected):
    player1 = Player()
    player2 = Player()
    referee = Referee(player1, player2)
    referee._register_player("P1")
    referee._register_player("P2")
    referee._update_board_with_placements([[0, 0], [4, 0]])
    referee.turn = 1 if referee.turn == 0 else 0
    referee._update_board_with_placements([[4, 4], [0, 4]])
    referee.turn = 1 if referee.turn == 0 else 0
    for count, play in enumerate(plays):
        referee._update_board_with_play(play)
        referee.turn = 1 if referee.turn == 0 else 0  # TODO - get rid of hacky fix
        assert expected[count] == referee.board.board
