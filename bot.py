#!/usr/bin/env python
# pylint: disable=C0116,W0613

import logging
import os
import json
import pymongo as Mongo

from dotenv import load_dotenv, find_dotenv

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


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
client = Mongo.MongoClient("mongodb+srv://"+MONGODB_USER+":"+MONGODB_PSW+MONGODB_SERVER)
db = client.repbot.users

admins = []

def getUser(idToFind, name):
    res = db.find_one({"user_id": idToFind})
    if res is None:
        print("Found no one, inserting it")
        insertNew(idToFind, name)
        res = getUser(idToFind, name)
    print ("Found user: " + str(res))
    return res

def insertNew(idtoInsert, name):
    db.insert_one({"user_id": idtoInsert, "name": name, "rep": 0, "lvl": 0})

def addRep(usrToUpdate):
    try:
        newrep = usrToUpdate["rep"] + 1
        result = db.update_one({"user_id":usrToUpdate["user_id"]},{ "$set": { "rep" : newrep}})
    except:
        print("Error while adding rep")

def decRep(usrToUpdate):
    try:
        newrep = usrToUpdate["rep"] - 1
        result = db.update_one({"user_id":usrToUpdate["user_id"]},{ "$set": { "rep" : newrep}})
    except:
        print("Error while adding rep")

def updateName(idtoUpdate, name):
    try:
        result = db.update_one({"user_id":idtoUpdate},{"$set":{ "name" : name}})
    except:
        print("Error while updating name")


def getLeaderboard():
    res = db.find().sort("rep", -1)
    return res

def checkAdmin(id):
    res = client.repbot.admins.find_one({"user_id": id})
    if res is not None:
        return True
    return False

def addAdmin(id, name):
    client.repbot.admins.insert_one({"user_id": id, "name": name})

def initAdmins():
    res = client.repbot.admins.find()
    print(str(res))
    for i in res:
        print("Caricato admin: "+ i["name"] +" - "+ i["user_id"])
        admins.append(i["user_id"])

# Commands

def leaderboardCommand(update: Update, context: CallbackContext) -> None:
    sender = str(update.message.from_user.id)
    for admin in admins:
        admin = str(admin)
        if admin == sender:
            elems = getLeaderboard()
            msg = "Classifica Reputazione\n\n"
            count = 1
            for elem in elems[:10]:
                msg = msg +str(count)+". "+str(elem["name"]) + "  ✨Punteggio: " + str(elem["rep"])+"\n"
                count = count + 1
            update.message.reply_text(msg)


def addAdminCommand(update: Update, context: CallbackContext) -> None:
    sender = update.message.from_user
    replier = getattr(update.message.reply_to_message, 'from_user', None)
    senderID = str(sender.id)
    if ( replier is not None):
        replierID = str(replier.id)
        replierName = str(replier.first_name)
        for admin in admins:
            admin = str(admin)
            if admin == sender:
                if not checkAdmin(replierID):
                    addAdmin(replierID, replierName)
    else:
        # DEBUG
        update.message.reply_text("Non era una risposta a qualcosa")


def checkifRepMsg(update: Update, context: CallbackContext) -> None:
    if update.message.text == "+++" or update.message.text == "---":
        sender = update.message.from_user.id
        replier = getattr(update.message.reply_to_message, 'from_user', None)
        if ( replier is not None):
            replierID = replier.id
            replierName = replier.first_name
            sender = str(sender)
            replierID = str(replierID)
            for admin in admins:
                admin = str(admin)
                if admin == sender:
                    usr = getUser(replierID, replierName)
                    repNow = usr["rep"]
                    if update.message.text == "+++":
                        addRep(usr)
                        update.message.reply_text("🆙 - Aumentata la ✨ reputazione ✨  di " + replierName + " da " + str(repNow) + " 👉 " + str(repNow+1) + "!")
                    else:
                        decRep(usr)
                        update.message.reply_text("⚠️ - Diminuita la ✨ reputazione ✨  di " + replierName + " da " + str(repNow) + " 👉 " + str(repNow-1) + "!")
                    if replierName != usr["name"]:
                        updateName(replierID, replierName)
                    return
        else:
            # DEBUG
            update.message.reply_text("Non era una risposta a qualcosa")
    

def main() -> None:
    if not checkAdmin(OWNER_ID):
        addAdmin(OWNER_ID, "owner")
    initAdmins()
    # Create the Updater and pass it your bot's token.
    TOKEN = os.getenv('TOKEN')
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("classifica", leaderboardCommand))

    dispatcher.add_handler(CommandHandler("addMauritioAdmin", addAdminCommand))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, checkifRepMsg))
    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()