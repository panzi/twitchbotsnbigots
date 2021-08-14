#!/usr/bin/env python3

from typing import Set
from codecs import BOM_UTF8, BOM_UTF16_BE, BOM_UTF16_LE, BOM_UTF32_BE, BOM_UTF32_LE

import io
import csv
import zipfile

import requests

URL = 'https://github.com/hackbolt/twitchbotsnbigots/raw/main/Bots%20n%20Bigots.zip'

def decode_using_bom(data: bytes) -> str:
    if data.startswith(BOM_UTF16_BE):
        value = data[len(BOM_UTF16_BE):].decode('UTF-16BE', errors='replace')

    elif data.startswith(BOM_UTF16_LE):
        value = data[len(BOM_UTF16_LE):].decode('UTF-16LE', errors='replace')

    elif data.startswith(BOM_UTF32_BE):
        value = data[len(BOM_UTF32_BE):].decode('UTF-32BE', errors='replace')

    elif data.startswith(BOM_UTF32_LE):
        value = data[len(BOM_UTF32_LE):].decode('UTF-32LE', errors='replace')

    elif data.startswith(BOM_UTF8):
        value = data[len(BOM_UTF8):].decode('UTF-8', errors='replace')

    else:
        value = data.decode('UTF-8', errors='replace')

    return value

def update() -> None:
    print(f"Downloading {URL} ...")
    response = requests.get(URL)
    response.raise_for_status()
    bots: Set[str] = set()
    count = 0

    print("Reading file...")
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip:
        with zip.open("Bots n Bigots.csv", "r") as fp:
            data = fp.read()

    text = decode_using_bom(data)

    print("Converting file...")
    for row in csv.reader(io.StringIO(text)):
        for cell in row:
            cell = cell.strip()
            if cell and 'Compiled by Hackbolt' not in cell:
                bots.add(cell)
                count += 1

    sorted_bots = sorted(bots)

    print("Writing new file...")
    with open("bots_n_bigots.csv", "w") as outfp:
        csv.writer(outfp).writerows([bot] for bot in sorted_bots)

    print(f"Entries: {count:7d}")
    print(f"Unique:  {len(sorted_bots):7d}")
    print(f"Doubled: {count - len(sorted_bots):7d}")

if __name__ == '__main__':
    update()
