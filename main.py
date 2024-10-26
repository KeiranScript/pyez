#!/usr/bin/env python3

from urllib.parse import urlparse, urlunparse
from modules.deleter import (delete_from_csv, delete_file,
                             append_to_csv, CSV_FILE)
from modules.login import (login, read_config,
                           save_config, CONFIG_DIR)
from modules.requests import upload, shorten
from pathlib import Path
import typer
import csv

app = typer.Typer(no_args_is_help=True, help="E-Z.gg CLI",
                  add_completion=False, add_help_option=False)


@app.command(
    name="print-config",
    help="Print the path to the configuration file.")
def print_config():
    typer.echo(CONFIG_DIR)


verbose = read_config()["DEBUG"] or False


@app.command(name="login", help="Save your API key")
def auth():
    login()
    return read_config()["API_KEY"] or None


@app.command(name="logout", help="Clear your API key from the config file.")
def logout():
    if auth() is None or read_config()["API_KEY"] == "":
        typer.echo("Please login first (pyez login)")
        return

    config = read_config()
    config["API_KEY"] = ""
    save_config(config)
    typer.echo("Logout successful.")


@app.command(name="config", help="Interactively edit the config file")
def edit_config():
    config = read_config()

    if not config:
        typer.echo("No configuration to edit.")
        return

    typer.echo("Current configuration:")
    for key, value in config.items():
        typer.echo(f"{key}: {value}")

    for key in config.keys():
        new_value = typer.prompt(
            f"Enter new value for {key} (leave blank to keep current value)",
            default=config[key])
        if new_value:
            config[key] = new_value

    save_config(config)


@app.command(name="upload", help="Upload a file to E-Z.gg")
def uploader(
        file: str = typer.Argument(None, help="The file to upload."),
        raw: bool = typer.Option(False, help="Include raw file URL."),
        domain: str = typer.Option(
            "i.e-z.gg", "--domain", "-d",
        help="Override the domain of the uploaded file.")
):
    if auth() is None or read_config()["API_KEY"] == "":
        typer.echo("Please login first (pyez login)")
        return

    if file is None:
        file = typer.prompt("Please enter the path to the file to upload")

    file_path = Path(file).expanduser()

    if not file_path.exists():
        typer.echo(f"File does not exist in {file_path}")
        return

    typer.echo(f"Uploading {file_path}...")

    imageUrl, rawUrl, deletionUrl, status_code = upload(
        read_config()["API_KEY"], file_path)

    parsed_url = urlparse(url=imageUrl)
    if domain.startswith("https://"):
        domain = domain.split("//")[1]
    modified_url = parsed_url._replace(netloc=domain)

    updated_imageUrl = urlunparse(modified_url)

    append_to_csv(deletionUrl, str(updated_imageUrl))

    typer.echo(f"Uploaded to {updated_imageUrl}")
    if raw:
        typer.echo(f"Raw file: {rawUrl}")
    typer.echo(f"Delete: {deletionUrl}")
    if verbose:
        typer.echo(f"Status code: {status_code}")


@app.command(name="shorten", help="Shorten a URL")
def shortener(
        url=typer.Argument(None,
                           help="The URL to shorten."),
):
    if auth() is None or read_config()["API_KEY"] == "":
        typer.echo("Please login first (pyez login)")
        if verbose:
            typer.echo(f"Api key: {read_config()['API_KEY']}")
        return

    if url is None:
        url = typer.prompt("Please enter the URL to shorten")

    typer.echo(f"Shortening {url}...")

    shortenedUrl, deletionUrl, status_code = shorten(
        read_config()["API_KEY"], url)

    append_to_csv(deletionUrl, shortenedUrl, verbose)

    typer.echo(f"Shortened to {shortenedUrl}")
    typer.echo(f"Delete: {deletionUrl}")
    if verbose:
        typer.echo(f"Status code: {status_code}")


@app.command(name="delete", help="Delete a file using its deletion URL")
def delete(
    index: int = typer.Argument(
        None,
        help="The index of the file to delete.")
):
    with open(CSV_FILE, mode='r', newline='') as file:
        rows = list(csv.reader(file))

    if index < 0 or index >= len(rows):
        typer.echo("Index out of range.")
        return

    deletion_url = rows[index][0]

    if delete_file(deletion_url):
        delete_from_csv(index)


if __name__ == '__main__':
    app()
