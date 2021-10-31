from typing import List
from typing import Tuple

import json
import os
import config
import ffmpeg


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


def process_video_for_beeping(timestamps: Timestamps, orig_audio_fpath: str, prefix: str, video_output_fpath: str) -> None:
    """
    with prefix finds the blurred nosound video in tmp
    by orig_audio_fpath finds the audio
    """
    parts = []
    begin = 0

    censor = AudioSegment.from_wav('censor.wav')
    audio = AudioSegment.from_wav(orig_audio_fpath)

    for start, end in timestamp_tuples:
        part = audio[begin*1000:start*1000]
        parts.append(part)  
        
        duration = (end - start) * 1000
        part = censor[:duration]
        parts.append(part)

        begin = end

    parts.append(audio[begin*1000:])
    output = sum(parts[1:], parts[0])

    output_path = os.path.join(config.get_tmp_dir_path(), prefix + "-beeped.wav")
    output.export(output_path, format='wav')

    ffmpeg_input = output_path
    audio = (
            ffmpeg
            .input(ffmpeg_input)
            )

    video_blurred_path = os.path.join(config.get_tmp_dir_path, prefix + ".mp4")
    video_blurred = (
            ffmpeg
            .input(video_blurred_path)
            .video
            )

    (
            ffmpeg
            .concat(video_blurred, audio, v=1, a=1)
            .output(video_output_fpath)
            .run(overwrite_output=True)
            )
    
