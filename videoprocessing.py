from typing import List
from typing import Tuple

import json
import os

import ffmpeg

Timestamps = List[Tuple[float, float]]

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


def process_video_for_beeping(timestamps: Timestamps, video_source_fpath: str, video_output_fpath: str) -> None:
    if len(timestamps) == 0:
        (
                ffmpeg
                .input(video_source_fpath)
                .output(video_output_fpath)
                .run(overwrite_output=True)
                )
        return
    video = (
            ffmpeg
            .input(video_source_fpath)
            .video
            )
    first_cut = timestamps[0][0]
    first_audio_part = (
            ffmpeg
            .input(video_source_fpath)
            .audio
            .filter('atrim', end=first_cut)
            )

    cur_audio = first_audio_part
    last_end = None
    for (start, end) in timestamps:
        if last_end is not None:
            # merge the original audio that is before the current start timestamp
            passed_audio = (
                    ffmpeg
                    .input(video_source_fpath)
                    .audio
                    .filter('atrim', start=last_end, end=start)
                    )
            cur_audio = (
                    cur_audio
                    .filter((cur_audio, passed_audio), 'concat', n=2, v=0, a=1)
                    )
        audio_beep = (
                ffmpeg
                .input('censor.wav')
                .filter('atrim', end=end-start)
                .filter('aeval', exprs="val(ch)/2") # make twice as silent
                )
        cur_audio = (
                ffmpeg
                .filter((cur_audio, audio_beep), 'concat', n=2, v=0, a=1)
                )
        last_end = end

    last_audio_part = (
            ffmpeg
            .input(video_source_fpath)
            .audio
            .filter('atrim', start=timestamps[-1][1])
            )
    res_audio = (
            ffmpeg
            .filter((cur_audio, last_audio_part), 'concat', n=2, v=0, a=1)
            )
    (
            ffmpeg
            .concat(video, res_audio, v=1, a=1)
            .output(video_output_fpath)
            .run(overwrite_output=True)
            )

