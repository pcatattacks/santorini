from Board import Board
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
        if not RuleChecker.is_legal_initial_board(board, color):
            raise ContractViolation("Invalid initial board provided to Strategy class: {}".format(board))
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
    def get_plays(board, color):
        """
        Returns a list of all possible legal plays that cannot not result in the opposing player winning with the next
        move.

        :param Board board: an instance of Board (refer to documentation of Board class).
        :param string color: color (as defined above)
        :return: a `list` of legal plays (as defined above)
        :rtype: `list`
        """
        if not RuleChecker.is_valid_color(color):
            raise ContractViolation("Invalid color given: {}".format(color))
        if not RuleChecker.is_legal_board(board):
            raise ContractViolation("Invalid board given: {}".format(board))

        # algorithm - a basic DFS
        #
        # R <- []
        # P <- get legal plays for current player
        # for p in P:
        #   simulate play - so edit the board
        #   Q <- get legal plays for opposing player
        #   for q in Q:
        #       if q not is winning_play: # TODO - will have to write a function in RuleChecker for this
        #           R.append(p)
        #   undo play (if you're using the same board - don't need if we're deepcopy-ing the board for each play)

        available_colors = list(RuleChecker.COLORS)
        available_colors.remove(color)
        opposition_player_color = available_colors[0]

        result_plays = []

        player_legal_plays = Strategy._get_legal_plays(board, color)

        for play in player_legal_plays:
            if len(play[1]) == 1:  # TODO: replace with RuleChecker.is_winning_play
                result_plays.append(play)
            else:
                opposition_win = False
                worker = play[0]
                move_dir, build_dir = play[1]

                board.move(worker, move_dir)
                board.build(worker, build_dir)

                opposition_player_legal_plays = Strategy._get_legal_plays(board, opposition_player_color)

                for opp_play in opposition_player_legal_plays:
                    if len(opp_play[1]) == 1:  # TODO: replace with RuleChecker.is_winning_play
                        opposition_win = True
                        break

                if not opposition_win:
                    result_plays.append(play)

                # undoing the build and move in that order
                board.undo_build(worker, build_dir)
                board.move(worker, Board.get_opposite_direction(move_dir))

        return result_plays

    @staticmethod
    def _get_legal_plays(board, color):
        """
        Returns a list of all possible legal plays for players of the given color.

        :param Board board: an instance of Board (refer to documentation of Board class).
        :param string color: color (as defined above)
        :return: a `list` of legal plays (as defined above)
        :rtype: list
        """
        if not RuleChecker.is_valid_color(color):
            raise ContractViolation("Invalid color given: {}".format(color))
        if not RuleChecker.is_legal_board(board):
            raise ContractViolation("Invalid board given: {}".format(board))

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
                    opp_dir = Board.get_opposite_direction(move_dir)
                    board.move(player, opp_dir)  # undoing the move

        return legal_plays


