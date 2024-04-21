from pymongo import MongoClient
import json

with open('config.json', 'r', encoding="utf8") as f:
    data = json.load(f)
    db_url = data['db_url']

client = MongoClient(db_url)

db = client.mikey

prefixes = db.prefixes
wallets = db.wallets
toggle = db.toggle
shops = db.shops