from typing import List
from typing import Tuple

import json
import os

import ffmpeg

Timestamps = List[Tuple[float, float]]

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
    last_cut = timestamps[-1][1]

    first_audio_part = (
            ffmpeg
            .input(video_source_fpath)
            .audio
            .filter('atrim', end=first_cut)
            )

    last_audio_part = (
            ffmpeg
            .input(video_source_fpath)
            .audio
            .filter('atrim', start=last_cut)
            )

    def timestamp_to_beep_of_length(timestamp):
        length = timestamp[1] - timestamp[0]
        return (
                ffmpeg
                .input("censor.wav")
                .filter('atrim', end=length)
                )
    all_beeps = list(map(timestamp_to_beep_of_length, timestamps))
    middle_audios = []
    for i in range(len(timestamps)):
        if i == len(timestamps) - 1:
            break
        start = timestamps[i][0]
        end = timestamps[i + 1][1]
        new_part = (
                ffmpeg
                .input(video_source_fpath)
                .audio
                .filter('atrim', start=start, end=end)
                )
        middle_audios.append(new_part)

    res_audios = [first_audio_part]
    for i in range(len(all_beeps) + len(middle_audios)):
        if i % 2 == 0:
            res_audios.append(all_beeps[i // 2])
        else:
            print(i // 2 + 1)
            res_audios.append(middle_audios[i // 2])
    res_audios.append(last_audio_part)
    res_audio = (
            ffmpeg
            .filter(res_audios, 'concat', n=len(res_audios), v=0, a=1)
            )
    (
            ffmpeg
            .concat(video, res_audio, v=1, a=1)
            .output(video_output_fpath)
            .run(overwrite_output=True)
            )

