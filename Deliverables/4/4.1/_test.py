import pytest
from JsonParser import parse_json
import subprocess


@pytest.fixture()
def exe_name():
    """
    :return: name of executable file for deliverable.
    """
    return "rule-checker-test-harness.sh"


def test_all(exe_name):
    """
    Will check all input file values with output file values to see if they're the same.

    Checks by creating a python representation of the json values in input and output files and comparing them, not the
    raw strings.

    :param string exe_name: name of executable
    """
    for i in range(1, 6):
        # getting output from executable script
        actual_output = subprocess.check_output(["./{filename} < input{num}".format(filename=exe_name, num=i)],
                                                shell=True)
        actual_output = parse_json(actual_output)  # parsing json into python list of values
        with open("output{}".format(i), "r") as output_file:
            # reading + parsing output json into python list of values
            expected_output = parse_json(output_file.readlines())
        assert expected_output == actual_output
