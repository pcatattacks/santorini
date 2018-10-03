#!/usr/bin/python3

import json
import sys


def take_input():
    input_string = ""
    while True:
        try:
            input_string += input()
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
    try:
        for i in range(len(input_string)):
            if input_string[i] in start_delimiters:
                stack.append(input_string[i])
            elif input_string[i] in end_delimiters:
                if not match_delimiters(stack.pop(), input_string[i]):
                    print("Malformed JSON object at index {}.".format(object_index))
                    sys.exit(1)
                if not stack:
                    results.append({"index": object_index,
                                    "value": json.loads(input_string[start_index:i+1])})
                    start_index = i + 1
                    object_index += 1
        if stack:
            print("Malformed JSON object at index {}.".format(object_index))
            sys.exit(1)
    except ValueError:
        print("Malformed JSON object at index {}.".format(object_index))
        sys.exit(1)
    return results


def main():
    results = parse_json(take_input())
    for i in range(len(results)-1, -1, -1):
        print(json.dumps(results[i]))


if __name__ == "__main__":
    main()
