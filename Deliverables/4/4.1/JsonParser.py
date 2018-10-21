import json
import sys


def take_input():
    input_string = ""
    while True:
        try:
            line = input()
            if line.strip() == "":
                continue
            input_string += line + "\n"
        except EOFError:
            break
    return input_string


def match_delimiters(opening, closing):
    return (opening == "{" and closing == "}") or \
           (opening == "[" and closing == "]")


def parse_json(input_string):
    stack = []
    start_delimiters = ["[", "{"]
    end_delimiters = ["]", "}"]
    object_index = 1
    start_index = 0
    results = []
    in_value = False
    try:
        for i, char in enumerate(input_string):
            if in_value:
                if char == '\n':
                    try:
                        val = "[" + input_string[start_index:i] + "]"
                        results.append({"index": object_index,
                                        "value": json.loads(val)[0]})
                        in_value = False
                        object_index += 1
                    except ValueError:
                        continue
            else:
                if char in start_delimiters:
                    if not stack:
                        start_index = i
                    stack.append(char)
                elif char in end_delimiters:
                    if not match_delimiters(stack.pop(), char):
                        print("Malformed JSON value at index {}.".format(object_index))
                        sys.exit(1)
                    if not stack:
                        results.append({"index": object_index,
                                        "value": json.loads(input_string[start_index:i + 1])})
                        start_index = i + 1
                        object_index += 1
                elif not stack:  # starting a new value
                    in_value = True
                    start_index = i
        if stack:
            print("Malformed JSON value at index {}.".format(object_index))
            # sys.exit(1)
    except ValueError as e:
        print("Malformed JSON value at index {}.".format(object_index), e)
        # sys.exit(1)
    except IndexError as e:
        print("Malformed JSON value at index {}.".format(object_index-1), e)
        # sys.exit(1)
    return results


def main():
    results = parse_json(take_input())
    for val in reversed(results):
        print(json.dumps(val))


if __name__ == "__main__":
    main()
