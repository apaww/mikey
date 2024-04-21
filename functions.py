import json
from mongo import prefixes, wallets, shops


with open('config.json', 'r', encoding="utf8") as f:
    data = json.load(f)
    token = data['token']
    dprefix = data['prefix']
    owner_id = data['owner_id']
    status = data['status']
    color = int(data['color'], 16)


async def get_sprefix(guild):
    sprefix = dprefix
    if find := prefixes.find_one({"server": str(guild.id)}):
        sprefix = find["prefix"]
    return sprefix


async def is_owner(uid):
    return uid == owner_id


async def create_wallet(uid, sid):
    if find := wallets.find_one({"uid": str(uid), "sid": str(sid)}):
        return
    wallets.insert_one({
        "uid": str(uid),
        "sid": str(sid),
        "bal": 0
    })


async def add_bal(uid, sid, amount):
    await create_wallet(uid, sid)
    bal = await get_bal(uid, sid)
    wallets.update_one({"uid": str(uid), "sid": str(sid)},
                       {"$set": {"bal": bal + amount}})


async def sub_bal(uid, sid, amount):
    await create_wallet(uid, sid)
    bal = await get_bal(uid, sid)
    wallets.update_one({"uid": str(uid), "sid": str(sid)},
                       {"$set": {"bal": bal - amount}})


async def get_bal(uid, sid):
    await create_wallet(uid, sid)
    wallet = int(wallets.find_one({"uid": str(uid), "sid": str(sid)})["bal"])
    return wallet


async def get_all_bals(sid):
    return wallets.find({"sid": str(sid)})


async def add_item(sid, item, cost):
    if find := shops.find_one({"sid": str(sid), "item": str(item)}):
        return False
    shops.insert_one({
        "sid": str(sid),
        "item": str(item),
        "cost": cost
    })
    return True


async def rm_item(sid, item):
    if find := shops.find_one({"sid": str(sid), "item": str(item)}):
        shops.delete_one({"sid": str(sid), "item": str(item)})
        return True
    return False


async def get_all_items(sid):
    return shops.find({"sid": str(sid)})


async def get_item(sid, item):
    return shops.find_one({"sid": str(sid), "item": str(item)})
