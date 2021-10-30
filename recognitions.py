import config

# todo
def do_machine_learning(path_to_video: str) -> tuple[str, str]:
    return (
            '{"type": "audio"}',
            '{"type": "video"}'
            )

def get_all_result_file_names(prefix: str) -> tuple[str, str, str]:
    return (
            prefix + "_audio.json",
            prefix + "_video.json",
            prefix + "_result.mp4",
            )

def make_all_recognition(prefix: str) -> None:
    """
    This is a dummy method right now
    """

    downloaded_video_path = get_downloaded_video_path(prefix)
    # get the file by path
    # process it
    processed_folder = get_processed_dir_path()
    result_audio_fname, result_video_fname, result_processed_video_fname = get_all_result_file_names(prefix)
    result_audio, result_video = get_all_result_file_names(prefix)

    with open(os.path.join(processed_folder, result_audio_fname), "wt") as f:
        f.write(result_audio)

    with open(os.path.join(processed_folder, result_video_fname), "wt") as f:
        f.write(result_video) 

    with open(os.path.join(processed_folder, result_processed_video_fname), "wt") as f:
        f.write("oh boy...") # todo



