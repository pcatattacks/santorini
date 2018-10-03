import json


def take_input():
    inputs = []
    while True:
        try:
            line = input()
            inputs.append(line)
        except EOFError:
            break
    return inputs


def parse_json(input_line, index):
    try:
        val = json.loads(input_line)
        return json.dumps({"index": index, "value": val})
    except ValueError:
        return "Bad JSON object detected."


def main():
    inputs = take_input()
    results = []
    for i in range(len(inputs)):
        results.append(parse_json(inputs[i], i))

    for i in range(len(results)-1, -1, -1):
        print(results[i])


if __name__ == "__main__":
    main()
