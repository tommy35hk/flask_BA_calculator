from flask import Flask, render_template, request
import sqlite3
from scipy.optimize import minimize
import numpy as np

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect("BlueArchive.db")
    conn.row_factory = sqlite3.Row
    return conn


def count_minimum(rewards, need, missions):
    bnds = [(0,10000) for _ in range(len(missions))]
    x0 = [1 for _ in range(len(missions))]
    cons = [
        {
            'type':'ineq',
            'fun': lambda x, coef=key: np.matmul(rewards[coef], x) - need[coef]
        } for key in rewards
    ]
    sol = minimize(lambda x: sum(x), x0, method="SLSQP", bounds=bnds,
                   constraints=cons)
    result = {mission: qty for mission, qty in zip(missions, sol.x)}
    return result


def get_missions(event_id):
    conn = get_db_connection()
    missions = conn.execute(
        "SELECT DISTINCT name FROM Missions "
        "WHERE event_ID = %i" % event_id
    )
    missions = [i['name'] for i in missions]

    return missions
def get_exhcange_store(event_id):
    conn = get_db_connection()
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
    conn = get_db_connection()
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


@app.route("/")
def index():
   conn = get_db_connection()
    events = conn.execute(
        "SELECT DISTINCT Events.event_ID, event_name FROM Events "
        "INNER JOIN Missions "
        "ON Events.event_id = Missions.event_ID"
    )
    events = events.fetchall()
    events = {event["event_ID"]: event["event_name"] for event in events}
    return

@app.route("/result", methods=['POST', 'GET'])
def result():
    store_items = get_exhcange_store(16)
    missions = get_missions(16)

    if request.method == 'POST':
        form = request.form
        need = {}
        for key, val in store_items.items():
            temp = 0
            for i in val:
                temp += i['Cost'] * int(form.get(i['Name']))
            need[key] = temp
        rewards = get_reward(16)
        for key, val in rewards.items():
            rewards[key] = [i * round(1 + float(form.get(key+'reward'))) for i in val]
        result = count_minimum(rewards, need, missions)
    else:
        result = None
    return render_template("result.html", store_items=store_items, result=result)


