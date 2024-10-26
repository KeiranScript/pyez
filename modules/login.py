from pathlib import Path
import json
import requests
from typer import echo

CONFIG_DIR = Path("~/.config/pyE-Z/config.json").expanduser()

DEFAULT = {
    "API_KEY": "",
    "COPY_TO_CLIPBOARD": True,
    "DEBUG": True,
    "RAW_FILE": False
}


def initialize_config():
    if not CONFIG_DIR.exists():
        Path.mkdir(CONFIG_DIR.parent, exist_ok=True)
        with CONFIG_DIR.open("w") as file:
            json.dump(DEFAULT, file, indent=4)
        echo(f"Created {CONFIG_DIR} with default values")
        return DEFAULT
    return read_config()


def read_config() -> dict:
    if not CONFIG_DIR.exists():
        return initialize_config()

    try:
        with CONFIG_DIR.open("r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        echo("Invalid JSON in config file, resetting to defaults.")
        return initialize_config()


def save_config(config: dict):
    with CONFIG_DIR.open("w") as file:
        json.dump(config, file, indent=4)


def get_value(key: str):
    config = read_config()
    return config.get(key, None)


def login():
    config = read_config()

    if not config["API_KEY"]:
        while True:
            config["API_KEY"] = input("Please enter your API key: ")

            if not validate_key(config["API_KEY"]):
                echo("Invalid API key, please try again.")
                continue
            break

    save_config(config)
    echo("Login successful.")


def validate_key(key: str) -> bool:
    if not key:
        return False

    response = requests.get(f"https://api.e-z.gg/paste/config?key={key}")

    return response.status_code == 200


def config_dir():
    echo("Configuration directory: " + str(CONFIG_DIR))


if __name__ == '__main__':
    login()
