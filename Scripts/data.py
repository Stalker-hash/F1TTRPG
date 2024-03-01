import json

#loads the json data from the file and returns it as a dictionary
def load_json_data(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data
