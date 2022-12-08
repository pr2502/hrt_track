#!/usr/bin/python3

from download import get_events
import json
import requests
import time


DB = "./db"
MEDS = [
    # transmasc
    ("0186652", "SUSTANON"),
    ("0223477", "NEBIDO"),
    # transfem
    ("0186147", "NEOFOLLIN"),
    ("0224641", "ANDROCUR 50MG"),
    ("0225253", "ANDROCUR 100MG"),
    ("0053797", "ESTROFEM 1MG"),
    ("0096491", "ESTROFEM 2MG"),
    ("0076922", "OESTROGEL"),
]


def load_events(code: str):
    try:
        with open(f"{DB}/{code}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_events(code: str, events):
    with open(f"{DB}/{code}.json", "w") as f:
        json.dump(events, f)

def load_secrets():
    with open("secrets.json", "r") as f:
        return json.load(f)


def discord_notif(message):
    for url in load_secrets()['discord_webhooks']:
        res = requests.post(url, json={ "username": "SÚKLtrack", "content": message })
        if len(res.text) > 0:
            print("discord_notif:", res.text)
        time.sleep(1)


def find_updates(old, new):
    def id(event):
        return event["event_type"] + event["start_date"]

    updates = []
    for event in new:
        if not any([id(event) == id(o) for o in old]):
            updates += [event]
    return updates


for code, name in MEDS:
    print(code, "...", end=" ")
    old = load_events(code)
    new = get_events(code)
    updates = find_updates(old, new)
    if len(updates) > 0:
        for update in updates:
            message = f"{name} {update['event_type']} {update['start_date']}"
            if update["replacement"] is not None:
                message += f", náhrada: '{update['replacement']}'"
            if update["reason"] is not None:
                message += f", z duvodu: '{update['reason']}'"
            if update["expected_return"] is not None:
                message += f", očekávané obnovení {update['expected_return']}"
            discord_notif(message)
    save_events(code, new)
    print("done")

