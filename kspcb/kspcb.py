"""Crawler to download pollution data of lakes and rivers of Bangalore
from Karnataka State Pollution Control Board (KSPCB) dashboards.

https://tpro.telsys.in/tpportal/kspcblake
https://tpro.telsys.in/tpportal/kspcbriver
"""
from pathlib import Path
import datetime
from zoneinfo import ZoneInfo
import requests
import click

URLS = {
    "lake": "https://tpro.telsys.in/tpportal/kspcblake",
    "river": "https://tpro.telsys.in/tpportal/kspcbriver"
}

@click.group()
def app():
    pass


def get_current_timestamp():
    """Returns current timestamp in IST in YYYYMMDDHH format.
    """
    return datetime.datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y%m%d%H")

@app.command()
@click.option("-d", "--directory", help="path to download the snapshot (default: html/)", default="html")
def download(directory):
    """Download a snapshot of the bwssb dashboard.
    """
    download_html(directory, "lake")
    download_html(directory, "river")

def download_html(directory, kind):
    """Download HTML for lake or river.
    """
    url = URLS[kind]
    timestamp = get_current_timestamp()
    month = timestamp[:6]
    path = Path(directory) / kind / month / (timestamp + ".html")
    path.parent.mkdir(parents=True, exist_ok=True)

    print("downloading", url)
    html = requests.get(url).text
    print("writing to", path)
    path.write_text(html)


if __name__ == "__main__":
    app()