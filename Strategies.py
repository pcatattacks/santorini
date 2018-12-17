from abc import ABC, abstractmethod
import random
from RuleChecker import RuleChecker
from CustomExceptions import ContractViolation
import math


class BaseStrategy(ABC):
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

    @abstractmethod
    def get_placements(self, board, color):
        """

        :param Board board: an instance of Board (refer to documentation of Board class).
        :param str color: color (as defined above)
        :return: `list` of [position1, position2] where position1 and position2 are positions of the first and second
        worker respectively. See `worker` and `position` in Board.py documentation.
        :rtype: list
        """
        pass

    @abstractmethod
    def get_play(self, board, color):
        """

        :param Board board: an instance of Board (refer to documentation of Board class).
        :param str color: color (as defined above)
        :return: a play (as defined above)
        :rtype: list
        """
        pass

    @staticmethod
    def get_legal_plays(board, color):
        """
        Returns a list of all possible legal plays for players of the given color.

        :param Board board: an instance of Board (refer to documentation of Board class).
        :param str color: color (as defined above)
        :return: a `list` of legal plays (as defined above)
        :rtype: list
        """
        if not RuleChecker.is_valid_color(color):
            raise ContractViolation("Invalid color given: {}".format(color))

        legal_plays = []
        players = [str(color + "1"), str(color + "2")]
        player_movable_directions = [[], []]

        # Valid Move directions
        for direc in RuleChecker.DIRECTIONS:
            for i, player in enumerate(players):
                if RuleChecker.is_valid_move(board, player, direc):
                    player_movable_directions[i].append(direc)

        # Constructing all possible legal plays
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


class RandomStrategy(BaseStrategy):
    """
    Strategy implementation that returns random placements and random plays, if they are legal.
    """

    def get_placements(self, board, color):
        """
        Returns random worker placements of given color.

        :param Board board: an instance of Board (refer to documentation of Board class).
        :param str color: color (as defined above)
        :return: `list` of [position1, position2] where position1 and position2 are positions of the first and second
        worker respectively. See `worker` and `position` in Board.py documentation.
        :rtype: list
        """
        num_rows, num_cols = board.get_dimensions()
        placements = []
        while len(placements) != 2:
            placement = [random.randint(0, num_rows - 1), random.randint(0, num_cols - 1)]
            while board.has_worker(*placement) or placement in placements:
                placement = [random.randint(0, num_rows - 1), random.randint(0, num_cols - 1)]
            placements.append(placement)
        assert len(placements) == 2  # shouldn't needed since we're checking that the board is valid at the start, but
        # may as well
        return placements

    def get_play(self, board, color):
        """
        Returns a random play from all possible legal plays. If no legal plays, returns an empty list.

        :param Board board:
        :param str color:
        :return: A random play.
        :rtype: list
        """
        plays = self.get_legal_plays(board, color)
        if not plays:
            return []
        return random.choice(plays)


