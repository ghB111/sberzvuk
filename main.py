from fastapi import FastAPI, status
import boto3
import os
import requests

import config
import s3_config
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


def upload_file(file_name: str, bucket: str, object_name=None):
    """Upload a file to an S3 bucket

    @param file_name: File to upload
    @param bucket: Bucket to upload to
    @param object_name: S3 object name. If not specified then file_name is used
    """

    if object_name is None:
        object_name = os.path.basename(file_name)

    s3_client = boto3.client(
        service_name="s3",
        endpoint_url=s3_config.endpoint_url,
        aws_access_key_id=s3_config.key_id,
        aws_secret_access_key=s3_config.access_key,
        use_ssl=False,
        verify=False,
    )

    s3_client.upload_file(file_name, bucket, object_name)


@app.post("/recognise", status_code=status.HTTP_200_OK)
def read_input(source: str, prefix: str):
    r = requests.get(source, allow_redirects=True)
    dest_folder = config.DOWNLOADS_FOLDER
    download(source, dest_folder, prefix)

    recognitions.make_all_recognition(prefix)

    return {}
