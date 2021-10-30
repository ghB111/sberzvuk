import os, sys

DOWNLOADS_FOLDER = "downloads"
def get_downloads_dir_path() -> str:
    return os.path.join(os.getcwd, DOWNLOADS_FOLDER)


