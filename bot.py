# !/usr/bin/env python
# pylint: disable=C0116,W0613
# pylint: disable=broad-except
# pylint: disable=missing-docstring

import logging
import os

import pymongo as mongo
from dotenv import load_dotenv, find_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

load_dotenv(find_dotenv())

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

OWNER_ID = os.environ.get('OWNER_ID')

MONGODB_USER = os.environ.get('MONGODB_USER')
MONGODB_PSW = os.environ.get('MONGODB_PSW')
MONGODB_SERVER = os.environ.get('MONGODB_SERVER')
client = mongo.MongoClient(
    "mongodb+srv://" + MONGODB_USER + ":" + MONGODB_PSW + MONGODB_SERVER)
db = client.repbot.users

admins = []


def get_user(id_to_find, name):
    res = db.find_one({"user_id": id_to_find})
    if res is None:
        print("Found no one, inserting it")
        insert_new(id_to_find, name)
        res = get_user(id_to_find, name)
    print("Found user: " + str(res))
    return res


def insert_new(id_to_insert, name):
    db.insert_one({"user_id": id_to_insert, "name": name, "rep": 0, "lvl": 0})


def inc_rep(usr_to_update):
    newrep = usr_to_update["rep"] + 1
    db.update_one({"user_id": usr_to_update["user_id"]}, {
        "$set": {"rep": newrep}})


def dec_rep(usr_to_update):
    newrep = usr_to_update["rep"] - 1
    db.update_one({"user_id": usr_to_update["user_id"]}, {
        "$set": {"rep": newrep}})


def update_name(id_to_update, name_to_update):
    db.update_one({"user_id": id_to_update},
                  {"$set": {"name": name_to_update}})


def get_leaderboard():
    res = db.find().sort("rep", -1)
    return res


def check_admin(id_to_check):
    res = client.repbot.admins.find_one({"user_id": id_to_check})
    if res is not None:
        return True
    return False


def add_admin(id_to_add, name_to_add):
    client.repbot.admins.insert_one(
        {"user_id": id_to_add, "name": name_to_add})


def init_admins():
    res = client.repbot.admins.find()
    print(str(res))
    for i in res:
        print("Caricato admin: " + i["name"] + " - " + i["user_id"])
        admins.append(i["user_id"])


# Telegram Chat Commands

def leaderboard_cmd(update: Update) -> None:
    sender = str(update.message.from_user.id)
    for admin in admins:
        admin = str(admin)
        if admin == sender:
            elems = get_leaderboard()
            msg = "Classifica Reputazione\n\n"
            count = 1
            for elem in elems[:10]:
                msg = msg + \
                    str(count) + ". " + str(elem["name"]) + \
                    "  ✨Punteggio: " + str(elem["rep"]) + "\n"
                count = count + 1
            update.message.reply_text(msg)


def add_admin_cmd(update: Update) -> None:
    sender = update.message.from_user
    replier = getattr(update.message.reply_to_message, 'from_user', None)
    sender_id = str(sender.id)
    if replier is not None:
        replier_id = str(replier.id)
        print("Called addAdmin command for user: " + replier_id)
        replier_name = str(replier.first_name)
        if sender_id == OWNER_ID:
            if not check_admin(replier_id):
                add_admin(replier_id, replier_name)
                print("Aggiunto Admin: " + replier_name)
                update.message.reply_text("Aggiunto Admin: " + replier_name)
    else:
        # DEBUG
        update.message.reply_text("Non era una risposta a qualcosa")


def rep_cmd(update: Update) -> None:
    if update.message.text in ("+++", "---"):
        sender = update.message.from_user.id
        replier = getattr(update.message.reply_to_message, 'from_user', None)
        if replier is not None:
            replier_id = replier.id
            replier_name = replier.first_name
            sender = str(sender)
            replier_id = str(replier_id)
            for admin in admins:
                admin = str(admin)
                if admin == sender:
                    usr = get_user(replier_id, replier_name)
                    rep_now = usr["rep"]
                    if update.message.text == "+++":
                        inc_rep(usr)
                        update.message.reply_text(
                            "🆙 - Aumentata la ✨ reputazione ✨  di " + replier_name + " da " + str(
                                rep_now) + " 👉 " + str(rep_now + 1) + "!")
                    else:
                        dec_rep(usr)
                        update.message.reply_text(
                            "⚠️ - Diminuita la ✨ reputazione ✨  di " + replier_name + " da " + str(
                                rep_now) + " 👉 " + str(rep_now - 1) + "!")
                    if replier_name != usr["name"]:
                        update_name(replier_id, replier_name)
                    return
        else:
            # DEBUG
            update.message.reply_text("Non era una risposta a qualcosa")


def main() -> None:
    if not check_admin(OWNER_ID):
        add_admin(OWNER_ID, "owner")
    init_admins()
    # Create the Updater and pass it your bot's token.
    bot_token = os.getenv('TOKEN')
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("classifica", leaderboard_cmd))

    dispatcher.add_handler(CommandHandler("addAdmin", add_admin_cmd))

    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, rep_cmd))
    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