class NLooksAheadStrategy(BaseStrategy):

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

    def __init__(self, num_looks_ahead):
        if not isinstance(num_looks_ahead, int) or num_looks_ahead < 1:
            raise ContractViolation("num_looks_ahead must be a positive integer! Given: {}".format(num_looks_ahead))
        self.num_looks_ahead = num_looks_ahead

    def get_placements(self, board, color):
        """
        Returns worker placements of given color, by scheme of choosing the first two unoccupied corner cells, starting
        from top left, in the clockwise direction.

        :param Board board: an instance of Board (refer to documentation of Board class).
        :param str color: color (as defined above)
        :return: `list` of [position1, position2] where position1 and position2 are positions of the first and second
        worker respectively. See `worker` and `position` in Board.py documentation.
        :rtype: list
        """
        # num_rows, num_cols = board.get_dimensions()
        # corners = ([0, 0], [0, num_cols-1], [num_rows-1, num_cols-1], [num_rows-1, 0])
        # placements = []
        # for corner in corners:
        #     if not board.has_worker(*corner):
        #         placements.append(corner)
        #     if len(placements) == 2:
        #         break
        # assert len(placements) == 2  # shouldn't needed since we're checking that the board is valid at the start, but
        # # may as well
        # return placements

        # making this return random placements now, not corners - so we can play against local players.
        # TODO - make the placements somewhat strategic?
        num_rows, num_cols = board.get_dimensions()
        placements = []
        while len(placements) != 2:
            placement = [random.randint(0, num_rows - 1), random.randint(0, num_cols - 1)]
            while board.has_worker(*placement) or placement in placements:
                placement = [random.randint(0, num_rows - 1), random.randint(0, num_cols - 1)]
            placements.append(placement)
        assert len(placements) == 2  # shouldn't needed since we're checking that the board is valid at the start, but
        # may as well
        return placements

    def get_play(self, board, color):
        """
        Returns a winning or random play from all possible plays that don't result in a loss within self.num_looks_ahead
         of the opponents moves.

        :param Board board: an instance of Board (refer to documentation of Board class).
        :param str color: color (as defined above)
        :return: a play (as defined above)
        :rtype: list
        """
        plays = NLooksAheadStrategy.get_plays(board, color, self.num_looks_ahead)
        if not plays:
            return []
        for play in plays:
            if len(play[1]) == 1:  # return first winning play found in plays list
                return play
        return random.choice(plays)

    @staticmethod
    def get_plays(board, color, num_look_ahead):  # TODO - make private method
        """
        Returns a list of all possible legal plays that cannot not result in the opposing player winning within the next
        `num_look_ahead` moves.

        CONTRACT:
         - `num_look_ahead` must be >= 1

        :param Board board: an instance of Board (refer to documentation of Board class).
        :param str color: color (as defined above)
        :param int num_look_ahead: number of moves to look ahead by
        :return: a `list` of legal plays (as defined above)
        :rtype: `list`
        """
        if not RuleChecker.is_valid_color(color):
            raise ContractViolation("Invalid color given: {}".format(color))

        available_colors = list(RuleChecker.COLORS)
        available_colors.remove(color)
        opp_color = available_colors[0]

        result_plays = []

        for play in NLooksAheadStrategy.get_legal_plays(board, color):
            # avoid circular import
            # if RuleChecker.is_winning_play(board, *play):
            #     result_plays.append(play)
            # print("checking", play)  # debug
            if len(play[1]) == 1:
                result_plays.append(play)
            else:
                opposition_win = False
                worker = play[0]
                move_dir, build_dir = play[1]

                # player play
                board.move(worker, move_dir)
                board.build(worker, build_dir)

                opp_legal_plays = NLooksAheadStrategy.get_legal_plays(board, opp_color)
                if any(len(opp_play[1]) == 1 for opp_play in opp_legal_plays):  # try and prune search
                    opposition_win = True
                else:
                    for opp_play in opp_legal_plays:
                        # avoid circular import
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

                            opposition_win = NLooksAheadStrategy._loses_in_n_moves(board, color, num_look_ahead - 1)

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
        :param str color:
        :param int n:
        :return:
        :rtype: bool
        """
        if n == 0:
            return False

        opp_color = "blue" if color == "white" else "white"

        legal_plays = NLooksAheadStrategy.get_legal_plays(board, color)
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

            opp_legal_plays = NLooksAheadStrategy.get_legal_plays(board, opp_color)
            if any(len(opp_play[1]) == 1 for opp_play in opp_legal_plays):  # try and prune search
                loses = True
            else:
                loses = False  # if opposition has no plays, which means player wins, which means loop never executes
                for opp_play in opp_legal_plays:
                    # avoid circular import
                    # if RuleChecker.is_winning_play(board, *opp_play):
                    #     loses = True
                    if len(opp_play[1]) == 1:
                        loses = True
                        break
                    elif n > 1:
                        opp_worker = opp_play[0]
                        opp_move_dir, opp_build_dir = opp_play[1]

                        # opposition play
                        board.move(opp_worker, opp_move_dir)
                        board.build(opp_worker, opp_build_dir)

                        loses = NLooksAheadStrategy._loses_in_n_moves(board, color, n - 1)  # recurse

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


class SmartStrategy(BaseStrategy):
    def __init__(self, num_looks_ahead=1):
        if not isinstance(num_looks_ahead, int) or num_looks_ahead < 1:
            raise ContractViolation("num_looks_ahead must be a positive integer! Given: {}".format(num_looks_ahead))
        self.num_looks_ahead = num_looks_ahead

    def get_placements(self, board, color):
        opp_color = RuleChecker.COLORS[0] if color == RuleChecker.COLORS[1] else RuleChecker.COLORS[1]
        opp_workers = [opp_color + "1", opp_color + "2"]

        if not board.worker_exists(opp_workers[0]):
            rows, cols = board.get_dimensions()
            half_row = rows / 2

            return [[math.floor(half_row), 0], [math.floor(half_row) + 1, 0]]
        else:
            return self._get_placements_helper(board, opp_workers)

    def _get_placements_helper(self, board, opp_workers):
        distances = {}

        rows, cols = board.get_dimensions()
        for row in range(rows):
            for col in range(cols):
                distances[str(row) + str(col)] = SmartStrategy._get_worker_distance(board, row, col, opp_workers[0]) + \
                                                 SmartStrategy._get_worker_distance(board, row, col, opp_workers[1])

        distances_list = [(coor, distances[coor]) for coor in distances]
        distances_list.sort(key=lambda x: x[1], reverse=True)

        placements = []

        # for i in range(2):
        #     coor_str = distances_list[i][0]
        #     coor_len = len(coor_str)
        #
        #     placement_row = int(coor_str[0:coor_len//2])
        #     placement_col = int(coor_str[coor_len//2:coor_len])
        #
        #     placements.append([placement_row, placement_col])

        far_coor_str = distances_list[0][0]
        far_coor_len = len(far_coor_str)
        clo_coor_str = distances_list[len(distances_list) - 3][0]
        clo_coor_len = len(clo_coor_str)

        far_placement_row = int(far_coor_str[0:far_coor_len // 2])
        far_placement_col = int(far_coor_str[far_coor_len // 2:far_coor_len])
        clo_placement_row = int(clo_coor_str[0:clo_coor_len // 2])
        clo_placement_col = int(clo_coor_str[clo_coor_len // 2:clo_coor_len])

        placements.append([far_placement_row, far_placement_col])
        placements.append([clo_placement_row, clo_placement_col])

        return placements

    def get_play(self, board, color):
        print("strategizing...")  # debug
        plays = self.get_legal_plays(board, color)
        if not plays:
            return []

        play_data = {}
        play_scores = {}
        play_win_pcts = {}
        play_loss_pcts = {}

        for play in plays:
            worker, directions = play

            if len(directions) == 1:
                return play

            move_dir, build_dir = directions

            board.move(worker, move_dir)
            board.build(worker, build_dir)

            play_str = worker + move_dir + build_dir

            play_data[play_str] = play
            play_scores[play_str] = 0
            play_win_pcts[play_str] = 0
            play_loss_pcts[play_str] = 0

            self._score_look_ahead(board, play_str, play_scores, play_win_pcts, play_loss_pcts, color, False, 1, self.num_looks_ahead)

            win_score = play_win_pcts[play_str] * 161
            loss_score = play_loss_pcts[play_str] * -161
            play_scores[play_str] += win_score + loss_score

            board.undo_build(worker, build_dir)
            board.move(worker, board.get_opposite_direction(move_dir))

        results = [(play, play_scores[play]) for play in play_scores]
        results.sort(key=lambda x: x[1], reverse=True)
        return play_data[results[0][0]]

    def _score_look_ahead(self, board, play, play_scores, play_win_pcts, play_loss_pcts, color, is_turn, prop, num_looks_ahead):
        if is_turn:
            turn_color = color
        else:
            turn_color = RuleChecker.COLORS[0] if color == RuleChecker.COLORS[1] else RuleChecker.COLORS[1]

        turn_plays = self.get_legal_plays(board, turn_color)
        if not turn_plays:
            if is_turn:
                play_loss_pcts[play] += prop
            else:
                play_win_pcts[play] += prop
            return

        for turn_play in turn_plays:
            turn_worker, turn_directions = turn_play
            if len(turn_directions) == 1:
                if is_turn:
                    play_win_pcts[play] += prop
                else:
                    play_loss_pcts[play] += prop
                return

        # prop /= len(turn_plays)

        best_score = None

        for turn_play in turn_plays:
            turn_worker, turn_directions = turn_play
            turn_move_dir, turn_build_dir = turn_directions

            board.move(turn_worker, turn_move_dir)
            board.build(turn_worker, turn_build_dir)

            if num_looks_ahead > 1:
                # self._score_look_ahead(board, play, play_scores, play_win_pcts, play_loss_pcts, color, (not is_turn), prop, num_looks_ahead-1)
                self._score_look_ahead(board, play, play_scores, play_win_pcts, play_loss_pcts, color, (not is_turn),
                                       (prop / len(turn_plays)), num_looks_ahead - 1)
            else:
                # play_scores[play] += self._score_board(board, color) * prop
                turn_score = self._score_board(board, color)
                if best_score is None:
                    best_score = turn_score
                elif (is_turn and turn_score > best_score) or (not is_turn and turn_score < best_score):
                    best_score = turn_score

            board.undo_build(turn_worker, turn_build_dir)
            board.move(turn_worker, board.get_opposite_direction(turn_move_dir))

        if best_score is not None:
            play_scores[play] += best_score * prop

    def _score_board(self, board, color):
        opp_color = RuleChecker.COLORS[0] if color == RuleChecker.COLORS[1] else RuleChecker.COLORS[1]
        return self._score_board_helper(board, color) - self._score_board_helper(board, opp_color)

    @staticmethod
    def _score_board_helper(board, color):
        score = 0
        workers = [color + "1", color + "2"]
        for worker in workers:
            row, col, height = board.get_worker_position(worker)
            score += height * 16
            for direction in RuleChecker.DIRECTIONS:
                adj_height = board.get_height(worker, direction)
                if adj_height and adj_height < 4:
                    score += adj_height * 2 + adj_height - height
                if board.is_occupied(worker, direction):
                    score -= 1
        return score

    @staticmethod
    def _get_worker_distance(board, row, col, worker):
        worker_row, worker_col, worker_height = board.get_worker_position(worker)
        if worker_row == row and worker_col == col:
            rows, cols = board.get_dimensions()
            distance = -1 * (rows + cols)
        else:
            distance = math.sqrt(pow(row - worker_row, 2) + pow(col - worker_col, 2))
        return distance


class GreedyStrategy(BaseStrategy):
    """
    Implementation of strategy that greedily chooses a play based on scoring a board using a heuristic.

    # TODO - could parameterize further by passing the heuristic function as an argument. or could create subclass for
    different types of heuristics. Make _score_board() an abstract method.
    """

    def get_placements(self, board, color):
        """
        # TODO - create heuristic for placements too, returns random worker placements of given color right now.

        :param Board board: an instance of Board (refer to documentation of Board class).
        :param str color: color (as defined above)
        :return: `list` of [position1, position2] where position1 and position2 are positions of the first and second
        worker respectively. See `worker` and `position` in Board.py documentation.
        :rtype: list
        """
        num_rows, num_cols = board.get_dimensions()
        placements = []
        while len(placements) != 2:
            placement = [random.randint(0, num_rows - 1), random.randint(0, num_cols - 1)]
            while board.has_worker(*placement) or placement in placements:
                placement = [random.randint(0, num_rows - 1), random.randint(0, num_cols - 1)]
            placements.append(placement)
        assert len(placements) == 2  # shouldn't needed since we're checking that the board is valid at the start, but
        # may as well
        return placements

    def get_play(self, board, color):
        """
        Returns the best play given a list of plays, using a heuristic function. Winning plays are returned immediately.

        :param Board board: an instance of Board (refer to documentation of Board class).
        :param str color: color (as defined above)
        :return: a legal play (as defined above)
        :rtype: list
        """
        plays = self.get_legal_plays(board, color)
        if not plays:
            return []

        best_score = 0
        best_play = None
        for play in plays:
            worker, directions = play
            if len(directions) == 1:
                return play
            move_dir, build_dir = directions
            board.move(worker, move_dir)
            board.build(worker, build_dir)
            score = self._score_board(board, color)
            if score > best_score:
                best_score = score
                best_play = play
            board.undo_build(worker, build_dir)
            board.move(worker, board.get_opposite_direction(move_dir))
        return best_play

    @staticmethod
    def _score_board(board, color):
        """
        A heuristic function used to score a given board for a player of a given color. It assigns points for the height
        of cells under and adjacent to the player's workers.

        :param Board board: an instance of Board (refer to documentation of Board class).
        :param str color: color (as defined above)
        :return: a numeric score for the given board
        :rtype: float
        """
        score = 0
        workers = [color + "1", color + "2"]
        for worker in workers:
            row, col, height = board.get_worker_position(worker)
            score += height * 5
            for direction in RuleChecker.DIRECTIONS:
                adj_height = board.get_height(worker, direction)
                if adj_height:
                    score += adj_height
        return score


class InteractiveStrategy(BaseStrategy):
    """
    Implementation of strategy that allows manual selections to be made for plays and placements from the console.

    Does not check for legality of placements or plays.
    """

    def get_placements(self, board, color):
        print("You were assigned color {}.".format(color))
        InteractiveStrategy._display_board_state(board)

        placements = []
        while len(placements) != 2:
            try:
                placement = [int(x) for x in input("Please make a placement in the form of row, col: ").strip().split(",")]
                placements.append(placement)
            except ValueError:
                print("row, col must be comma separated integers.")

        return placements

    def get_play(self, board, color):
        InteractiveStrategy._display_board_state(board)

        worker = input("Please select {} worker to play with: ".format(color))
        move_dir = input("Please select move direction: ".format(color)).upper()
        build_dir = input("Please select build direction or skip: ".format(color)).upper()
        return [worker, [move_dir, build_dir]] if build_dir else [worker, [move_dir]]

    @staticmethod
    def _display_board_state(board):
        print("\nBoard State:")
        print("---------------------------")
        print(board)


class CheatingStrategy(BaseStrategy):
    def get_placements(self, board, color):
        placements = []
        rows, cols = board.get_dimensions()
        for i in range(2):
            row = random.randint(0, rows-1)
            col = random.randint(0, cols-1)
            placements.append([row, col])
        return placements

    def get_play(self, board, color):
        workers = [color + "1", color + "2"]
        worker = random.choice(workers)
        directions = [random.choice(RuleChecker.DIRECTIONS)]
        if random.random() < 0.9:
            directions.append(random.choice(RuleChecker.DIRECTIONS))
        play = [worker, directions]
        return play

