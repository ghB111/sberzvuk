import json
import os


def json_video_print(filename, frameNum, fps, corner1, corner2):
    # check on 0 size and if exists JSON file
    if not os.path.exists(filename) or os.stat(filename).st_size == 0:
        with open(filename, 'w') as outfile:
            data = {'result': []}
            json.dump(data, outfile)
    with open(filename, 'r+') as f:
        # First we load existing data into a dict
        data = json.load(f)
        x = {"time_start" : frameNum/fps, "time_end" : (frameNum+1)/fps,
             "corner_1": corner1, "corner_2": corner2}
        # Join new data with data of file inside result
        data["result"].append(x)
        # Sets file's current position at offset.
        f.seek(0)
        # convert back to json.
        json.dump(data, f, indent=4)


# example of input
json_video_print('data.json', 355, 25, [123, 456], [456, 789])
