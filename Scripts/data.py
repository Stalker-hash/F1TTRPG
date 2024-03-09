import json


# loads the json data from the file and returns it as a dictionary
def load_json_data(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data


def format_lap_time(time_in_seconds):
    minutes, seconds = divmod(time_in_seconds, 60)
    seconds, milliseconds = divmod(seconds, 1)
    milliseconds = round(milliseconds * 1000)
    return f"{int(minutes)}m {int(seconds)}s {milliseconds}ms"


def find_driver_index(driver_name, drivers):
    for i, driver in enumerate(drivers):
        if driver.name == driver_name:
            return i
    return -1
