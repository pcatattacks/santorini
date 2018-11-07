# Note: These are the base rules. To add rules with God Powers, Create new class which inherits from RuleChecker and
# override methods to adjust for God Power rule additions.

from CustomExceptions import ContractViolation


class RuleChecker:

    """
    A class that contains methods to check if the rules of the Santorini game are being followed.

    Definitions:

    play
        `list`: [worker, [direction1, direction2]] or [worker, [direction1]] where direction1 is the direction to move
        and direction2 is the direction to build.
    """

    WORKERS = ("blue1", "blue2", "white1", "white2")
    DIRECTIONS = ("N", "NE", "E", "SE", "S", "SW", "W", "NW")
    COLORS = ("blue", "white")

    @staticmethod
    def is_winning_move(board, worker, direction):
        if not RuleChecker.is_valid_worker(worker) or not RuleChecker.is_valid_direction(direction):
            raise ContractViolation("Invalid (or no) worker / direction provided.")
        return board.get_height(worker, direction) == 3

    @staticmethod
    def is_winning_build(board, worker, direction):
        if not RuleChecker.is_valid_worker(worker) or not RuleChecker.is_valid_direction(direction):
            raise ContractViolation("Invalid (or no) worker / direction provided.")
        # TODO
        pass

    @staticmethod
    def is_winning_play(board, worker, directions):
        """
        Takes in a play (as specified above) and checks if it's a winning play.

        This entails checking if the `worker` is moving up to height 3, or if the play blocks the opposition player from
        making any moves or builds.

        CONTRACT:
         - `[worker, directions]` must be a legal play.

        :param Board board:
        :param string worker:
        :param list directions:
        :return:
        :rtype: bool
        """
        if not RuleChecker.is_valid_worker(worker):
            raise ContractViolation("Invalid (or no) worker provided.")
        if not all(map(RuleChecker.is_valid_direction, directions)):
            raise ContractViolation("Invalid (or no) directions provided.")
        if not RuleChecker.is_legal_play(board, worker, directions):
            raise ContractViolation("Illegal play passed into is_winning_play: {}".format([worker, directions]))

        color = worker[-1]
        opp_color = list(RuleChecker.COLORS).remove(color)[0]

        if len(directions) == 1:  # must be winning, since one direction is only legal in the winning case
            return True
        else:
            opp_cannot_play = False
            move_dir, build_dir = directions

            # simulate play
            board.move(worker, move_dir)
            board.build(worker, build_dir)

            opposition_player_legal_plays = Strategy.Strategy.get_legal_plays(board, opp_color)

            if not opposition_player_legal_plays:
                opp_cannot_play = True

            # undo play
            board.undo_build(worker, build_dir)
            board.move(worker, board.get_opposite_direction(move_dir))

            return opp_cannot_play

    @staticmethod
    def is_valid_move(board, worker, direction):
        if not RuleChecker.is_valid_worker(worker) or not RuleChecker.is_valid_direction(direction):
            raise ContractViolation("Invalid (or no) worker / direction provided.")
        worker_height = board.get_worker_position(worker)[2]
        adj_cell_height = board.get_height(worker, direction)
        return (board.neighboring_cell_exists(worker, direction)
                and not board.is_occupied(worker, direction)
                and adj_cell_height != 4
                and adj_cell_height - worker_height <= 1)

    @staticmethod
    def is_valid_build(board, worker, direction):
        if not RuleChecker.is_valid_worker(worker) or not RuleChecker.is_valid_direction(direction):
            raise ContractViolation("Invalid (or no) worker / direction provided.")
        adj_cell_height = board.get_height(worker, direction)
        return (board.neighboring_cell_exists(worker, direction)
                and not board.is_occupied(worker, direction)
                and adj_cell_height != 4)

    @staticmethod
    def is_legal_play(board, worker, directions):
        """
        :param Board board:
        :param string worker:
        :param list directions:
        :return: `True` if play is legal, `False` otherwise
        :rtype: bool
        """
        build_dir = None
        if len(directions) == 1:
            move_dir = directions[0]
        elif len(directions) == 2:
            move_dir, build_dir = directions
        else:
            raise ContractViolation("Too many/few directions provided.")

        if RuleChecker.is_valid_move(board, worker, move_dir):
            if RuleChecker.is_winning_move(board, worker, move_dir):
                if build_dir is None:  # checking for win
                    return True
                else:
                    return False
            elif build_dir is None:
                return False
            board.move(worker, move_dir)
            if RuleChecker.is_valid_build(board, worker, build_dir):
                return_val = True
            else:
                return_val = False
            board.move(worker, board.get_opposite_direction(move_dir))  # undo the move
            return return_val
        else:
            return False

    @staticmethod
    def is_legal_initial_board(board, color):  # TODO - Pranav needs to read over implementation
        """
        Checks the validity of an initial board.

        :param list board: A board (as defined in the documentation of Board).
        :param string color: A color (as defined in the documentation of Referee).
        :return: 'True' if the board is a valid initial board, else 'False'.
        :rtype: bool
        """
        if not RuleChecker.is_valid_color(color):
            raise ContractViolation("Invalid color provided: {}".format(color))
        unset_workers = [color + "1", color + "2"]
        return RuleChecker.is_legal_board(board, unset_workers, 0)

    @staticmethod
    def is_legal_board(board, unset_workers=[], max_height=4):  # TODO - Pranav needs to read over implementation
        """
        Checks the validity of a board.

        :param list board: A board (as defined in the documentation of Board).
        :param list unset_workers: A list of workers (as defined in the documentation of Board) not in the board that
        will be accounted for later (default: empty list).
        :param int max_height: Maximum height (as defined in the documentation of Board) that any cell in the board
        should have (default: 4).
        :return: 'True' if the board is a valid board, else 'False'.
        :rtype: bool
        """
        workers = unset_workers
        for row in range(len(board)):
            for col in range(len(board[0])):
                cell = board[row][col]
                if isinstance(cell, list):
                    cell_height = cell[0]
                    cell_worker = cell[1]
                    max_cell_height = max(max_height, 2)
                    if cell_worker in workers or not RuleChecker.is_valid_worker(cell_worker):
                        return False
                    workers.append(cell_worker)
                else:
                    cell_height = cell
                    max_cell_height = max_height
                if not 0 <= cell_height <= max_cell_height:
                    return False
        num_workers = len(workers)
        if unset_workers:
            if num_workers != 2 and num_workers != 4:
                return False
        else:
            if num_workers != 4:
                return False
        return True

    @staticmethod
    def is_valid_worker(worker):
        return worker in RuleChecker.WORKERS

    @staticmethod
    def is_valid_direction(direction):
        return direction in RuleChecker.DIRECTIONS

    @staticmethod
    def is_valid_color(color):
        return color in RuleChecker.COLORS


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
            if RuleChecker.is_winning_play(board, *play):
                result_plays.append(play)
            else:
                opposition_win = False
                worker = play[0]
                move_dir, build_dir = play[1]

                # player play
                board.move(worker, move_dir)
                board.build(worker, build_dir)

                for opp_play in Strategy.get_legal_plays(board, opp_color):
                    if RuleChecker.is_winning_play(board, *opp_play):
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

        loses = True  # if the player has no plays, which means player lost, which means loop never executes
        for play in Strategy.get_legal_plays(board, color):
            if RuleChecker.is_winning_play(board, *play):
                return False
            worker = play[0]
            move_dir, build_dir = play[1]

            # player play
            board.move(worker, move_dir)
            board.build(worker, build_dir)

            loses = False  # if the opposition has no plays, which means player wins, which means loop never executes
            for opp_play in Strategy.get_legal_plays(board, opp_color):
                if RuleChecker.is_winning_play(board, *opp_play):
                    loses = True
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

            # undoing player play
            board.undo_build(worker, build_dir)
            board.move(worker, board.get_opposite_direction(move_dir))

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
