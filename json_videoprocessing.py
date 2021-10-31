import json
import os


def parser_to_json(filename, fps, frame_array):
    for frame in frame_array:
        frame_num = frame[0]
        coord1 = frame[1]
        coord2 = frame[2]
        json_video_print(filename, frame_num, fps,  coord1, coord2)


def json_video_print(filename, frame_num, fps, corner1, corner2):
    # check on 0 size and if exists JSON file
    if not os.path.exists(filename) or os.stat(filename).st_size == 0:
        with open(filename, 'w') as outfile:
            data = {'result': []}
            json.dump(data, outfile)
    with open(filename, 'r+') as f:
        # First we load existing data into a dict
        data = json.load(f)
        x = {"time_start" : frame_num/fps, "time_end" : (frame_num+1)/fps,
             "corner_1": corner1, "corner_2": corner2}
        # Join new data with data of file inside result
        data["result"].append(x)
        # Sets file's current position at offset.
        f.seek(0)
        # convert back to json.
        json.dump(data, f, indent=4)


# example of input
# parser_to_json(25, [[255, (344, 444), (123, 345)], [342, (324, 214), (134, 234)]])

#fps, frameArray = recognize("source.mp4", "res.mp4")
# frameNum = frameArray[0][0]
# x1y1 = frameArray[0][1]
# x1 = frameArray[0][1][0]
