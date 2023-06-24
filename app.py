from flask import Flask, render_template, request
import sqlite3
from flask_wtf import FlaskForm
from wtforms import Form, FloatField, validators

app = Flask(__name__)


def create_bonus_form(store_items):
    class BonusForm(Form):
        ...

    for key in store_items.keys():
        setattr(BonusForm, str(key), FloatField(str(key), validators=[validators.DataRequired()]))

    return BonusForm

def get_db_connection():
    conn = sqlite3.connect("BlueArchive.db")
    conn.row_factory = sqlite3.Row
    return conn


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


@app.route("/")
def index():
    conn = get_db_connection()
    store_items = get_exhcange_store(16)
    form = create_bonus_form(store_items)
    return render_template("index.html", form=form, store_items=store_items)


@app.route("/data", methods = ["POST", "GET"])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        r = form.r.data
        return render_template("data.html", json_data=json_data)
