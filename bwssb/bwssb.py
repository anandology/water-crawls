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
import sys
import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import sqlite3

import click
import requests
from bs4 import BeautifulSoup
import pandas as pd

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

    # The HTML has javascript to only show one table and hide all others
    # and cycle the table shown as a slideshow.
    # Disabled all of it to see all the data at once.
    html = html.replace('slides[i].style.display = "none"', 'slides[i].style.display = "block"')
    html = html.replace('setTimeout', '// setTimeout')

    print("writing to", path)
    path.write_text(html)

def extract_table(table):
    """Extracts data from a table element of BeautifulSoup.
    """
    trs = table.select("tr")
    return [[cell.get_text().strip() for cell in tr.select("td, th")] for tr in trs]

def is_quality_table(data):
    """"Checks if the table data is for water quality or not.
    """
    try:
        return data[1][0].strip() == "Parameters" and data[2][0].strip() == "pH"
    except IndexError:
        return False

def sanitize_name(name):
    return name.lower().replace(" ", "_")

def process_water_quality_table(raw_data) -> pd.DataFrame:
    """Process the data of water quality table.
    """
    names = raw_data[0][1:]
    data = {name: {} for name in names}

    def process_row(row):
        param, *values = row
        if param == "Parameters":
            param = "timestamp"
        param = sanitize_name(param)

        for name, value in zip(names, values):
            data[name][param] = value

    for row in raw_data[1:]:
        process_row(row)

    return pd.DataFrame(data).transpose()

@app.command()
@click.argument("path")
def parse(path):
    """Parse the snapshot with given timestamp.
    """
    # month = timestamp[:6] # YYYYMM
    # filename = timestamp + ".html"
    # path = Path("html") / month / filename
    html = open(path).read()
    soup = BeautifulSoup(html, "lxml")
    tables = [extract_table(t) for t in soup.select("table")]

    recorded_timestamp = Path(path).stem

    dfs = [process_water_quality_table(t) for t in tables if is_quality_table(t)]
    df = pd.concat(dfs).reset_index(names=['stp_name'])

    df['updated_on'] = recorded_timestamp
    df.to_csv(sys.stdout, index=False)

@app.command()
@click.argument("paths", nargs=-1)
def load_db(paths):
    for path in paths:
        print("loading", path)
        df = pd.read_csv(path)
        updated_on = Path(path).stem

        with sqlite3.connect("bwssb.db") as conn:
            cur = conn.cursor()
            cur.execute("delete from water_quality where updated_on=?", [updated_on])

        conn = "sqlite:///bwssb.db"
        df.to_sql("water_quality", conn, if_exists='append', index=False)

if __name__ == "__main__":
    app()