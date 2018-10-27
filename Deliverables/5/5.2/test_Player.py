import pytest

@pytest.fixture()
def exe_name():
    """
    :return: name of executable file for deliverable.
    """
    return "player-test-harness.sh"


@pytest.mark.parametrize("input_num", [1, 2, 3, 4, 5])
def test_input_x(exe_name, input_num):
    # getting output from executable script
    actual_output = subprocess.check_output(["./{filename} < input{num}".format(filename=exe_name, num=input_num)],
                                            shell=True)
    actual_output = actual_output.decode("utf-8")
    actual_output = parse_json(actual_output)  # parsing json into python list of values
    with open("output{}".format(input_num), "r") as output_file:
        # reading + parsing output json into python list of values
        data = output_file.read() + '\n'  # adding newline for our parser
        expected_output = parse_json(data)
    # print(expected_output)
    # print(actual_output)
    assert expected_output == actual_output