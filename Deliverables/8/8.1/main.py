import sys
from JsonParser import parse_json
from Admin import RoundRobinAdmin
from SmartPlayer import SmartPlayer


def main(num_games, host, port, default_player):
    if num_games < 1 or not isinstance(port, int):
        raise ValueError()

    admin = RoundRobinAdmin(host, port, 1, fallback_player=default_player)
    try:
        admin.run_tournament(num_games)
        admin.print_rankings()
    except Exception as e:
        print(e)
        admin.s.close()


if __name__ == "__main__":
    try:
        n = sys.argv[1]

        with open("santorini.config") as f:
            data = parse_json(f.read())[0]["value"]
            ip, port = data["IP"], data["port"]

        main(int(n), ip, port, SmartPlayer)
    except ValueError:
        print("usage: ./santorini.sh [option] ... [n]")
        print("n must be integer >= 1.")
        sys.exit(1)
    except AttributeError:
        print("Module at path given in santorini.config does not have attribute named 'Player'!")
        sys.exit(1)
