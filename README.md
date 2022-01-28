# pyRepBot - [Telegram](https://www.telegram.org/) Private Group Reputation Bot



Table of Contents
-----------------

  * [Requirements](#Requirements)
  * [Installation](#Installation)
  * [Usage](#Usage)

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
If you want to run the bot with in the background you can do:
```bash
nohup python3 bot.py &
```

*WORK_IN PROGRESS*

*Enjoy!*