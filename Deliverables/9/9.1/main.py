import sys
from importlib.machinery import SourceFileLoader
from JsonParser import parse_json
from Admin import RoundRobinAdmin, SingleEliminationAdmin


def main(tournament, num_remote_players, host, port, default_player):
    if num_remote_players < 1 or not isinstance(port, int):
        raise ValueError()

    if tournament == "cup":
        admin = SingleEliminationAdmin(host, port, num_remote_players, fallback_player=default_player)
    elif tournament == "league":
        admin = RoundRobinAdmin(host, port, num_remote_players, fallback_player=default_player)
    else:
        raise ValueError()

    try:  # wrapped in try-except to gracefully close the socket if anything unexpected happens.
        admin.run_tournament()
        admin.print_rankings()
    except Exception as e:
        print(e)
        admin.s.close()


if __name__ == "__main__":
    try:
        tournament_type, n = sys.argv[1:]

        with open("santorini.config") as f:
            data = parse_json(f.read())[0]["value"]
            ip, port = data["IP"], data["port"]
            default_player_path = data["default-player"]

        DefaultPlayerModule = SourceFileLoader("DefaultPlayerModule", default_player_path).load_module()
        DefaultPlayer = DefaultPlayerModule.Player

        main(tournament_type[1:], int(n), ip, port, DefaultPlayer)
    except ValueError:
        print("usage: ./santorini.sh [option] ... [-cup n | -league n]")
        print("n must be a positive integer.")
        sys.exit(1)
    except AttributeError:
        print("Module at path given in santorini.config does not have attribute named 'Player'!")
        sys.exit(1)

