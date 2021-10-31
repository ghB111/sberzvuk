import json
import os


def json_audio_print(filename, time_start, time_end):
    if not os.path.exists(filename):
        with open(filename, 'w') as outfile:
            data = {'result': []}
            json.dump(data, outfile)
    with open(filename, 'r+') as f:
        # First we load existing data into a dict
        data = json.load(f)
        x = {"time_start" : time_start, "time_end" : time_end}
        # Join new data with data of file inside result
        data["result"].append(x)
        # Sets file's current position at offset.
        f.seek(0)
        # convert back to json.
        json.dump(data, f, indent=4)


json_audio_print('data.json', 228, 1337)
