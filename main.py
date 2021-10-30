from typing import Optional

from fastapi import FastAPI
from fastapi import FastAPI, status
import os
import requests

import config
import recognitions

app = FastAPI()

def download(url: str, dest_folder: str, filename: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename_refactored = filename.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_folder, filename_refactored)

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))

@app.post("/recognise", status_code= status.HTTP_200_OK )
def read_input(source: str, prefix: str):
    r = requests.get(source, allow_redirects=True)
    dest_folder =  config.DOWNLOADS_FOLDER
    download(source, dest_folder, prefix)

    recognitions.make_all_recognition(prefix)

    return {"source": len(r.content), "prefix":prefix} # todo return message



