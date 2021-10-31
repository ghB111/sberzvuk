from typing import Tuple

import os
from json_videoprocessing import parser_to_json
import config
from video_blur import recognize
from names_detector import NamesDetector

from videoprocessing import json_audio_print

def make_mono_wav_of_file(prefix: str) -> str:
    res_path = os.path.join(config.get_tmp_dir_path(), prefix + ".wav")
    proc = subprocess.Popen(["ffmpeg",
        "-i",
        prefix + ".mp4",
        "-ac 1",
        res_path])
    proc.wait()
    return res_path


def get_all_result_file_names(prefix: str) -> Tuple[str, str, str]:
    return (
            prefix + "_audio.json",
            prefix + "_video.json",
            prefix + "_result.mp4"
            )

def make_all_recognition(prefix: str) -> None:

    downloaded_video_path = config.get_downloaded_video_path(prefix)
    processed_folder = config.get_processed_dir_path()
    result_audio_fname, result_video_fname, result_processed_video_fname = get_all_result_file_names(prefix)

    detector = NamesDetector()
    # make a blurred video
    fps, frame_array = recognize(downloaded_video_path, os.path.join(config.get_tmp_dir_path(), prefix + ".mp4"))
    sound_fpath = make_mono_wav_of_file(prefix)
    timestamps_to_beep = detector.process_audio(sound_fpath)

    final_video_dest = os.path.join(processed_folder, result_video_fname)
    process_video_for_beeping(timestamps_to_beep, sound_fpath, prefix, final_video_dest)

    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)

    result_audio_path = os.path.join(processed_folder, result_audio_fname)
    json_audio_print(result_audio_path, timestamps)

    result_video_path = os.path.join(processed_folder, result_audio_fname)
    parser_to_json(result_video_path, fps, frame_array)


