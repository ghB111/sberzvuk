import os, sys

DOWNLOADS_FOLDER = "downloads"
def get_downloads_dir_path() -> str:
    return os.path.join(os.getcwd(), DOWNLOADS_FOLDER)

def get_downloaded_video_path(prefix: str) -> str:
    return os.path.join(get_downloads_dir_path(), prefix)

PROCESSED_FOLDER = "processed"
def get_processed_dir_path() -> str:
    return os.path.join(os.getcwd(), PROCESSED_FOLDER)

# tmp folder is for blurred video files without sound
# files from tmp then get processed by adding beeped audio and
# the result will be in the processed dir
TMP_FOLDER = "tmp"
def get_tmp_dir_path() -> str:
    return os.path.join(os.getcwd(), TMP_FOLDER)


