from modules.login import read_config, CONFIG_DIR
import requests


def upload(key, file):
    with open(file, "rb") as file_obj:
        r = requests.post(
            "https://api.e-z.host/files",
            headers={"key": key},  # Set API key in headers
            files={"file": file_obj}  # Pass the opened file
        )

    if r.status_code not in (200, 401, 403):
        raise ValueError(f"Upload failed with status code {r.status_code}")

    elif r.status_code in (401, 403):
        raise ValueError("Authorization error. Is your API key correct?")

    res = r.json()

    return res["imageUrl"], res["rawUrl"], res["deletionUrl"], r.status_code


def shorten(key, url):
    r = requests.post(
        "https://api.e-z.host/shortener",
        headers={"key": key},
        data={"url": url}
    )

    if r.status_code not in (200, 401, 403):
        raise ValueError(f"Shorten failed with status code {r.status_code}")

    elif r.status_code in (401, 403):
        raise ValueError("Authorization error. Is your API key correct?")

    res = r.json()

    return res["shortendUrl"], res["deletionUrl"], r.status_code

if __name__ == '__main__':
    print("This is a module. Please run `main.py`")