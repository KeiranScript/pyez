import csv
import requests

CSV_FILE = "uploads.csv"


def append_to_csv(deletion_url: str, url: str, debug: bool = False):
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([deletion_url, url])
    if debug: print(f"Appended {deletion_url} and {url} to {CSV_FILE}")


def delete_from_csv(index: int, debug: bool = False):
    with open(CSV_FILE, mode='r', newline='') as file:
        rows = list(csv.reader(file))

    if index < 0 or index >= len(rows):
        if debug: print("Index out of range.")
        return

    del rows[index]

    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    if debug: print(f"Removed entry at index {index} from {CSV_FILE}")


def delete_file(deletion_url: str, debug: bool = False):
    response = requests.get(deletion_url)
    if response.status_code == 200:
        print(f"Successfully deleted file at {deletion_url}")
        return True
    else:
        if debug: print(f"Failed to delete file at {deletion_url}. Status code: {response.status_code}")
        return False