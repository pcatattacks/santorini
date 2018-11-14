from RuleChecker import RuleChecker
from CustomExceptions import ContractViolation


class Strategy:
    """
    A class that is used by the player to construct plays that a `Player` uses.

    Dependencies:
     - Board class. Refer to Board documentation.
     - RuleChecker class. Refer to RuleChecker documentation.

    Definitions:

    play
        `list`: [worker, [direction1, direction2]] or [worker, [direction1]] where direction1 is the direction to move
        and direction2 is the direction to build.

    """
    # TODO: Discuss
    # Should each player have it's own instance of the strategy class? By having both players use static methods of
    # the strategy class (and passing in color as a parameter), we'll have to write a lot of if-statements and
    # additional logic in the strategy class so it can make conditional plays based on for which color it outputs a
    # strategy. But we'll have to do this anyway.
    # This also means that an opposing player can get another player's strategy, by just passing in the other color.
    # This enables cheating.
    # If we make Strategy a member variable of Player, and instantiate it with the color passed into player, we can add
    # functionality for god powers etc later. We're probably going to extend the Strategy class if we create God powers,
    # for each God power. if so, we'll have to always find which GodPowerStrategy class to find and use, rather than
    # just finding it once and storing it. Not sure.

    # TODO: Discuss
    # by making Strategy a public class with static member functions, we aren't enabling any cheating are we? or should
    # strategy be a private class within player? that doesn't make sense to me. having some of Strategy's function's
    # exposed doesn't allow any manipulation to variables that represent the game state, so it should be fine (I think).

    @staticmethod
    def get_placements(board, color):
        """
        Returns worker placements of given color, by scheme of choosing the first two unoccupied corner cells, starting
        from top left, in the clockwise direction.

        :param Board board: an instance of Board (refer to documentation of Board class).
        :param string color: color (as defined above)
        :return: `list` of [position1, position2] where position1 and position2 are positions of the first and second
        worker respectively. See `worker` and `position` in Board.py documentation.
        :rtype: list
        """
        num_rows, num_cols = board.get_dimensions()
        corners = ([0, 0], [0, num_cols-1], [num_rows-1, num_cols-1], [num_rows-1, 0])
        placements = []
        for corner in corners:
            if not board.has_worker(*corner):
                placements.append(corner)
            if len(placements) == 2:
                break
        assert len(placements) == 2  # shouldn't needed since we're checking that the board is valid at the start, but
        # may as well
        return placements

    @staticmethod
    def get_play(board, color):
        """
        Returns the optimal play for a given board and a color that identifies the player.

        :param Board board: an instance of Board (refer to documentation of Board class).
        :param string color: color (as defined above)
        :return: a play (as defined above)
        :rtype: list
        """
        pass

    @staticmethod
    def get_plays(board, color, num_look_ahead):
        """
        Returns a list of all possible legal plays that cannot not result in the opposing player winning within the next
        `num_look_ahead` moves.

        CONTRACT:
         - `num_look_ahead` must be >= 1

        :param Board board: an instance of Board (refer to documentation of Board class).
        :param string color: color (as defined above)
        :param int num_look_ahead: number of moves to look ahead by
        :return: a `list` of legal plays (as defined above)
        :rtype: `list`
        """
        if not RuleChecker.is_valid_color(color):
            raise ContractViolation("Invalid color given: {}".format(color))
        if num_look_ahead < 1:
            return ContractViolation("Must look at least 1 move ahead! Given {}".format(num_look_ahead))

        available_colors = list(RuleChecker.COLORS)
        available_colors.remove(color)
        opp_color = available_colors[0]

        result_plays = []

        for play in Strategy.get_legal_plays(board, color):
            # if RuleChecker.is_winning_play(board, *play):
            #     result_plays.append(play)
            if len(play[1]) == 1:
                result_plays.append(play)
            else:
                opposition_win = False
                worker = play[0]
                move_dir, build_dir = play[1]

                # player play
                board.move(worker, move_dir)
                board.build(worker, build_dir)

                opp_legal_plays = Strategy.get_legal_plays(board, opp_color)
                if any(len(opp_play[1]) == 1 for opp_play in opp_legal_plays):  # try and prune search
                    opposition_win = True
                else:
                    for opp_play in opp_legal_plays:
                        # if RuleChecker.is_winning_play(board, *opp_play):
                        #     opposition_win = True
                        #     break
                        if len(opp_play[1]) == 1:
                            opposition_win = True
                            break
                        elif num_look_ahead > 1:
                            opp_worker = opp_play[0]
                            opp_move_dir, opp_build_dir = opp_play[1]

                            # opposition play
                            board.move(opp_worker, opp_move_dir)
                            board.build(opp_worker, opp_build_dir)

                            opposition_win = Strategy._loses_in_n_moves(board, color, num_look_ahead - 1)

                            # undoing opposition play
                            board.undo_build(opp_worker, opp_build_dir)
                            board.move(opp_worker, board.get_opposite_direction(opp_move_dir))

                            if opposition_win:
                                break

                # undoing player play
                board.undo_build(worker, build_dir)
                board.move(worker, board.get_opposite_direction(move_dir))

                if not opposition_win:
                    result_plays.append(play)

        return result_plays

    @staticmethod
    def _loses_in_n_moves(board, color, n):
        """

        :param Board board:
        :param string color:
        :param int n:
        :return:
        :rtype: bool
        """
        if n == 0:
            return False

        opp_color = "blue" if color == "white" else "white"

        legal_plays = Strategy.get_legal_plays(board, color)
        if all(len(play[1]) == 1 for play in legal_plays):
            return False

        loses = True  # if the player has no plays, which means player lost, which means loop never executes
        for play in legal_plays:
            if len(play[1]) == 1:
                continue
            worker = play[0]
            move_dir, build_dir = play[1]

            # player play
            board.move(worker, move_dir)
            board.build(worker, build_dir)

            opp_legal_plays = Strategy.get_legal_plays(board, opp_color)
            if any(len(opp_play[1]) == 1 for opp_play in opp_legal_plays):  # try and prune search
                loses = True
            else:
                loses = False  # if opposition has no plays, which means player wins, which means loop never executes
                for opp_play in opp_legal_plays:
                    # if RuleChecker.is_winning_play(board, *opp_play):
                    #     loses = True
                    if len(opp_play[1]) == 1:
                        loses = True
                        break
                    elif n > 1:  # TODO - check. should this be 1 or 0
                        opp_worker = opp_play[0]
                        opp_move_dir, opp_build_dir = opp_play[1]

                        # opposition play
                        board.move(opp_worker, opp_move_dir)
                        board.build(opp_worker, opp_build_dir)

                        loses = Strategy._loses_in_n_moves(board, color, n-1)  # recurse

                        # undoing opposition play
                        board.undo_build(opp_worker, opp_build_dir)
                        board.move(opp_worker, board.get_opposite_direction(opp_move_dir))

                        if loses:
                            break

            # undoing player play
            board.undo_build(worker, build_dir)
            board.move(worker, board.get_opposite_direction(move_dir))

            if loses:
                break

        return loses

    @staticmethod
    def get_legal_plays(board, color):
        """
        Returns a list of all possible legal plays for players of the given color.

        :param Board board: an instance of Board (refer to documentation of Board class).
        :param string color: color (as defined above)
        :return: a `list` of legal plays (as defined above)
        :rtype: list
        """
        if not RuleChecker.is_valid_color(color):
            raise ContractViolation("Invalid color given: {}".format(color))

        legal_plays = []
        players = [str(color+"1"), str(color+"2")]
        player_movable_directions = [[], []]

    #   Valid Move directions
        for direc in RuleChecker.DIRECTIONS:
            for i, player in enumerate(players):
                if RuleChecker.is_valid_move(board, player, direc):
                    player_movable_directions[i].append(direc)

    #   Constructing all possible legal plays.
        for i, player in enumerate(players):
            for move_dir in player_movable_directions[i]:
                if RuleChecker.is_winning_move(board, player, move_dir):
                    legal_plays.append([player, [move_dir]])

                else:
                    board.move(player, move_dir)
                    for build_dir in RuleChecker.DIRECTIONS:
                        if RuleChecker.is_valid_build(board, player, build_dir):
                            legal_plays.append([player, [move_dir, build_dir]])
                    opp_dir = board.get_opposite_direction(move_dir)
                    board.move(player, opp_dir)  # undoing the move

        return legal_plays
