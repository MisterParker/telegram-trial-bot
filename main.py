from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.ext.dispatcher import run_async
import requests
import re
from env import getenv
import json

def get_users():
    try:
        with open("users.json") as f:
            data = json.load(f)
            return data
    except Exception as e:
        if (
            type(e).__name__ == "JSONDecodeError"
            or type(e).__name__ == "FileNotFoundError"
        ):
            open("users.json", "w+").write(json.dumps({}))
            return {}
        else:
            logging.error("Exception occured", exc_info=True)
    return False


def save_users(users):
    try:
        open("users.json", "w").write(json.dumps(users))
    except Exception:
        logging.error("Exception occured", exc_info=True)


def add_user(chat_id, username, first_name):
    users = get_users()
    user_data = {
        "username": username,
        "first_name": first_name,
    }
    users[str(chat_id)] = user_data
    save_users(users)

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

def get_image_url():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url

@run_async
def bop(update, context):
    url = get_image_url()
    add_user(chat_id, update.message.chat.username, update.message.chat.first_name)
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)

def main():
    updater = Updater(getenv('TELEGRAM_API_KEY'), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop',bop))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()