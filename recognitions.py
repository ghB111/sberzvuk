from typing import Tuple

import os

import config
from video_blur import recognize

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

    # make a blurred video
    recognize(downloaded_video_path, os.path.join(config.get_tmp_dir_path(), prefix))

    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)

    # json stuff
    with open(os.path.join(processed_folder, result_audio_fname), "w") as f:
        f.write(result_audio)

    # json stuff
    with open(os.path.join(processed_folder, result_video_fname), "w") as f:
        f.write(result_video) 

    # final video
    with open(os.path.join(processed_folder, result_processed_video_fname), "w") as f:
        f.write("oh boy...") # todo



