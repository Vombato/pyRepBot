# pyRepBot - [Telegram](https://www.telegram.org/) Private Group Reputation Bot

[![Pylint](https://github.com/Vombato/pyRepBot/actions/workflows/pylint.yml/badge.svg)](https://github.com/Vombato/pyRepBot/actions/workflows/pylint.yml) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

---

Table of Contents
-----------------

  * [Requirements](#Requirements)
  * [Installation](#Installation)
  * [Usage](#Usage)
  * [Bot Commands](#Commands)

## Requirements

**pyRepBot** requires the following pip packages to run:

- [python-dotenv](https://pypi.org/project/python-dotenv/) any version
- [pymongo/pymongo[srv]](https://pypi.org/project/pymongo/) 4.0.0+
- [python-telegram-bot](https://pypi.org/project/python-telegram-bot/) 13.10+

Those packages can be easily installed by running the commands below in "Installation" section.

## **Installation**

```bash
git clone https://github.com/Vombato/pyRepBot
cd /pyRepBot
pip install -r requirements.txt
```

Create a `.env` using `.env-template` as template setting each variable as necessary

Example:

```python
TOKEN = YOUR_TELEGRAM_BOT_TOKEN
OWNER_ID = YOU_TELEGRAM_PERSONAL_ID
MONGODB_USER = username
MONGODB_PSW = password
MONGODB_SERVER = @yourmongodbaddress
```

## **Usage**

```bash
python3 bot.py
```
If you want to run the bot in the background you can do:
```bash
nohup python3 bot.py &
```

## **Commands**

### Admin commands

### **Add Reputation**

Send `+++` as a reply to the user's message

###  **Remove Reputation**

Send `+++` as a reply to the user's message

### **Display the leaderboard**

`/classifica`

-------
### Owner commands


### **Add Admin**

`/AddAdmin`  as a reply to the user's message

---
# WORK IN PROGRESS

*Some strings and commands are still in italian, for the moment I have no plans to translate them for internatonalization, if you wish to do so you are welcome to make a **PR** or **fork** the project!*

### *Enjoy!*
