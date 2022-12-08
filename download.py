#!/usr/bin/python3

import bs4
import json
import requests


def map_row(row):
    cells = list(row.find_all("td"))

    if len(cells) == 0:
        return None

    def map_field(field):
        if field is None:
            return None
        text = str(field).strip()
        if len(text) == 0:
            return None
        return text


    return {
        "event_type": map_field(cells[0].string),
        "start_date": map_field(cells[1].string),
        "replacement": map_field(cells[2].string),
        "reason": map_field(cells[3].string),
        "expected_return": map_field(cells[4].string),
    }


def get_events(code: str):
    url = f"https://www.sukl.cz/modules/medication/detail.php?code={code}&tab=available"
    html = requests.get(url).text
    soup = bs4.BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if table is None:
        return []
    rows = [row for row in map(map_row, table.find_all("tr")) if row is not None]
    return rows[::-1]


def main(args):
    code = args[0]
    events = get_events(code)
    print(json.dumps(events))


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
