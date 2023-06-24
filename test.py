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



class ItemForm2(Form):
    item1 = FloatField("豆袋", validators=[validators.DataRequired()])


class ItemForm(FlaskForm):
    def __init__(self, store_items):
        self.entries = []
        for key in store_items.keys():
            self.entries.append(FloatField(str(key), validators=[validators.DataRequired()]))


def create(store_items):
    class ItemForm3(Form):
        ...

    for i, key in enumerate(store_items.keys()):
        setattr(ItemForm3, "item" + str(i), FloatField(str(key), validators=[validators.DataRequired()]))

    return ItemForm3


test = create(get_store_items(16))
#print(getattr(test, "item1"))

test2 = ItemForm2()
print(dir(test2.item1))