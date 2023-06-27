import sqlite3
from flask_wtf import FlaskForm
from wtforms import validators, FloatField, Form

conn = sqlite3.connect("BlueArchive.db")
conn.row_factory = sqlite3.Row


def get_store_items(event_id):
    store_items = {}
    items = conn.execute(
        "SELECT item_ID, item_name FROM Items "
        "WHERE event_ID = %i" % event_id
    )
    items = items.fetchall()
    for item_id, item_name in items:
        store_item = conn.execute(
            "SELECT Name, Cost, start_qty FROM Exchange_Store "
            "WHERE item_ID = %i" % item_id
        )
        store_item = store_item.fetchall()
        store_items[item_name] = store_item

    return store_items

def get_reward(event_id):
    rewards = {}
    items = conn.execute(
        "SELECT item_ID, item_name FROM Items "
        "WHERE event_ID = %i" % event_id
    )
    items = items.fetchall()
    for item_id, item_name in items:
        reward = conn.execute(
            "SELECT reward FROM Missions "
            "WHERE item_ID = %i" % item_id
        )
        reward = [i["reward"] for i in reward]
        rewards[item_name] = reward
    return rewards


def get_missions(event_id):
    missions = conn.execute(
        "SELECT DISTINCT name FROM Missions "
        "WHERE event_ID = %i" % event_id
    )
    missions = [i['name'] for i in missions]

    return missions


test = get_missions(16)
print(test)