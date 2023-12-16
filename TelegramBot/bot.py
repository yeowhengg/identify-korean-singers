import os
from dotenv import load_dotenv
from telebot import TeleBot
import requests

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
API_URL = "http://backend:8000/"

bot = TeleBot(BOT_TOKEN)


def send_image(local_file_path):

    url = f'{API_URL}uploadfiles/'
    print(url)
    file_path = f"https://api.telegram.org/file/bot{BOT_TOKEN}/photos/{local_file_path}"
    get_image_res = requests.get(file_path)
    read_files = {"files": (local_file_path, get_image_res.content)}
    response = requests.post(url, files=read_files)

    return response


@bot.message_handler(content_types=['photo', 'text'])
def handle_photo(message):
    if message.photo:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path.replace("photos/", "")

        if file_path.endswith(".jpg"):
            photo_id_tag = message.id

            bot.send_message(message.chat.id, "processing image",
                             reply_to_message_id=photo_id_tag)
            print(f"sending image to server... {file_path}")
            status = send_image(file_path)

            if status.status_code == 200:

                # rantext to be replaced with idol description
                # placeholder# details over here should be the description of idols. Callback is handled by 127.0.0.1 backend
                import random as ran
                randomstuff = ["1", "2", "3", "4"]
                rantext = ran.choice(randomstuff)
                bot.send_message(message.chat.id, rantext,
                                 reply_to_message_id=photo_id_tag)

            else:
                bot.send_message(message.chat.id,
                                 "something went wrong.. please try again later..")

                print(status.raise_for_status())

        else:
            bot.send_message(message.chat.id, "Please send a JPG file.")

    else:
        bot.send_message(
            message.chat.id, "Please send a valid photo that is in the JPG format")


@bot.message_handler(commands=['start', 'help'])
def message_handler(message):
    bot.send_message(
        message.chat.id, "Upload image(s) in .jpg format to continue")


print("bot started")
bot.infinity_polling()
