import sys
import socket
from JsonParser import parse_json


def main(tournament, num_remote_players, host, port):
    if num_remote_players < 1 or not isinstance(port, int):
        raise ValueError()

    # TODO - accept num_remote_player connections
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind((host, port))
    listener.listen(num_remote_players)  # WIP

    if tournament == "cup":
        pass  # TODO
    elif tournament == "league":
        pass  # TODO
    else:
        raise ValueError()


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

