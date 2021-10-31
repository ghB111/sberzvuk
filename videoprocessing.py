from typing import List
from typing import Tuple

import json
import os
import config


from pydub import AudioSegment

Timestamps = List[Tuple[float, float]]
def audio_parser_to_json(filename, array):
    for x in array:
        time_start = x[0]
        time_end = x[1]
        json_audio_print(filename, time_start, time_end)


def json_audio_print(filename, time_start, time_end):
    # check on 0 size and if exists JSON file
    if not os.path.exists(filename) or os.stat(filename).st_size == 0:
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


def process_video_for_beeping(timestamps: Timestamps, orig_audio_fpath: str, video_output_fpath: str) -> None:








    # b.export('new_audio.wav', format='wav')
