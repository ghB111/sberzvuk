import os, sys

DOWNLOADS_FOLDER = "downloads"
def get_downloads_dir_path() -> str:
    return os.path.join(os.getcwd, DOWNLOADS_FOLDER)

def get_downloaded_video_path(prefix: str) -> str:
    return os.path.join(get_downloads_dir_path(), prefix)

PROCESSED_FOLDER = "processed"
def get_processed_dir_path() -> str:
    return os.path.join(os.getcwd, DOWNLOADS_FOLDER)


