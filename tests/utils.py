import os
import json


def get_response_from_file(file_name: str) -> dict:
    # get the current directory
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # construct the full path
    file_path = os.path.join(base_dir, "test_data", f"{file_name}.json")

    # open the file and load the json
    with open(file_path, 'r') as f:
        response = json.load(f)
    return response