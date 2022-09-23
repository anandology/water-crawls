"""Script to download and parse the data from BWSSB real-time dashboard.

USAGE:

download a snapshot:

    $ python bwssb.py download
    saving html/202209/2022092010.html

Parse a snapshot:

    $ python bwssb.py parse 2022092010
    reading html/202209/2022092010.html
    saving data/raw/202209/2022092010.csv
    generating data/daily/202209/2022092010.csv
    generating data/monthly/202209/2022092010.csv

Parse all pending snapshots:

    $ python bwssb.py parse-all
    ...

Re-parse all snapshots:

    $ python bwssb.py parse-all --force
    ...

"""
import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import click
import requests

URL = "https://tpro.telsys.in/tpportal/bwssb"

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
    timestamp = get_current_timestamp()
    month = timestamp[:6]
    path = Path(directory) / month / (timestamp + ".html")
    path.parent.mkdir(parents=True, exist_ok=True)

    print("downloading", URL)
    html = requests.get(URL).text

    html = html.replace('slides[i].style.display = "none"', 'slides[i].style.display = "block"')
    html = html.replace('setTimeout', '// setTimeout')

    print("writing to", path)
    path.write_text(html)


@app.command()
def parse(timestamp):
    """Parse the snapshot with given timestamp.
    """
    pass

if __name__ == "__main__":
    app()