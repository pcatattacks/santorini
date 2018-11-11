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
def test_check_placements(placements, expected):
    player1 = Player()
    player2 = Player()
    referee = Referee(player1, player2)
    referee._register_player("P1")
    referee._register_player("P2")
    for count, placement in enumerate(placements):
        assert expected[count] == referee.check_placements(placement)


@pytest.mark.parametrize("plays, expected", [
    ([["blue1", ["E", "W"]]], [[[1, [0, "blue1"], 0, 0, [0, "white2"]],
                                [0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0],
                                [[0, "blue2"], 0, 0, 0, [0, "white1"]]]])
])
def test_check_play(plays, expected):
    player1 = Player()
    player2 = Player()
    referee = Referee(player1, player2)
    referee._register_player("P1")
    referee._register_player("P2")
    referee.check_placements([[0, 0], [4, 0]])
    referee.check_placements([[4, 4], [0, 4]])
    for count, play in enumerate(plays):
        assert expected[count] == referee.check_play(play)