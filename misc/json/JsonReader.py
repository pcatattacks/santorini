import json
import sys


def read_json_stream(stream):
    """Generator that yields json values. Taken from Team 3's approach."""
    block = ""
    for line in stream:
        block += line
        try:
            yield json.loads(block)
            block = ""
        except ValueError:
            pass


if __name__ == "__main__":
    for obj in read_json_stream(sys.stdin):
        print(obj)
