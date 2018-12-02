import sys
from JsonParser import parse_json
from Admin import RoundRobinAdmin, SingleEliminationAdmin


def main(tournament, num_remote_players, host, port):
    if num_remote_players < 1 or not isinstance(port, int):
        raise ValueError()

    if tournament == "cup":
        admin = SingleEliminationAdmin(host, port, num_remote_players)
    elif tournament == "league":
        admin = RoundRobinAdmin(host, port, num_remote_players)
    else:
        raise ValueError()

    try:  # wrapped in try-except to gracefully close the socket.
        admin.run_tournament()
        admin.print_rankings()
    except Exception:
        admin.s.close()


if __name__ == "__main__":
    try:
        tournament_type, n = sys.argv[1:]

        with open("santorini.config") as f:
            data = parse_json(f.read())[0]["value"]
            ip, port = data["IP"], data["port"]

        main(tournament_type[1:], int(n), ip, port)
    except ValueError:
        print("usage: ./santorini.sh [option] ... [-cup n | -league n]")
        print("n must be a positive integer.")
        sys.exit(1)

