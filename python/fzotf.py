#!/usr/bin/env python3

import argparse
import datetime
import json
import pathlib
import shutil
import sqlite3
import sys
import tempfile


def format_creators(creators):
    """Generate an abbreviated string representation of the authors"""
    creators.sort(key=lambda x: x[2])
    output = ", ".join([x[1] for x in creators[0:3]])
    if len(creators) > 3:
        output = output + " et al"
    return output


def format_date(date):
    """Generate an abbreviated string representation of the date"""
    if date[8:10] != "00" and date[5:7] != "00":
        return datetime.datetime.strptime(date[0:10], "%Y-%m-%d").strftime("%Y %b %d")

    if date[5:7] != "00":
        return datetime.datetime.strptime(date[0:7], "%Y-%m").strftime("%Y %b")

    return date[0:4]


def format_entry(citekey, data, creators):
    """Generate a one-line string representing the item"""
    # Transform data into a dictionary
    item_data = {x[1]: x[2] for x in data}
    output = citekey.ljust(20)

    if len(creators) > 0:
        output = " ".join([output, format_creators(creators)]) + "."

    if "title" in item_data:
        output = " ".join([output, item_data["title"]]) + "."

    if "publicationTitle" in item_data:
        output = " ".join([output, item_data["publicationTitle"]]) + "."

    if "date" in item_data:
        output = " ".join([output, format_date(item_data["date"])]) + ";"

    if "volume" in item_data:
        output = "".join([output, item_data["volume"]])

    if "issue" in item_data:
        output = "".join([output, "(", item_data["issue"], ")"])

    if "pages" in item_data:
        if "volume" in item_data or "issue" in item_data:
            output = ":".join([output, item_data["pages"]])
        else:
            output = " ".join([output, item_data["pages"]])

    if "DOI" in item_data:
        output = ". doi:".join([output, item_data["DOI"]])

    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Print a list of citekeys and citations from Zotero, one per line",
        epilog="Requires the Better BibTeX extension",
    )
    parser.add_argument(
        "-z", "--zotdir", help="path to zotero data directory (default: ~/Zotero)"
    )
    args = parser.parse_args()
    zotdir = args.zotdir if args.zotdir else "~/Zotero"

    with tempfile.TemporaryDirectory() as cachedir:
        # Copying the database gets around the fact that Better BibTeX and
        # Zotero sometimes lock the database
        shutil.copy(
            str(pathlib.Path(zotdir).expanduser() / "better-bibtex.sqlite"), cachedir
        )
        shutil.copy(str(pathlib.Path(zotdir).expanduser() / "zotero.sqlite"), cachedir)

        bbt_conn = sqlite3.connect(pathlib.Path(cachedir) / "better-bibtex.sqlite")
        bbt_c = bbt_conn.cursor()
        bbt_query = (
            "SELECT data from `better-bibtex` WHERE name = 'better-bibtex.citekey'"
        )
        bbt_c.execute(bbt_query)
        citekeys = {
            item["itemKey"]: item["citekey"]
            for item in json.loads(bbt_c.fetchone()[0])["data"]
        }
        bbt_conn.close()

        zdb_conn = sqlite3.connect(pathlib.Path(cachedir) / "zotero.sqlite")
        zdb_c = zdb_conn.cursor()
        zdb_data_query = """
            SELECT items.key, fields.FieldName, itemDataValues.value
            FROM itemData
            LEFT JOIN items ON itemData.itemID = items.itemID
            LEFT JOIN fields on itemData.fieldID = fields.fieldID
            LEFT JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
            WHERE itemData.fieldID IN (110, 12, 14, 4, 5, 10, 26)
            """
        zdb_data = zdb_c.execute(zdb_data_query).fetchall()
        zdb_creators_query = """
            SELECT items.key, creators.lastName, itemCreators.orderIndex
            FROM itemCreators
            LEFT JOIN items on itemCreators.itemID = items.itemID
            LEFT JOIN creators on itemCreators.creatorID = creators.creatorID
            """
        zdb_creators = zdb_c.execute(zdb_creators_query).fetchall()
        zdb_conn.close()

    for itemKey, citekey in citekeys.items():
        print(
            format_entry(
                citekey,
                [x for x in zdb_data if x[0] == itemKey],
                [x for x in zdb_creators if x[0] == itemKey],
            )
        )
